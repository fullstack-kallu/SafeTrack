"""SafeTrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from Track.views import *
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = [
	path('admin/', admin.site.urls),
	 path('login/',TemplateView.as_view(template_name = 'common/login.html')),
	path('home/',TemplateView.as_view(template_name = 'common/index.html')),
	path('aboutus/',TemplateView.as_view(template_name = 'common/aboutus.html')),
	path('contactus/',TemplateView.as_view(template_name = 'common/contactus.html')),
	path('regadmin/',TemplateView.as_view(template_name = 'common/reg_admin.html')),
	path('reginsert/',reginsert, name = 'reginsert'),
	path('approve/',approve, name = 'approve'),
	 path('worker_salary/', worker_salary, name='worker_salary'),
	path('reject/',reject, name = 'reject'),
	path('emp/',TemplateView.as_view(template_name = 'common/reg_emp.html')),
	path('regempinsert/',regempinsert, name = 'regempinsert'),
	path('police/',TemplateView.as_view(template_name = 'common/reg_policestation.html')),
	path('regpoliceinsert/',regpoliceinsert, name = 'regpoliceinsert'),
	path('registration/',TemplateView.as_view(template_name = 'common/reg_worker.html')),
	path('reg_worker/',TemplateView.as_view(template_name = 'common/reg_worker.html')),
	path('regworkerinsert/',regworkerinsert, name = 'regworkerinsert'),
	path('index/',index, name = 'index'),
	path('login/',login, name = 'login'),
	#url('registration/',TemplateView.as_view(template_name = 'vacancy.html')),
	#url('vacancyinsert/',vacancyinsert, name = 'vacancyinsert'),

	path('searchlogin/',searchlogin, name = 'searchlogin'),
	path('',TemplateView.as_view(template_name = 'common/index.html')),
	path('viewacceptemprequest/',viewacceptemprequest, name = 'viewacceptemprequest'),
	path('viewemprequest/',viewemprequest, name = 'viewemprequest'),
	path('acceptemprequest/',acceptemprequest, name = 'acceptemprequest'),
	path('rejectemprequest/',rejectemprequest, name = 'rejectemprequest'),
	path('viewworkeraccept/',viewworkeraccept, name = 'viewworkeraccept'),
	path('viewnocaccept/',viewnocaccept, name = 'viewnocaccept'),
	path('viewacceptworkerrequest/',viewacceptworkerrequest, name = 'viewacceptworkerrequest'),
	path('rejectworkerrequest/',rejectworkerrequest, name = 'rejectworkerrequest'),
	path('acceptworkerrequest/',acceptworkerrequest, name = 'acceptworkerrequest'),
	path('vieweditemp/',vieweditemp, name = 'vieweditemp'),
	path('edit_employer/',edit_employer, name = 'edit_employer'),
	path('update_employer/',update_employer, name = 'update_employer'),
	path('addvacancy/',TemplateView.as_view(template_name = 'agency/vacancy.html')),
	path('vacancyinsert/',vacancyinsert, name = 'vacancyinsert'),

	path('noc_insert1/',noc_insert1, name = 'noc_insert1'),
	path('noc_insert/',noc_insert, name = 'noc_insert'),
	path('addnoc/',addnoc, name = 'addnoc'),
	path('viewvacancydetails/',viewvacancydetails, name = 'viewvacancydetails'),
	path('insertworkerdetails/',insertworkerdetails, name = 'insertworkerdetails'),
	path('insertworkerdetails/',insertworkerdetails, name = 'insertworkerdetails'),
	path('viewworkerdetails/',viewworkerdetails, name = 'viewworkerdetails'),
	path('viewworker/',viewworker, name = 'viewworker'),
	#url('viewworkerdetails1/',TemplateView.as_view(template_name = 'view_shedduled_workerdetails.html')),
	
	path('feedbackinsert/',feedbackinsert, name = 'feedbackinsert'),
	path('addfeedback/',addfeedback, name = 'addfeedback'),
	path('homeworker/',TemplateView.as_view(template_name = 'worker/home_worker.html')),
	path('homeadmin/',TemplateView.as_view(template_name = 'admin/home_admin.html')),
	path('homeemp/',TemplateView.as_view(template_name = 'agency/home_emp.html')),
	path('homepolice/',TemplateView.as_view(template_name = 'police/home_police.html')),
	path('viewemydetails/',viewemydetails, name = 'viewemydetails'),
	path('viewempworker/',viewempworker, name = 'viewempworker'),
	path('viewnoc1/',viewnoc1, name = 'viewnoc1'),
	path('viewnoc2/',viewnoc2, name = 'viewnoc2'),
	path('view_feedbackworker/',view_feedbackworker, name = 'view_feedbackworker'),
	path('addvacancy/',TemplateView.as_view(template_name = 'agency/vacancy.html')),
	path('vacancyinsert/',vacancyinsert, name = 'vacancyinsert'),
	path('viewvacancy/',viewvacancy, name = 'viewvacancy'),
	
	path('editvacancy1/',editvacancy1, name = 'editvacancy1'),
	path('editvacancy2/',editvacancy2, name = 'editvacancy2'),
	path('editvacancy3/',editvacancy3, name = 'editvacancy3'),
	path('viewvacancyhome/',viewvacancyhome, name = 'viewvacancyhome'),
	path('viewvacancyhome2/',viewvacancyhome2, name = 'viewvacancyhome2'),
	path('viewvacancyhome3/',viewvacancyhome3, name = 'viewvacancyhome3'),
	
	path('viewvacancyhome4/',viewvacancyhome4, name = 'viewvacancyhome4'),
	path('viewappliedvacancy/',viewappliedvacancy, name = 'viewappliedvacancy'),
	path('viewappliedvacancy2/',viewappliedvacancy2, name = 'viewappliedvacancy2'),
	path('addmyworker/',addmyworker, name = 'addmyworker'),
	path('editfeedbackworker1/',editfeedbackworker1, name = 'editfeedbackworker1'),
	path('editfeedbackworker2/',editfeedbackworker2, name = 'editfeedbackworker2'),
	path('editfeedbackworker3/',editfeedbackworker3, name = 'editfeedbackworker3'),
	path('viewemydetailsworker/',viewemydetailsworker, name = 'viewemydetailsworker'),
	path('worker_profile/',worker_profile, name = 'worker_profile'),
	path('viewmyworker/',viewmyworker, name = 'viewmyworker'),
	path('viewfeedback/',viewfeedback, name = 'viewfeedback'),
	path('viewadmin/',viewadmin, name = 'viewadmin'),
	path('editadmin1/',editadmin1, name = 'editadmin1'),
	path('editadmin2/',editadmin2, name = 'editadmin2'),
	path('editadmin3/',editadmin3, name = 'editadmin3'),
	path('viewadminworker/',viewadminworker, name = 'viewadminworker'),
	path('editadminworker/',editadminworker, name = 'editadminworker'),
	path('editadminworker2/',editadminworker2, name = 'editadminworker2'),
	path('editadminworker3/',editadminworker3, name = 'editadminworker3'),
	path('viewfeedbackworkerhome/',viewfeedbackworkerhome, name = 'viewfeedbackworkerhome'),
	path('viewmyworker_jobsheddule/',viewmyworker_jobsheddule, name = 'viewmyworker_jobsheddule'),
	path('jobsheddule1/',jobsheddule1, name = 'jobsheddule1'),
	path('jobsheddule2/',jobsheddule2, name = 'jobsheddule2'),
	path('passwordchanging/',TemplateView.as_view(template_name = 'changepaswd.html')),
	path('changepassword/',changepassword, name = 'changepassword'),
	path('viewempadmin/',viewempadmin, name = 'viewempadmin'),
	
	# Admin Employer Approval URLs
	path('admin_view_pending_employers/',admin_view_pending_employers, name = 'admin_view_pending_employers'),
	path('admin_view_employer_detail/',admin_view_employer_detail, name = 'admin_view_employer_detail'),
	path('admin_approve_employer/',admin_approve_employer, name = 'admin_approve_employer'),
	path('admin_reject_employer/',admin_reject_employer, name = 'admin_reject_employer'),
	
	# Admin View All Employers URLs
	path('admin_view_all_employers/',admin_view_all_employers, name = 'admin_view_all_employers'),
	path('admin_view_single_employer/',admin_view_single_employer, name = 'admin_view_single_employer'),
	path('viewpolice/',viewpolice, name = 'viewpolice'),
	path('viewadminpolice/',viewadminpolice, name = 'viewadminpolice'),
	path('editpolice1/',editpolice1, name = 'editpolice1'),
	path('editpolice2/',editpolice2, name = 'editpolice2'),
	path('editpolice3/',editpolice3, name = 'editpolice3'),
	path('deletenoc1/',deletenoc1, name = 'deletenoc1'),
	path('deletenoc2/',deletenoc2, name = 'deletenoc2'),
	path('deletenoc3/',deletenoc3, name = 'deletenoc3'),
	
	path('deletevacancy1/',deletevacancy1, name = 'deletevacancy1'),
	path('deletevacancy2/',deletevacancy2, name = 'deletevacancy2'),
	path('deletefeedback1/',deletefeedback1, name = 'deletefeedback1'),
	path('deletefeedback2/',deletefeedback2, name = 'deletefeedback2'),
	path('view_feedbackemp/',view_feedbackemp, name = 'view_feedbackemp'),
	path('feedbackinsertworker/',feedbackinsertworker, name = 'feedbackinsertworker'),
	path('addfeedbackworker/',addfeedbackworker, name = 'addfeedbackworker'),
	path('viewfeedbackemp/',viewfeedbackemp, name = 'viewfeedbackemp'),
	path('perdayjob/',perdayjob, name = 'perdayjob'),
	path('viewnoc/',viewnoc, name = 'viewnoc'),
	path('addcomplaint/',addcomplaint, name = 'addcomplaint'),
	path('complaint2/',complaint2, name = 'complaint2'),
	path('addcomplaint3/',addcomplaint3, name = 'addcomplaint3'),
	path('editnoc1/',editnoc1, name = 'editnoc1'),
	path('editnoc2/',editnoc2, name = 'editnoc2'),
	path('editnoc3/',editnoc3, name = 'editnoc3'),
	path('editnoc4/',editnoc4, name = 'editnoc4'),
	path('viewpoliceworker/',viewpoliceworker, name = 'viewpoliceworker'),
	path('viewfeedbackworker1/',viewfeedbackworker1, name = 'viewfeedbackworker1'),
	path('viewfeedbackworker2/',viewfeedbackworker2, name = 'viewfeedbackworker2'),
	path('viewfeedbackworker3/',viewfeedbackworker3, name = 'viewfeedbackworker43'),
	path('viewworkercomplaint/',viewworkercomplaint, name = 'viewworkercomplaint'),
	#url('viewworkercomplaint1/',viewworkercomplaint1, name = 'viewworkercomplaint1'),
	
	path('insurencejoin1/',insurencejoin1,name='insurencejoin1'),
	path('insurencejoin2/',insurencejoin2, name = 'insurencejoin2'),
	path('view_workershedduledetails1/',view_workershedduledetails1,name='view_workershedduledetails1'),
	path('workersheddule2/',workersheddule2,name='workersheddule2'),
	path('view1/',view1,name='view1'),
	path('idcard/',idcard,name='idcard'),
	path('viewjobshedule/',viewjobshedule,name='viewjobshedule'),
	path('viewjobshedule2/',viewjobshedule2,name='viewjobshedule2'),
	path('deletejobshedule1/',deletejobshedule1,name='deletejobshedule1'),
	path('deletejobshedule2/',deletejobshedule2,name='deletejobshedule2'),
	path('deletejobshedule3/',deletejobshedule3,name='deletejobshedule3'),
	path('searchvaccancy/',searchvaccancy, name = 'searchvaccancy'),
	path('view2/',view2, name = 'view2'),
	path('vacancy_search/',vacancy_search, name = 'vacancy_search'),
	path('policehome/',TemplateView.as_view(template_name = 'police/home_police.html')),
	path('workerhome/',TemplateView.as_view(template_name = 'worker/home_worker.html')),
	path('emphome/',TemplateView.as_view(template_name = 'agency/home_emp.html')),
	path('password/',TemplateView.as_view(template_name = 'changepaswd.html')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += staticfiles_urlpatterns()
