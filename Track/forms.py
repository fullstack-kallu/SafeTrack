from django import forms
from django.contrib.auth.hashers import make_password
from Track.models import (
    tbl_admin, tbl_login, tbl_emp, tbl_worker, tbl_vacancy, 
    tbl_jobdetails, tbl_workerdetails, tbl_workershedule, 
    tbl_noc, tbl_noccomplaint, tbl_policestation, 
    tbl_feedback, tbl_complaint, tbl_myworker, tbl_insurence
)

# ==================== ADMIN FORMS ====================

class AdminForm(forms.ModelForm):
    pasw = forms.CharField(widget=forms.PasswordInput, label="Password")
    
    class Meta:
        model = tbl_admin
        fields = ['name', 'country', 'state', 'phone', 'mobile', 'email', 'pasw']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'pasw': forms.PasswordInput(attrs={'class': 'form-control', 'required': True}),
        }

# ==================== LOGIN FORMS ====================

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    user_type = forms.ChoiceField(
        choices=[('admin', 'Admin'), ('emp', 'Agency'), ('worker', 'Worker'), ('police', 'Police')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class TblLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    
    class Meta:
        model = tbl_login
        fields = ['username', 'password', 'user_type', 'u_id', 'status']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': True}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'u_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ==================== EMPLOYEE/AGENCY FORMS ====================

class EmpForm(forms.ModelForm):
    pswd = forms.CharField(widget=forms.PasswordInput, label="Password")
    
    class Meta:
        model = tbl_emp
        fields = ['name', 'gender', 'firm_name', 'aadhar_no', 'dob', 'emp_address', 
                  'place', 'phone', 'mobile', 'email', 'pswd', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')]),
            'firm_name': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhar_no': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'emp_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'pswd': forms.PasswordInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ==================== WORKER FORMS ====================

class WorkerForm(forms.ModelForm):
    paswd = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = tbl_worker
        fields = [
            'worker_name', 'gender', 'dob', 'age', 'aadhar_number',
            'place', 'address', 'languages_known',
            'phone', 'mobile', 'email', 'paswd', 'image'
        ]
        widgets = {
            'worker_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(
                attrs={'class': 'form-control'},
                choices=[('Male', 'Male'), ('Female', 'Female')]
            ),
            'dob': forms.TextInput(attrs={'class': 'form-control'}),  # 🔥 FIXED
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'aadhar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'languages_known': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'paswd': forms.PasswordInput(attrs={'class': 'form-control'}),
            'image': forms.TextInput(attrs={'class': 'form-control'})  # 🔥 FIXED
        }


class WorkerDetailsForm(forms.ModelForm):
    class Meta:
        model = tbl_workerdetails
        fields = ['worker_id', 'vacancy_id', 'qualification', 'experience']
        widgets = {
            'worker_id': forms.TextInput(attrs={'class': 'form-control'}),
            'vacancy_id': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# ==================== VACANCY FORMS ====================

class VacancyForm(forms.ModelForm):
    class Meta:
        model = tbl_vacancy
        fields = ['emp_id', 'date', 'vacancy', 'vacancy_no', 'description']
        widgets = {
            'emp_id': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'vacancy': forms.TextInput(attrs={'class': 'form-control'}),
            'vacancy_no': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# ==================== JOB DETAILS FORMS ====================

class JobDetailsForm(forms.ModelForm):
    class Meta:
        model = tbl_jobdetails
        fields = ['emp_id', 'job_details']
        widgets = {
            'emp_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'job_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# ==================== SCHEDULE FORMS ====================

class WorkerScheduleForm(forms.ModelForm):
    class Meta:
        model = tbl_workershedule
        fields = ['emp_id', 'worker_id', 'job_details', 'salary', 'time_from', 'working_houres']
        widgets = {
            'emp_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'worker_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'job_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'time_from': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'working_houres': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ==================== MY WORKER FORMS ====================

class MyWorkerForm(forms.ModelForm):
    class Meta:
        model = tbl_myworker
        fields = ['emp_id', 'worker_id', 'vacancy_id', 'date', 'status']
        widgets = {
            'emp_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'worker_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'vacancy_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ==================== POLICE FORMS ====================

class PoliceStationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = tbl_policestation
        fields = ['branch', 'address', 'phone', 'mobile', 'email', 'district', 
                  'city', 'state', 'password']
        widgets = {
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class NocForm(forms.ModelForm):
    class Meta:
        model = tbl_noc
        fields = ['worker_id', 'station_id', 'date', 'crime', 'crime_details']
        widgets = {
            'worker_id': forms.TextInput(attrs={'class': 'form-control'}),
            'station_id': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'crime': forms.TextInput(attrs={'class': 'form-control'}),
            'crime_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class NocComplaintForm(forms.ModelForm):
    class Meta:
        model = tbl_noccomplaint
        fields = ['worker_id', 'noc_id', 'complaint', 'complaint_date']
        widgets = {
            'worker_id': forms.TextInput(attrs={'class': 'form-control'}),
            'noc_id': forms.TextInput(attrs={'class': 'form-control'}),
            'complaint': forms.TextInput(attrs={'class': 'form-control'}),
            'complaint_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# ==================== FEEDBACK FORMS ====================

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = tbl_feedback
        fields = ['emp_id', 'worker_id', 'date', 'feedback_title', 'feedback_description']
        widgets = {
            'emp_id': forms.TextInput(attrs={'class': 'form-control'}),
            'worker_id': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'feedback_title': forms.TextInput(attrs={'class': 'form-control'}),
            'feedback_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# ==================== COMPLAINT FORMS ====================

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = tbl_complaint
        fields = ['emp_id', 'complaint', 'cmp_date']
        widgets = {
            'emp_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'complaint': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cmp_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# ==================== INSURANCE FORMS ====================

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = tbl_insurence
        fields = ['worker_id', 'emp_id', 'myworker_id', 'date', 'insurence_type', 
                  'insurence_period', 'insurence_rupee', 'currently_insured', 
                  'details', 'nominee_name']
        widgets = {
            'worker_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'emp_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'myworker_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'insurence_type': forms.TextInput(attrs={'class': 'form-control'}),
            'insurence_period': forms.TextInput(attrs={'class': 'form-control'}),
            'insurence_rupee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currently_insured': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'nominee_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ==================== BACKWARD COMPATIBILITY ALIASES ====================
# Maintain compatibility with existing code
workerform = WorkerForm
