from django.contrib import admin
from Track.models import (
    tbl_admin, tbl_login, tbl_emp, tbl_complaint, tbl_feedback,
    tbl_jobdetails, tbl_myworker, tbl_noc, tbl_noccomplaint,
    tbl_policestation, tbl_vacancy, tbl_worker, tbl_workerdetails,
    tbl_workershedule, tbl_insurence
)

# Register all custom models
admin.site.register(tbl_admin)
admin.site.register(tbl_login)
admin.site.register(tbl_emp)
admin.site.register(tbl_complaint)
admin.site.register(tbl_feedback)
admin.site.register(tbl_jobdetails)
admin.site.register(tbl_myworker)
admin.site.register(tbl_noc)
admin.site.register(tbl_noccomplaint)
admin.site.register(tbl_policestation)
admin.site.register(tbl_vacancy)
admin.site.register(tbl_worker)
admin.site.register(tbl_workerdetails)
admin.site.register(tbl_workershedule)
admin.site.register(tbl_insurence)
