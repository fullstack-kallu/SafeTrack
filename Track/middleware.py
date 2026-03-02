import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


class TabScopedSessionMiddleware:
    """
    Keep auth/session keys isolated per browser tab using a tab id (_tsid).

    Existing view code can continue using request.session['u_id'], etc.
    This middleware hydrates those keys from a tab-specific store at request
    start and writes them back to the same tab entry at response time.
    """

    TAB_ID_PARAM = "_tsid"
    TAB_STORE_KEY = "_tab_sessions"
    MANAGED_KEYS = ("username", "u_id", "user_type", "emp_id", "myworker_id")
    SCRIPT_MARKER = "tab-session-bridge"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._hydrate_request_session(request)
        response = self.get_response(request)
        response = self._persist_request_session(request, response)
        response = self._inject_tab_script(response)
        return response

    def _extract_tab_id(self, request):
        tab_id = (
            request.GET.get(self.TAB_ID_PARAM)
            or request.POST.get(self.TAB_ID_PARAM)
            or request.headers.get("X-Tab-Session")
        )
        if not tab_id:
            return None
        tab_id = str(tab_id).strip()
        return tab_id or None

    def _hydrate_request_session(self, request):
        tab_id = self._extract_tab_id(request)
        request._tab_session_id = tab_id
        if not tab_id:
            return

        store = request.session.get(self.TAB_STORE_KEY, {})
        tab_data = store.get(tab_id)

        # First request in a tab can arrive with _tsid before this tab has been
        # persisted in _tab_sessions. In that case keep the current session as-is
        # and let _persist_request_session seed the tab entry.
        if tab_data is None:
            return
        if not isinstance(tab_data, dict):
            return

        for key in self.MANAGED_KEYS:
            request.session.pop(key, None)

        for key in self.MANAGED_KEYS:
            if key in tab_data:
                request.session[key] = tab_data[key]

    def _persist_request_session(self, request, response):
        tab_id = getattr(request, "_tab_session_id", None)
        if not tab_id:
            return response

        store = dict(request.session.get(self.TAB_STORE_KEY, {}) or {})
        tab_data = dict(store.get(tab_id, {}) or {})

        for key in self.MANAGED_KEYS:
            if key in request.session:
                tab_data[key] = request.session[key]
            else:
                tab_data.pop(key, None)

        if any(key in tab_data for key in self.MANAGED_KEYS):
            store[tab_id] = tab_data
        else:
            store.pop(tab_id, None)

        request.session[self.TAB_STORE_KEY] = store
        request.session.modified = True

        return self._append_tsid_to_redirect(response, tab_id)

    def _append_tsid_to_redirect(self, response, tab_id):
        location = response.get("Location")
        if not location or not (300 <= response.status_code < 400):
            return response

        if location.startswith(("javascript:", "mailto:", "tel:")):
            return response

        parts = urlsplit(location)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        if self.TAB_ID_PARAM in query:
            return response

        query[self.TAB_ID_PARAM] = tab_id
        new_query = urlencode(query, doseq=True)
        response["Location"] = urlunsplit(
            (parts.scheme, parts.netloc, parts.path, new_query, parts.fragment)
        )
        return response

    def _inject_tab_script(self, response):
        content_type = (response.get("Content-Type") or "").lower()
        if "text/html" not in content_type:
            return response

        content = getattr(response, "content", b"")
        if not content:
            return response

        if self.SCRIPT_MARKER.encode("utf-8") in content:
            return response

        script = (
            "<script id=\"tab-session-bridge\">"
            "(function(){"
            "var P='_tsid';var K='safetrack_tab_session_id';"
            "var id=sessionStorage.getItem(K);"
            "if(!id){id=(window.crypto&&window.crypto.randomUUID)?window.crypto.randomUUID():'ts'+Date.now().toString(36)+Math.random().toString(36).slice(2);sessionStorage.setItem(K,id);}"
            "function addParam(url){"
            "if(!url||url.charAt(0)==='#'||url.indexOf('javascript:')===0||url.indexOf('mailto:')===0||url.indexOf('tel:')===0){return url;}"
            "var u;try{u=new URL(url,window.location.href);}catch(e){return url;}"
            "if(u.origin!==window.location.origin){return url;}"
            "if(!u.searchParams.get(P)){u.searchParams.set(P,id);}"
            "if(url.indexOf('http://')===0||url.indexOf('https://')===0){return u.toString();}"
            "if(url.charAt(0)==='?'){return u.search+u.hash;}"
            "return u.pathname+u.search+u.hash;"
            "}"
            "function patchLink(a){var h=a.getAttribute('href');if(!h){return;}var n=addParam(h);if(n&&n!==h){a.setAttribute('href',n);}}"
            "function patchForm(f){"
            "var action=f.getAttribute('action')||window.location.href;"
            "var next=addParam(action);if(next){f.setAttribute('action',next);}"
            "var i=f.querySelector('input[name=\"_tsid\"]');"
            "if(!i){i=document.createElement('input');i.type='hidden';i.name='_tsid';f.appendChild(i);}i.value=id;"
            "}"
            "function patchAll(){"
            "document.querySelectorAll('a[href]').forEach(patchLink);"
            "document.querySelectorAll('form').forEach(patchForm);"
            "}"
            "var cur=new URL(window.location.href);"
            "if(!cur.searchParams.get(P)){cur.searchParams.set(P,id);history.replaceState(null,'',cur.pathname+cur.search+cur.hash);}"
            "if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',patchAll);}else{patchAll();}"
            "document.addEventListener('click',function(e){var a=e.target.closest('a[href]');if(a){patchLink(a);}},true);"
            "document.addEventListener('submit',function(e){if(e.target&&e.target.tagName==='FORM'){patchForm(e.target);}},true);"
            "})();"
            "</script>"
        ).encode("utf-8")

        if b"</body>" in content.lower():
            response.content = re.sub(
                b"</body>", script + b"</body>", content, count=1, flags=re.IGNORECASE
            )
        else:
            response.content = content + script

        return response
