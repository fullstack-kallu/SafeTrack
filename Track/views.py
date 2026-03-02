from django.shortcuts import render,HttpResponseRedirect,redirect
from django.shortcuts import render
from django.db import connection 
from django.http import HttpResponse 
from django.template import Context 
from django.template.loader import get_template 
from django.template import Template, Context
from django.db import models
from django.contrib import messages
from django.contrib import messages
from Track.forms import (
    workerform, WorkerForm, LoginForm, EmpForm, PoliceStationForm,
    VacancyForm, FeedbackForm, ComplaintForm, AdminForm
)
from django.db.models import Q
from Track.models import (
    tbl_worker, tbl_login, tbl_admin, tbl_emp, 
    tbl_policestation, tbl_vacancy, tbl_myworker, tbl_noc,
    tbl_workerdetails, tbl_feedback, tbl_workershedule, tbl_noccomplaint
)
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import date
from django.db import IntegrityError
import datetime
import os
now=str(date.today())


def send_salary_notification_email(worker_email, worker_name, salary_amount, month_year):
    """
    Send salary notification email to worker using EmailMultiAlternatives with HTML format.
    
    Args:
        worker_email: Worker's email address
        worker_name: Worker's name
        salary_amount: Salary amount
        month_year: Month and year string (e.g., 'January 2026')
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = 'Salary Payment Confirmation - SafeMigrate'
        
        # Plain text version
        text_content = f"""
Dear {worker_name},

Your salary has been successfully processed and confirmed.

Details:
- Salary Amount: Rs. {salary_amount}
- Month/Year: {month_year}

This is a professional confirmation that your salary payment has been processed. 
If you have any questions, please contact your employer.

Best regards,
SafeMigrate Team
        """
        
        # HTML version
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .details {{ margin: 20px 0; padding: 15px; background-color: white; border-left: 4px solid #4CAF50; }}
        .detail-row {{ margin: 10px 0; }}
        .label {{ font-weight: bold; color: #555; }}
        .value {{ color: #333; }}
        .footer {{ text-align: center; padding: 20px; color: #777; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Salary Payment Confirmation</h1>
        </div>
        <div class="content">
            <p>Dear <strong>{worker_name}</strong>,</p>
            <p>Your salary has been successfully processed and confirmed. Please find the details below:</p>
            
            <div class="details">
                <div class="detail-row">
                    <span class="label">Worker Name:</span>
                    <span class="value">{worker_name}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Salary Amount:</span>
                    <span class="value">Rs. {salary_amount}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Month/Year:</span>
                    <span class="value">{month_year}</span>
                </div>
            </div>
            
            <p>This is a professional confirmation that your salary payment has been processed. 
            If you have any questions or concerns, please contact your employer.</p>
            
            <p>Thank you for your hard work!</p>
            
            <p>Best regards,<br>
            <strong>SafeMigrate Team</strong></p>
        </div>
        <div class="footer">
            <p>This is an automated email. Please do not reply to this message.</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Create email with both plain text and HTML versions
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[worker_email]
        )
        
        # Attach HTML content
        email.attach_alternative(html_content, 'text/html')
        
        # Send the email
        email.send(fail_silently=False)
        
        print(f"Salary notification email sent successfully to {worker_email}")
        return True
        
    except Exception as e:
        print(f"Error sending salary notification email: {str(e)}")
        return False

def searchlogin(request):
	"""Authenticate user using custom tbl_login table"""
	try:
		username = request.GET.get('username', '').strip()
		password = request.GET.get('password', '').strip()
		
		if not username or not password:
			html = "<script>alert('Please provide username and password');window.location='/login/';</script>"
			return HttpResponse(html)
		
		# Use ORM instead of raw SQL - safer and cleaner
		login_user = tbl_login.objects.filter(
			username=username,
			password=password,
			status='true'
		).first()
		
		if login_user:
			request.session['username'] = username
			request.session['u_id'] = login_user.u_id
			request.session['user_type'] = login_user.user_type
			
			user_type = login_user.user_type
			if user_type == 'admin':
				return redirect('/homeadmin/')
			elif user_type == 'employer':
				return redirect('/homeemp/')
			elif user_type == 'police':
				return redirect('/homepolice/')
			elif user_type == 'worker':
				return redirect('/homeworker/')
			else:
				html = "<script>alert('Invalid user type');window.location='/login/';</script>"
				return HttpResponse(html)
		else:
			html = "<script>alert('Invalid username or password');window.location='/login/';</script>"
			return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Login error: {str(e)}');window.location='/login/';</script>"
		return HttpResponse(html)

def homeemp(request):
	if 'u_id' not in request.session or request.session.get('user_type') != 'employer':
		return HttpResponse("<script>alert('Please login as Agency first');window.location='/login/';</script>")
	return render(request, 'agency/home_emp.html')

def homeworker(request):
	if 'u_id' not in request.session or request.session.get('user_type') != 'worker':
		return HttpResponse("<script>alert('Please login as Worker first');window.location='/login/';</script>")
	return render(request, 'worker/home_worker.html')

def _ensure_police_session(request):
	"""Recover police session when u_id exists but user_type key is missing/stale."""
	u_id = request.session.get('u_id')
	if not u_id:
		username = request.session.get('username')
		if username:
			login_row = tbl_login.objects.filter(username=username, user_type='police', status='true').first()
			if login_row:
				request.session['u_id'] = login_row.u_id
				request.session['user_type'] = 'police'
				return True
		return False
	if request.session.get('user_type') == 'police':
		return True
	login_row = tbl_login.objects.filter(u_id=u_id, user_type='police', status='true').first()
	if login_row:
		request.session['user_type'] = 'police'
		return True
	return False

def _get_logged_police_station(request):
	"""Return police station object for the logged-in police session."""
	if not _ensure_police_session(request):
		return None

	station = tbl_policestation.objects.filter(station_id=request.session.get('u_id')).first()
	if station:
		return station

	# Fallback by username->email mapping for legacy/misaligned rows.
	username = request.session.get('username')
	if username:
		station = tbl_policestation.objects.filter(email=username).first()
		if station:
			request.session['u_id'] = station.station_id
			request.session['user_type'] = 'police'
			return station
	return None

def _get_workers_for_police_noc():
	"""Common worker source for police NOC listing pages.

	Use tbl_worker directly so legacy workers (missing/old login mappings)
	are still visible in police NOC pages.
	"""
	return tbl_worker.objects.all().order_by('-worker_id')

def homepolice(request):
	if not _ensure_police_session(request):
		return HttpResponse("<script>alert('Please login as Police Station first');window.location='/login/';</script>")
	return render(request, 'police/home_police.html')

def homeadmin(request):
	"""Admin view: Dashboard with analytics using ORM"""
	try:
		# Keep this page accessible for legacy admin flows that may not set u_id,
		# but still block clearly non-admin logged-in users.
		session_user_type = request.session.get('user_type')
		if session_user_type and session_user_type != 'admin':
			return redirect('/login/')
			
		worker_count = tbl_worker.objects.count()
		agency_count = tbl_emp.objects.filter(status='true').count()
		pending_agencies = tbl_login.objects.filter(user_type='employer', status='false').count()
		police_count = tbl_policestation.objects.count()
		
		# Get recent registrations (simulated for now with order_by ID)
		recent_workers = tbl_worker.objects.all().order_by('-worker_id')[:5]
		
		context = {
			'worker_count': worker_count,
			'agency_count': agency_count,
			'pending_agencies': pending_agencies,
			'police_count': police_count,
			'recent_workers': recent_workers,
		}
		return render(request, 'admin/home_admin.html', context)
	except Exception as e:
		return render(request, 'admin/home_admin.html', {'error': str(e)})
def logout(request):
	try:
		del request.session['u_id']
		del request.session['user_type']
	except:
		pass
	return HttpResponse("<script>alert('you are loged out');window.location='/login/';</script>")

def reginsert(request):
	"""Register admin using custom tables (no Django User model)"""
	try:
		name = request.GET.get('admin_name', '').strip()
		country = request.GET.get('country', '').strip()
		state = request.GET.get('state', '').strip()
		phone = request.GET.get('Phone', '').strip()
		mobile = request.GET.get('Mobile', '').strip()
		email_id = request.GET.get('Email_id', '').strip()
		password = request.GET.get('Password', '').strip()
		
		if not all([name, email_id, password]):
			html = "<script>alert('Required fields missing');window.location='/registration/';</script>"
			return HttpResponse(html)
		
		# Check if email already registered
		if tbl_login.objects.filter(username=email_id).exists():
			html = "<script>alert('Email already registered');window.location='/registration/';</script>"
			return HttpResponse(html)
		
		# Create admin record
		admin = tbl_admin.objects.create(
			name=name,
			country=country,
			state=state,
			phone=phone,
			mobile=mobile,
			email=email_id,
			pasw=password
		)
		
		# Create login record
		tbl_login.objects.create(
			username=email_id,
			password=password,
			user_type='admin',
			u_id=admin.admin_id,
			status='true'
		)
		
		html = "<script>alert('Successfully registered as admin!');window.location='/login/';</script>"
		return HttpResponse(html)
	except IntegrityError:
		html = "<script>alert('Registration failed: Duplicate entry');window.location='/registration/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Registration error: {str(e)}');window.location='/registration/';</script>"
		return HttpResponse(html)
	
def regempinsert(request):
	"""Register employee/agency using ORM with inline error handling"""
	try:
		# Check if it's a POST request
		if request.method == 'POST':
			name = request.POST.get('Emp_name', '').strip()
			gender = request.POST.get('Gender', '').strip()
			firm_name = request.POST.get('Firm_name', '').strip()
			aadhar_no = request.POST.get('Aadhar_number', '').strip()
			dob = request.POST.get('DOB', '').strip()
			address = request.POST.get('Emp_address', '').strip()
			place = request.POST.get('Place', '').strip()
			phone = request.POST.get('Phone', '').strip()
			mobile = request.POST.get('Mobile', '').strip()
			email_id = request.POST.get('Email_id', '').strip()
			password = request.POST.get('Password', '').strip()
			re_password = request.POST.get('re_Password', '').strip()
		else:
			# Fallback to GET for backward compatibility
			name = request.GET.get('Emp_name', '').strip()
			gender = request.GET.get('Gender', '').strip()
			firm_name = request.GET.get('Firm_name', '').strip()
			aadhar_no = request.GET.get('Aadhar_number', '').strip()
			dob = request.GET.get('DOB', '').strip()
			address = request.GET.get('Emp_address', '').strip()
			place = request.GET.get('Place', '').strip()
			phone = request.GET.get('Phone', '').strip()
			mobile = request.GET.get('Mobile', '').strip()
			email_id = request.GET.get('Email_id', '').strip()
			password = request.GET.get('Password', '').strip()
			re_password = request.GET.get('re_Password', '').strip()
		
		# Initialize error dictionary
		errors = {}
		
		# Validate required fields
		if not name:
			errors['name'] = 'Full Name is required'
		if not email_id:
			errors['email'] = 'Email Address is required'
		if not password:
			errors['password'] = 'Password is required'
		if not re_password:
			errors['re_password'] = 'Please confirm your password'
		
		# Check password match
		if password and re_password and password != re_password:
			errors['re_password'] = 'Passwords do not match'
		
		# Check if email already registered in tbl_login
		if email_id and tbl_login.objects.filter(username=email_id).exists():
			errors['email'] = 'This email is already registered'
		
		# Check if mobile already registered in tbl_emp
		if mobile and tbl_emp.objects.filter(mobile=mobile).exists():
			errors['mobile'] = 'This phone number is already registered'
		
		# Check if aadhar already registered in tbl_emp
		if aadhar_no and tbl_emp.objects.filter(aadhar_no=aadhar_no).exists():
			errors['aadhar'] = 'This Aadhar number is already registered'
		
		# If there are validation errors, render the form with error messages
		if errors:
			context = {
				'errors': errors,
				'form_data': {
					'Emp_name': name,
					'Gender': gender,
					'Firm_name': firm_name,
					'Aadhar_number': aadhar_no,
					'DOB': dob,
					'Emp_address': address,
					'Place': place,
					'Phone': phone,
					'Mobile': mobile,
					'Email_id': email_id,
				}
			}
			return render(request, 'common/reg_emp.html', context)
		
		# Create employee record
		emp = tbl_emp.objects.create(
			name=name,
			gender=gender,
			firm_name=firm_name,
			aadhar_no=aadhar_no,
			dob=dob,
			emp_address=address,
			place=place,
			phone=phone,
			mobile=mobile,
			email=email_id,
			pswd=password,
			status='pending'
		)
		
		# Create login record
		tbl_login.objects.create(
			username=email_id,
			password=password,
			user_type='employer',
			u_id=emp.emp_id,
			status='false'
		)
		
		html = "<script>alert('Successfully registered! Awaiting admin approval.');window.location='/login/';</script>"
		return HttpResponse(html)
	except IntegrityError as ie:
		html = f"<script>alert('Registration failed: Duplicate entry');window.location='/reg_emp/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Registration error: {str(e)}');window.location='/reg_emp/';</script>"
		return HttpResponse(html)
def regpoliceinsert(request):
	"""Register police station using ORM with inline error handling"""
	try:
		# Support both GET and POST
		if request.method == 'POST':
			branch = request.POST.get('branch', '').strip()
			address = request.POST.get('address', '').strip()
			phone = request.POST.get('Phone', '').strip()
			mobile = request.POST.get('Mobile', '').strip()
			email_id = request.POST.get('Email_id', '').strip()
			district = request.POST.get('district', '').strip()
			city = request.POST.get('city', '').strip()
			state = request.POST.get('state', '').strip()
			password = request.POST.get('Password', '').strip()
			re_password = request.POST.get('re_Password', '').strip()
		else:
			branch = request.GET.get('branch', '').strip()
			address = request.GET.get('address', '').strip()
			phone = request.GET.get('Phone', '').strip()
			mobile = request.GET.get('Mobile', '').strip()
			email_id = request.GET.get('Email_id', '').strip()
			district = request.GET.get('district', '').strip()
			city = request.GET.get('city', '').strip()
			state = request.GET.get('state', '').strip()
			password = request.GET.get('Password', '').strip()
			re_password = request.GET.get('re_Password', '').strip()
		
		# Initialize error dictionary
		errors = {}
		
		# Validate required fields
		if not branch:
			errors['branch'] = 'Station Branch Name is required'
		if not address:
			errors['address'] = 'Address is required'
		if not email_id:
			errors['email'] = 'Email Address is required'
		if not city:
			errors['city'] = 'City is required'
		if not district:
			errors['district'] = 'District is required'
		if not state:
			errors['state'] = 'State is required'
		if not password:
			errors['password'] = 'Password is required'
		if not re_password:
			errors['re_password'] = 'Please confirm your password'
		
		# Check password match
		if password and re_password and password != re_password:
			errors['re_password'] = 'Passwords do not match'
		
		# Check if email already registered in tbl_login
		if email_id and tbl_login.objects.filter(username=email_id).exists():
			errors['email'] = 'This email is already registered'
		
		# Check if mobile already registered in tbl_policestation
		if mobile and tbl_policestation.objects.filter(mobile=mobile).exists():
			errors['mobile'] = 'This phone number is already registered'
		
		# If there are validation errors, render the form with error messages
		if errors:
			context = {
				'errors': errors,
				'form_data': {
					'branch': branch,
					'address': address,
					'Phone': phone,
					'Mobile': mobile,
					'Email_id': email_id,
					'district': district,
					'city': city,
					'state': state,
				}
			}
			return render(request, 'common/reg_policestation.html', context)
		
		# Create police station record
		police = tbl_policestation.objects.create(
			branch=branch,
			address=address,
			phone=phone,
			mobile=mobile,
			email=email_id,
			district=district,
			city=city,
			state=state,
			password=password
		)
		
		# Create login record
		tbl_login.objects.create(
			username=email_id,
			password=password,
			user_type='police',
			u_id=police.station_id,
			status='true'
		)
		
		html = "<script>alert('Successfully registered as police station!');window.location='/login/';</script>"
		return HttpResponse(html)
	except IntegrityError:
		html = "<script>alert('Registration failed: Duplicate entry');window.location='/reg_police/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Registration error: {str(e)}');window.location='/reg_police/';</script>"
		return HttpResponse(html)
def regworkerinsert(request):
    """Register worker using ORM with inline error handling"""
    if request.method == "POST":
        form = WorkerForm(request.POST, request.FILES)

        # Initialize error dictionary
        errors = {}
        
        # Get form data for duplicate checks
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        aadhar_number = request.POST.get('aadhar_number', '').strip()
        
        # Check if email already registered in tbl_login
        if email and tbl_login.objects.filter(username=email).exists():
            errors['email'] = 'This email is already registered'
        
        # Check if mobile already registered in tbl_worker
        if mobile and tbl_worker.objects.filter(mobile=mobile).exists():
            errors['mobile'] = 'This phone number is already registered'
        
        # Check if aadhar already registered in tbl_worker
        if aadhar_number and tbl_worker.objects.filter(aadhar_number=aadhar_number).exists():
            errors['aadhar'] = 'This Aadhar number is already registered'

        # Stop submission early for duplicate checks and render inline messages
        if errors:
            context = {
                'form': form,
                'errors': errors,
                'form_data': {
                    'email': email,
                    'mobile': mobile,
                    'aadhar_number': aadhar_number,
                }
            }
            return render(request, 'common/reg_worker.html', context)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['paswd']

            # Check email already exists (additional check after form validation)
            if tbl_login.objects.filter(username=email).exists():
                # Render form with error
                errors['email'] = 'This email is already registered'
                context = {
                    'form': form,
                    'errors': errors,
                    'form_data': {
                        'email': email,
                        'mobile': mobile,
                        'aadhar_number': aadhar_number,
                    }
                }
                return render(request, 'common/reg_worker.html', context)

            try:
                # Save worker
                worker = form.save(commit=False)
                worker.regis_date = str(date.today())
                worker.status = 'Pending'
                worker.save()

                # Create login
                tbl_login.objects.create(
                    username=email,
                    password=password,
                    user_type='worker',
                    u_id=worker.worker_id,
                    status='false'
                )

                return HttpResponse(
                    "<script>alert('Successfully registered as worker!');window.location='/login/';</script>"
                )
            except IntegrityError as ie:
                # Handle race condition - another request might have created the same user
                errors['email'] = 'This email is already registered'
                context = {
                    'form': form,
                    'errors': errors,
                    'form_data': {
                        'email': email,
                        'mobile': mobile,
                        'aadhar_number': aadhar_number,
                    }
                }
                return render(request, 'common/reg_worker.html', context)

        else:
            # Form validation errors
            for field, error_list in form.errors.items():
                field_name = field
                if field == 'email':
                    errors['email'] = 'Please enter a valid email address'
                elif field == 'mobile':
                    errors['mobile'] = 'Please enter a valid mobile number'
                elif field == 'aadhar_number':
                    errors['aadhar'] = 'Please enter a valid Aadhar number'
                elif field == 'paswd':
                    errors['password'] = 'Password is required'
                else:
                    errors[field_name] = str(error_list[0]) if error_list else 'This field is required'
            
            print("FORM ERRORS =>", form.errors)

        # Render form with errors
        context = {
            'form': form,
            'errors': errors,
            'form_data': {
                'email': email,
                'mobile': mobile,
                'aadhar_number': aadhar_number,
            }
        }
        return render(request, 'common/reg_worker.html', context)

    return render(request, 'common/reg_worker.html', {'form': WorkerForm(), 'errors': {}, 'form_data': {}})
		
def vacancyinsert(request):
	"""Insert vacancy using ORM"""
	try:
		if 'u_id' not in request.session:
			html = "<script>alert('Please login first');window.location='/login/';</script>"
			return HttpResponse(html)
		
		emp_id = request.session['u_id']
		if request.method == 'POST':
			vacancy = request.POST.get('vacancy', '').strip()
			vacancy_num = request.POST.get('num', '').strip()
			description = request.POST.get('description', '').strip()
		else:
			# Backward compatibility for older GET based forms
			vacancy = request.GET.get('vacancy', '').strip()
			vacancy_num = request.GET.get('num', '').strip()
			description = request.GET.get('description', '').strip()
		
		if not all([vacancy, vacancy_num, description]):
			html = "<script>alert('All fields are required');window.location='/addvacancy/';</script>"
			return HttpResponse(html)
		
		tbl_vacancy.objects.create(
			date=now,
			emp_id=str(emp_id),
			vacancy=vacancy,
			vacancy_no=vacancy_num,
			description=description
		)
		
		html = "<script>alert('Vacancy created successfully!');window.location='/viewvacancy/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/addvacancy/';</script>"
		return HttpResponse(html)
def noc_insert1(request):
	"""Get workers for NOC entry using ORM"""
	try:
		# Get all workers from tbl_login that are active workers
		worker_logins = tbl_login.objects.filter(user_type='worker')
		workers_list = []
		
		for login in worker_logins:
			try:
				worker = tbl_worker.objects.get(worker_id=login.u_id)
				workers_list.append({
					'worker_id': worker.worker_id,
					'image': worker.image,
					'worker_name': worker.worker_name,
					'gender': worker.gender,
					'dob': worker.dob,
					'aadhar_number': worker.aadhar_number,
					'regis_date': worker.regis_date,
					'place': worker.place,
					'address': worker.address,
					'languages_known': worker.languages_known,
					'phone': worker.phone,
					'mobile': worker.mobile,
					'email': worker.email,
					'status': worker.status
				})
			except tbl_worker.DoesNotExist:
				continue
		
		return render(request, 'police/noc_insert1.html', {'list': workers_list})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homepolice/';</script>"
		return HttpResponse(html)
def addnoc(request):
	"""
	Display NOC form for a specific worker.
	Parameters:
	- worker_id: Required worker ID
	- _tsid: Optional tracking ID (ignored)
	"""
	worker_id = request.GET.get('worker_id')
	
	if not worker_id:
		html = "<script>alert('Worker ID is missing');window.location='/noc_insert1/';</script>"
		return HttpResponse(html)
	
	# Convert worker_id to integer for database query
	try:
		worker_id_int = int(worker_id)
	except ValueError:
		html = "<script>alert('Invalid Worker ID');window.location='/noc_insert1/';</script>"
		return HttpResponse(html)
	
	# Fetch worker details to display in the form
	try:
		worker = tbl_worker.objects.get(worker_id=worker_id_int)
		return render(request, 'police/noc.html', {'worker_id': worker_id, 'worker': worker})
	except tbl_worker.DoesNotExist:
		html = "<script>alert('Worker not found with ID: " + str(worker_id) + "');window.location='/noc_insert1/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = "<script>alert('Error: " + str(e) + "');window.location='/noc_insert1/';</script>"
		return HttpResponse(html)
def noc_insert(request):
	"""Insert NOC record using ORM"""
	try:
		if 'u_id' not in request.session:
			html = "<script>alert('Please login first');window.location='/login/';</script>"
			return HttpResponse(html)
		
		worker_id = request.GET.get('worker_id', '').strip()
		station_id = request.session['u_id']
		crime = request.GET.get('crime', '').strip()
		description = request.GET.get('description', '').strip()
		
		if not all([worker_id, crime, description]):
			html = "<script>alert('All fields are required');window.location='/homepolice/';</script>"
			return HttpResponse(html)
		
		tbl_noc.objects.create(
			worker_id=worker_id,
			station_id=str(station_id),
			date=now,
			crime=crime,
			crime_details=description
		)
		
		html = "<script>alert('NOC record created successfully!');window.location='/homepolice/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homepolice/';</script>"
		return HttpResponse(html)
def viewvacancydetails(request):
		cursor=connection.cursor()
		list=[]
		sql="select * from tbl_emp "
		
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row in result1:
			sql1="select * from tbl_vacancy where emp_id='%s'"%(row[0])
			cursor.execute(sql1)
			result=cursor.fetchall()
			for row1 in result:
				dict={'vacancy_id':row1[0],'date':row1[1],'emp_id':row1[2],'vacancy':row1[3],'vacancy_no':row1[4],'description':row1[5],'emp_id':row[0],'name':row[1],'gender':row[2],'firm_name':row[3],'aadhar_no':row[4],'dob':row[5],'emp_address':row[6],'place':row[7],'phone':row[8],'mobile':row[9],'email':row[10],'password':row[11],'status':row[12]}
				list.append(dict)
		return render(request,'agency/view_vacancy.html',{'list':list})

def insertworkerdetails(request):
		worker_id=request.session['u_id']
		vacancy_id=request.GET.get('v_id')

		# Validate vacancy_id
		if not vacancy_id:
			html = "<script>alert('Vacancy ID is missing');window.location='/viewvacancyhome/';</script>"
			return HttpResponse(html)

		# Check if form is submitted (experience and qualification are present)
		Experience = request.GET.get('experience')
		Qualification = request.GET.get('qualification')

		if Experience and Qualification:
			# Form submitted - insert into database
			cursor=connection.cursor()
			sql4="insert into tbl_workerdetails(worker_id,vacancy_id,experience,qualification)values('%s','%s','%s','%s')"%(worker_id,vacancy_id,Experience,Qualification)
			cursor.execute(sql4)
			html="<script>alert('successfully inserted! ');window.location='/viewvacancydetails/';</script>"
			return HttpResponse(html)

		# Show the form with vacancy_id
		return render(request,'agency/view_vacancyhome3.html',{'vacancy_id':vacancy_id})
# views.py

# views.py

# views.py

# views.py

from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
import datetime
import csv

def worker_salary(request):
    today = datetime.date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    export = request.GET.get('export') == 'csv'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                w.worker_name,
                SUM(s.salary) AS total_salary
            FROM tbl_workershedule s
            JOIN tbl_worker w ON s.worker_id = w.worker_id
            WHERE strftime('%%m', s.time_from) = %s AND strftime('%%Y', s.time_from) = %s
              AND s.attendance = 'Present'
            GROUP BY w.worker_name
        """, [str(month).zfill(2), str(year)])
        rows = cursor.fetchall()

    worker_salaries = [
        {'worker_name': row[0], 'total_salary': row[1]} for row in rows
    ]

    # If export=csv, return as CSV file
    if export:
        response = HttpResponse(content_type='text/csv')
        filename = f"worker_salaries_{year}_{month}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow(['Worker Name', 'Total Salary'])
        for row in worker_salaries:
            writer.writerow([row['worker_name'], row['total_salary']])
        return response

    return render(request, 'worker/worker_salary.html', {
        'worker_salaries': worker_salaries,
        'month': month,
        'year': year,
        'months': range(1, 13),
        'years': range(2020, 2031),
    })


def viewemprequest(request):
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='employer' and status='false'"
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_emp where emp_id='%s'"%(row1[3])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'emp_id':row[0],'name':row[1],'gender':row[2],'firm_name':row[3],'aadhar_no':row[4],'dob':row[5],'emp_address':row[6],'place':row[7],'phone':row[8],'mobile':row[9],'email':row[10],'password':row[11],'status':row[12]}
					list.append(dict)
		return render(request,'agency/view_emp.html',{'list':list})
def viewacceptemprequest(request):
		cursor=connection.cursor()
		emp_id=request.GET['emp_id']
		sql1="select * from tbl_emp where emp_id='%s'" %(emp_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		list=[]
		for row in result:
			dict={'emp_id':row[0],'name':row[1],'gender':row[2],'firm_name':row[3],'aadhar_no':row[4],'dob':row[5],'emp_address':row[6],'place':row[7],'phone':row[8],'mobile':row[9],'email':row[10],'password':row[11],'status':row[12]}
			list.append(dict)
		return render(request,'agency/view_idividual_emp.html',{'list':list})
def acceptemprequest(request):
		emp_id=request.GET['empid']
		cursor=connection.cursor()
		sql5="update tbl_login set status='true' where u_id='%s' and user_type='employer'" %(emp_id)
		
		cursor.execute(sql5)
		sql7="update tbl_emp set status='Active' where emp_id='%s'" %(emp_id)
		cursor.execute(sql7)
		html="<script>alert('successfully Accepted! ');window.location='/viewemprequest/';</script>"
		return HttpResponse(html)
def rejectemprequest(request):
		emp_id=request.GET['empid']
		cursor=connection.cursor()
		sql5="update tbl_login set status='reject' where u_id='%s' and user_type='employer'" %(emp_id)
		
		cursor.execute(sql5)
		sql7="update tbl_emp set status='Rejected' where emp_id='%s'" %(emp_id)
		cursor.execute(sql7)
		html="<script>alert('successfully Rejected! ');window.location='/viewemprequest/';</script>"
		return HttpResponse(html)
def approve(request):
  cursor=connection.cursor()
  id=request.GET['sid']
  sql="update tbl_login set status='true' where u_id='%s'"%(id)
  cursor.execute(sql)
  sql1="update tbl_worker set status='Active' where worker_id='%s'"%(id)
  cursor.execute(sql1)
  msg="<script>alert('updated');window.location='/homepolice/';</script>"
  return HttpResponse(msg)
def reject(request):
  cursor=connection.cursor()
  id=request.GET['sid']
  sql="update tbl_login set status='false' where u_id='%s'"%(id)
  cursor.execute(sql)
  sql1="update tbl_worker set status='Rejected' where worker_id='%s'"%(id)
  cursor.execute(sql1)
  msg="<script>alert('updated');window.location='/homepolice/';</script>"
  return HttpResponse(msg)
		
def viewworkeraccept(request):
	"""View worker registration requests for police approval using ORM for stability"""
	try:
		# Get all workers with status='false' from tbl_login
		worker_logins = tbl_login.objects.filter(user_type='worker', status='false')
		worker_list = []
		
		for login in worker_logins:
			try:
				worker = tbl_worker.objects.get(worker_id=login.u_id)
				worker_list.append({
					'worker_id': worker.worker_id,
					'image': worker.image,
					'worker_name': worker.worker_name,
					'gender': worker.gender,
					'dob': worker.dob,
					'aadhar_number': worker.aadhar_number,
					'regis_date': worker.regis_date,
					'place': worker.place,
					'address': worker.address,
					'languages_known': worker.languages_known,
					'phone': worker.phone,
					'mobile': worker.mobile,
					'email': worker.email,
					'status': worker.status
				})
			except tbl_worker.DoesNotExist:
				continue
				
		return render(request, 'police/viewworkeraccept.html', {'list': worker_list})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homepolice/';</script>"
		return HttpResponse(html)
def viewnocaccept(request):
	"""View NOC records for a specific worker using ORM"""
	try:
		worker_id = request.GET.get('worker_id')
		if not worker_id:
			html = "<script>alert('Worker ID missing');window.location='/viewworkeraccept/';</script>"
			return HttpResponse(html)
			
		noc_records = tbl_noc.objects.filter(worker_id=worker_id)
		
		if noc_records.exists():
			list_data = []
			for row in noc_records:
				dict_data = {
					'noc_id': row.noc_id,
					'worker_id': row.worker_id,
					'station_id': row.station_id,
					'date': row.date,
					'crime': row.crime,
					'crime_details': row.crime_details
				}
				list_data.append(dict_data)
			return render(request, 'police/viewnocaccept2.html', {'list': list_data})
		else:
			html = "<script>alert('No NOC added. Please find details of worker!');window.location='/viewworkeraccept/';</script>"
			return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/viewworkeraccept/';</script>"
		return HttpResponse(html)
def viewacceptworkerrequest(request):
	"""View individual worker request details using ORM"""
	try:
		worker_id = request.GET.get('worker_id')
		if not worker_id:
			return HttpResponse("<script>alert('Worker ID missing');window.location='/viewworkeraccept/';</script>")
			
		worker = tbl_worker.objects.get(worker_id=worker_id)
		dict_data = {
			'worker_id': worker.worker_id,
			'image': worker.image,
			'worker_name': worker.worker_name,
			'gender': worker.gender,
			'dob': worker.dob,
			'aadhar_number': worker.aadhar_number,
			'regis_date': worker.regis_date,
			'place': worker.place,
			'address': worker.address,
			'languages_known': worker.languages_known,
			'phone': worker.phone,
			'mobile': worker.mobile,
			'email': worker.email,
			'status': worker.status
		}
		return render(request, 'worker/view_individual_worker.html', {'list': [dict_data]})
	except tbl_worker.DoesNotExist:
		html = "<script>alert('Worker not found');window.location='/viewworkeraccept/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/viewworkeraccept/';</script>"
		return HttpResponse(html)
def acceptworkerrequest(request):
		worker_id=request.GET['worker_id']
		cursor=connection.cursor()
		sql5="update tbl_login set status='true' where u_id='%s' and user_type='worker'" %(worker_id)
		cursor.execute(sql5)
		sql7="update tbl_worker set status='Active' where worker_id='%s'" %(worker_id)
		cursor.execute(sql7)
		html="<script>alert('successfully Accepted! ');window.location='/homepolice/';</script>"
		return HttpResponse(html)
def rejectworkerrequest(request):
		worker_id=request.GET['worker_id']
		cursor=connection.cursor()
		sql5="update tbl_login set status='reject' where u_id='%s' and user_type='worker'" %(worker_id)
		
		cursor.execute(sql5)
		sql7="update tbl_worker set status='Rejected' where worker_id='%s'" %(worker_id)
		cursor.execute(sql7)
		html="<script>alert('successfully Rejected! ');window.location='/homepolice/';</script>"
		return HttpResponse(html)
def vieweditemp(request):
	"""Agency view: View profile details for editing using ORM"""
	try:
		u_id = request.session.get('u_id')
		if not u_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
			
		# Fetch employer details directly using the u_id from session
		# This is safer than the double lookup in tbl_login
		employer = tbl_emp.objects.get(emp_id=u_id)
		
		dict_data = {
			'emp_id': employer.emp_id,
			'name': employer.name,
			'gender': employer.gender,
			'firm_name': employer.firm_name,
			'aadhar_no': employer.aadhar_no,
			'dob': employer.dob,
			'emp_address': employer.emp_address,
			'place': employer.place,
			'phone': employer.phone,
			'mobile': employer.mobile,
			'email': employer.email,
			'password': employer.pswd,
			'status': employer.status
		}
		return render(request, 'agency/edit_view_emp.html', {'list': [dict_data]})
	except tbl_emp.DoesNotExist:
		html = "<script>alert('Employer record not found');window.location='/login/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def edit_employer(request):
		cursor=connection.cursor()
		emp_id=request.GET['empid']
		sql1="select * from tbl_emp where emp_id='%s'" %(emp_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		list=[]
		for row in result:
			dict={'emp_id':row[0],'name':row[1],'gender':row[2],'firm_name':row[3],'aadhar_no':row[4],'dob':row[5],'emp_address':row[6],'place':row[7],'phone':row[8],'mobile':row[9],'email':row[10],'password':row[11],'status':row[12]}
			list.append(dict)
		return render(request,'agency/edit_emp.html',{'list':list})
def update_employer(request):
		emp_id=request.GET['empid']
		Name=request.GET['name'] 
		Gender=request.GET['Gender']
		Office_name=request.GET['Firm_name']
		Aadhar_number=request.GET['Aadhar_number']
		DOB=request.GET['DOB']
		Address=request.GET['Emp_address']
		Place=request.GET['Place']
		Phone=int(request.GET['Phone'])
		Mobile=int(request.GET['Mobile'])
		Email_id=request.GET['Email_id']
		
		cursor=connection.cursor()
	
		sql7="update tbl_emp set name='%s',gender='%s',firm_name='%s',aadhar_no='%s',dob='%s',emp_address='%s',place='%s',phone='%s',mobile='%s',email='%s' where emp_id='%s'" %(Name,Gender,Office_name,Aadhar_number,DOB,Address,Place,Phone,Mobile,Email_id,emp_id)
		cursor.execute(sql7)
		html="<script>alert('successfully Editted! ');window.location='/homeemp/';</script>"
		
		return HttpResponse(html)
def viewworkerdetails(request):
	"""View all worker application details using ORM for stability"""
	try:
		details = tbl_workerdetails.objects.all().order_by('detail_id')
		list_data = []
		for detail in details:
			dict_data = {
				'worker_id': detail.worker_id,
				'vacancy_id': detail.vacancy_id,
				'qualification': detail.qualification,
				'experience': detail.experience
			}
			list_data.append(dict_data)
		return render(request, 'worker/view_shedduled_workerdetails.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def viewworker(request):
	"""View scheduled worker details using ORM for index stability"""
	try:
		worker_id = request.GET.get('worker_id')
		if not worker_id:
			return HttpResponse("<script>alert('Worker ID missing');window.location='/viewworkerdetails/';</script>")
			
		worker = tbl_worker.objects.get(worker_id=worker_id)
		dict_data = {
			'worker_id': worker.worker_id,
			'name': worker.worker_name,
			'gender': worker.gender,
			'dob': worker.dob,
			'aadhar_number': worker.aadhar_number,
			'regis_date': worker.regis_date,
			'place': worker.place,
			'address': worker.address,
			'languages_known': worker.languages_known,
			'phone': worker.phone,
			'mobile': worker.mobile,
			'email': worker.email
		}
		return render(request, 'worker/viewsheduledworker2.html', {'list': [dict_data]})
	except tbl_worker.DoesNotExist:
		html = "<script>alert('Worker not found');window.location='/viewworkerdetails/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/viewworkerdetails/';</script>"
		return HttpResponse(html)
def feedbackinsert(request):
		#now=datetime.datetime.today()
		Emp_id=request.session['u_id']
		Worker_id=request.GET['worker_id']
		Feedback_title=request.GET['title'] 
		Feedback_description=request.GET['description']
		cursor=connection.cursor()
		
		sql4="insert into tbl_feedback(date,emp_id,worker_id,feedback_title,feedback_description)values('%s','%s','%s','%s','%s')"%(now,Emp_id,Worker_id,Feedback_title,Feedback_description) 
		cursor.execute(sql4)
		html="<script>alert('successfully inserted! ');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def addfeedback(request):
		worker_id=request.GET['worker_id']
		return render(request,'agency/feedback.html',{'worker_id':worker_id})
def viewemydetails(request):
	"""Agency view: View profile details using ORM for stability"""
	try:
		u_id = request.session.get('u_id')
		if not u_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
			
		# Fetch employer details directly using the u_id from session
		employer = tbl_emp.objects.get(emp_id=u_id)
		
		dict_data = {
			'emp_id': employer.emp_id,
			'name': employer.name,
			'gender': employer.gender,
			'firm_name': employer.firm_name,
			'aadhar_no': employer.aadhar_no,
			'dob': employer.dob,
			'emp_address': employer.emp_address,
			'place': employer.place,
			'phone': employer.phone,
			'mobile': employer.mobile,
			'email': employer.email,
			'password': employer.pswd,
			'status': employer.status
		}
		return render(request, 'agency/view_mydetails.html', {'list': [dict_data]})
	except tbl_emp.DoesNotExist:
		html = "<script>alert('Employer record not found');window.location='/login/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def viewempworker(request):
	"""View all active workers for agency using ORM for stability"""
	try:
		# Get active worker IDs from login
		worker_ids = tbl_login.objects.filter(user_type='worker', status='true').values_list('u_id', flat=True)
		workers = tbl_worker.objects.filter(worker_id__in=worker_ids).order_by('worker_id')
		
		list_data = []
		for row in workers:
			dict_data = {
				'worker_id': row.worker_id,
				'worker_name': row.worker_name,
				'gender': row.gender,
				'dob': row.dob,
				'aadhar_number': row.aadhar_number,
				'regis_date': row.regis_date,
				'place': row.place,
				'address': row.address,
				'languages_known': row.languages_known,
				'phone': row.phone,
				'mobile': row.mobile,
				'email': row.email
			}
			list_data.append(dict_data)
		return render(request, 'agency/view_empworker.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def viewnoc1(request):
	"""View workers for NOC processing using ORM for stability"""
	try:
		worker_ids = tbl_login.objects.filter(user_type='worker').values_list('u_id', flat=True)
		workers = tbl_worker.objects.filter(worker_id__in=worker_ids).order_by('worker_id')
		
		list_data = []
		for worker in workers:
			dict_data = {
				'worker_id': worker.worker_id,
				'image': worker.image,
				'worker_name': worker.worker_name,
				'gender': worker.gender,
				'dob': worker.dob,
				'aadhar_number': worker.aadhar_number,
				'regis_date': worker.regis_date,
				'place': worker.place,
				'address': worker.address,
				'languages_known': worker.languages_known,
				'phone': worker.phone,
				'mobile': worker.mobile,
				'email': worker.email,
				'status': worker.status
			}
			list_data.append(dict_data)
		return render(request, 'police/view_noc1.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homepolice/';</script>"
		return HttpResponse(html)
def viewnoc2(request):
	"""View detailed NOC for a worker using ORM to avoid index shifts"""
	try:
		worker_id = request.GET.get('worker_id')
		if not worker_id:
			html = "<script>alert('Worker ID missing');window.location='/viewnoc1/';</script>"
			return HttpResponse(html)
			
		# Get latest NOC for worker
		noc = tbl_noc.objects.filter(worker_id=worker_id).order_by('-noc_id').first()
		
		if noc:
			try:
				worker = tbl_worker.objects.get(worker_id=noc.worker_id)
				dict_data = {
					'noc_id': noc.noc_id,
					'worker_id': noc.worker_id,
					'station_id': noc.station_id,
					'date': noc.date,
					'crime': noc.crime,
					'crime_details': noc.crime_details,
					'image': worker.image,
					'worker_name': worker.worker_name,
					'gender': worker.gender,
					'dob': worker.dob,
					'aadhar_number': worker.aadhar_number,
					'regis_date': worker.regis_date,
					'place': worker.place,
					'address': worker.address,
					'languages_known': worker.languages_known,
					'phone': worker.phone,
					'mobile': worker.mobile,
					'email': worker.email,
					'status': worker.status
				}
				return render(request, 'police/view_noc2.html', {'list': [dict_data]})
			except tbl_worker.DoesNotExist:
				html = "<script>alert('Worker profile not found for this NOC.');window.location='/viewnoc1/';</script>"
				return HttpResponse(html)
		else:
			html = "<script>alert('No NOC added. Please find the details and add it !! ');window.location='/viewnoc1/';</script>"
			return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/viewnoc1/';</script>"
		return HttpResponse(html)



def viewvacancy(request):
	"""View vacancies for the logged-in employer using ORM"""
	try:
		# Check session
		if 'u_id' not in request.session:
			html = "<script>alert('Please login first');window.location='/login/';</script>"
			return HttpResponse(html)
		
		emp_id = request.session['u_id']
		
		# Get employer details using ORM
		try:
			employer = tbl_emp.objects.get(emp_id=emp_id)
		except tbl_emp.DoesNotExist:
			return render(request, 'agency/view_vacancy.html', {'list': []})
		
		# Get all vacancies for this employer using ORM
		# Note: emp_id in tbl_vacancy is stored as CharField, so convert to string
		vacancies = tbl_vacancy.objects.filter(emp_id=str(emp_id))
		
		list_data = []
		for vacancy in vacancies:
			dict_data = {
				'vacancy_id': vacancy.vacancy_id,
				'date': vacancy.date,
				'emp_id': vacancy.emp_id,
				'vacancy': vacancy.vacancy,
				'vacancy_no': vacancy.vacancy_no,
				'description': vacancy.description,
				'name': employer.name,
				'gender': employer.gender,
				'firm_name': employer.firm_name,
				'aadhar_no': employer.aadhar_no,
				'dob': employer.dob,
				'emp_address': employer.emp_address,
				'place': employer.place,
				'phone': employer.phone,
				'mobile': employer.mobile,
				'email': employer.email,
				'status': employer.status
			}
			list_data.append(dict_data)
		
		return render(request, 'agency/view_vacancy.html', {'list': list_data})
		
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)

def view_vacany2(request):
	"""Agency vacancy detail page (prevents redirecting into worker flow)."""
	try:
		if 'u_id' not in request.session:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")

		emp_id = request.session['u_id']
		vacancy_id = request.GET.get('vacancy_id', '').strip()

		vacancies = tbl_vacancy.objects.filter(emp_id=str(emp_id))
		if vacancy_id:
			vacancies = vacancies.filter(vacancy_id=vacancy_id)

		list_data = []
		for vacancy in vacancies.order_by('-vacancy_id'):
			list_data.append({
				'vacancy_id': vacancy.vacancy_id,
				'date': vacancy.date,
				'vacancy': vacancy.vacancy,
				'vacancy_no': vacancy.vacancy_no,
				'description': vacancy.description,
			})

		return render(request, 'agency/view_vacancy2.html', {'list': list_data})
	except Exception as e:
		return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='/viewvacancy/';</script>")

def editvacancy1(request):
    """View vacancies for editing - uses ORM for better reliability"""
    try:
        # Check if user is logged in
        if 'u_id' not in request.session:
            html = "<script>alert('Please login first');window.location='/login/';</script>"
            return HttpResponse(html)
        
        emp_id = request.session['u_id']
        
        # Get employer details
        try:
            employer = tbl_emp.objects.get(emp_id=emp_id)
        except tbl_emp.DoesNotExist:
            return render(request, 'agency/edit_vacancy1.html', {'list': []})
        
        # Get all vacancies for this employer
        vacancies = tbl_vacancy.objects.filter(emp_id=str(emp_id))
        
        list_data = []
        for vacancy in vacancies:
            dict_data = {
                'vacancy_id': vacancy.vacancy_id,
                'date': vacancy.date,
                'emp_id': vacancy.emp_id,
                'vacancy': vacancy.vacancy,
                'vacancy_no': vacancy.vacancy_no,
                'description': vacancy.description,
                'name': employer.name,
                'gender': employer.gender,
                'firm_name': employer.firm_name,
                'aadhar_no': employer.aadhar_no,
                'dob': employer.dob,
                'emp_address': employer.emp_address,
                'place': employer.place,
                'phone': employer.phone,
                'mobile': employer.mobile,
                'email': employer.email,
                'status': employer.status
            }
            list_data.append(dict_data)
        
        return render(request, 'agency/edit_vacancy1.html', {'list': list_data})
        
    except Exception as e:
        html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
        return HttpResponse(html)

def editvacancy2(request):
		cursor=connection.cursor()
		vacancy_id=request.GET['vacancy_id']
		sql1="select * from tbl_vacancy where vacancy_id='%s'" %(vacancy_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		list=[]
		for row1 in result:
			dict={'vacancy_id':row1[0],'date':row1[1],'emp_id':row1[2],'vacancy':row1[3],'vacancy_no':row1[4],'description':row1[5]}
			list.append(dict)
		return render(request,'agency/edit_vacancy2.html',{'list':list})
def editvacancy3(request):
		vacancy_id=request.GET['vacancyid']
		#now=datetime.datetime.today()
		emp_id=request.session['u_id']
		Vacancy=request.GET['vacancy'] 
		Vacancy_num=request.GET['num']
		Description=request.GET['des']
		
		cursor=connection.cursor()
	
		sql7="update tbl_vacancy set date='%s',emp_id='%s',vacancy='%s',vacancy_no='%s',description='%s' where vacancy_id='%s' " %(now,emp_id,Vacancy,Vacancy_num,Description,vacancy_id)
		cursor.execute(sql7)
		html="<script>alert('successfully Editted! ');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def viewvacancyhome(request):
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='employer'"
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_emp where emp_id='%s' and emp_id in(select emp_id from tbl_vacancy)"%(row1[3])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					sql2="select vacancy_id, date, vacancy, vacancy_no, description, place from tbl_vacancy where emp_id='%s'"%(row[0])
					cursor.execute(sql2)
					result2=cursor.fetchall()
					for row2 in result2:
						dict={'vacancy_id':row2[0],'date':row2[1],'vacancy':row2[2],'vacancy_no':row2[3],'description':row2[4],'place':row2[5],'emp_id':row[0],'name':row[1],'firm_name':row[3]}
						list.append(dict)
		return render(request,'agency/view_vacancyhome.html',{'list':list})

def viewvacancyhome2(request):
		cursor=connection.cursor()
		Emp_id=request.GET['emp_id']
		sql1="select * from tbl_vacancy where emp_id='%s'" %(Emp_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		list=[]
		for row1 in result:
			dict={'vacancy_id':row1[0],'date':row1[1],'emp_id':row1[2],'vacancy':row1[3],'vacancy_no':row1[4],'description':row1[5]}
			list.append(dict)
		return render(request,'agency/view_vacancyhome2.html',{'list':list})
def viewvacancyhome3(request):
		worker_id=request.session['u_id']
		vacancy_id=request.GET['vacancy_id']
		return render(request,'agency/view_vacancyhome3.html',{'vacancy_id':vacancy_id})
def viewvacancyhome4(request):
		worker_id=request.session['u_id']
		vacancy_id=request.GET['v_id']
		Experience=request.GET['experience'] 
		Qualification=request.GET['qualification']
		cursor=connection.cursor()
		sql="select vacancy_id from tbl_workerdetails where worker_id='%s' and vacancy_id='%s'"%(worker_id,vacancy_id)
		cursor.execute(sql)
		if(cursor.rowcount>0): 
			html="<script>alert('Already applied! ');window.location='/homeworker/';</script>"
		else:
			sql4="insert into tbl_workerdetails(worker_id,vacancy_id,experience,qualification)values('%s','%s','%s','%s')"%(worker_id,vacancy_id,Experience,Qualification) 
			cursor.execute(sql4)
			html="<script>alert('successfully inserted! ');window.location='/homeworker/';</script>"
		return HttpResponse(html)
def viewappliedvacancy(request):
	"""Agency view: View workers who applied to vacancies using ORM"""
	try:
		emp_id = request.session.get('u_id')
		if not emp_id or request.session.get('user_type') != 'employer':
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
		
		# 1. Get all vacancies created by this employer
		vacancies = tbl_vacancy.objects.filter(emp_id=str(emp_id)).order_by('-vacancy_id')
		vacancy_map = {str(v.vacancy_id): v for v in vacancies}
		vacancy_ids = list(vacancy_map.keys())
		list_data = []

		# 2. Get all applications for employer vacancies in one pass.
		# vacancy_id in tbl_workerdetails is CharField; normalize with strip.
		if vacancy_ids:
			applications = tbl_workerdetails.objects.filter(vacancy_id__in=vacancy_ids).order_by('-detail_id')
		else:
			applications = []

		for app in applications:
			normalized_vacancy_id = str(app.vacancy_id).strip()
			vacancy = vacancy_map.get(normalized_vacancy_id)
			if not vacancy:
				continue
			try:
				# 3. Get worker details
				worker = tbl_worker.objects.get(worker_id=app.worker_id)
				dict_data = {
					'date': vacancy.date,
					'vacancy': vacancy.vacancy,
					'vacancy_no': vacancy.vacancy_no,
					'description': vacancy.description,
					'worker_id': worker.worker_id,
					'vacancy_id': vacancy.vacancy_id,
					'qualification': app.qualification,
					'experience': app.experience,
					'worker_name': worker.worker_name,
					'gender': worker.gender,
					'dob': worker.dob,
					'aadhar_number': worker.aadhar_number,
					'place': worker.place,
					'address': worker.address,
					'phone': worker.phone,
					'mobile': worker.mobile,
					'email': worker.email,
					'status': worker.status
				}
				list_data.append(dict_data)
			except tbl_worker.DoesNotExist:
				continue
		
		return render(request, 'worker/view_appliedvacancy.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)

def index(request):
	return render(request,'common/index.html')
def login(request):
	return render(request,'common/login.html')
def viewappliedvacancy2(request):
		cursor=connection.cursor()
		v_id=request.GET.get('vacid', '').strip()
		w_id=request.GET.get('worid', '').strip()
		if not v_id or not w_id:
			return HttpResponse("<script>alert('Vacancy id is missing');window.location='/viewappliedvacancy/';</script>")
		sql1="select * from tbl_worker where worker_id='%s'"%(w_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		list=[]
		for row in result:
				dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
				list.append(dict)
		sql1="select * from tbl_feedback where worker_id='%s'"%(w_id)
		cursor.execute(sql1)
		result1=cursor.fetchall()
		feed=[]
		for row1 in result1:
				dict={'feedback_title':row1[4],'feedback_description':row1[5]}
				feed.append(dict)
		return render(request,'worker/view_appliedvacancy2.html',{'list':list,'feed':feed})
def addmyworker(request):
		emp_id=request.session['u_id']
		worker_id=request.GET['worker_id']
		vacancy_id=request.GET['vacancy_id']
		Date=now 
		cursor=connection.cursor()
		sql1="select status from tbl_worker where worker_id='%s'"%(worker_id)
		cursor.execute(sql1)
		result2=cursor.fetchall()
		for r2 in result2:
			status1=r2[0]
		if(status1=='Active'):
			sql4="insert into tbl_myworker(emp_id,worker_id,vacancy_id,date,status)values('%s','%s','%s','%s','%s')"%(emp_id,worker_id,vacancy_id,Date,'fixed') 
			cursor.execute(sql4)
			sql5="update  tbl_worker set status='fixed' where worker_id='%s'"%(worker_id) 
			cursor.execute(sql5)
			html="<script>alert('successfully inserted! ');window.location='/homeemp/';</script>"
		else:
			html="<script>alert('Cannot add as myworker! ');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def view_feedbackworker(request):
	"""Agency view: View my workers to add feedback using ORM"""
	try:
		emp_id = request.session.get('u_id')
		if not emp_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
			
		# Use str(emp_id) because emp_id is CharField in tbl_myworker
		my_workers = tbl_myworker.objects.filter(emp_id=str(emp_id))
		list_data = []
		male_count = 0
		female_count = 0
		
		for my_w in my_workers:
			try:
				# Use str(my_w.worker_id) for safety
				worker = tbl_worker.objects.get(worker_id=str(my_w.worker_id))
				
				# Count genders for stats
				gender = str(worker.gender).lower()
				if gender == 'male':
					male_count += 1
				elif gender == 'female':
					female_count += 1
					
				dict_data = {
					'worker_id': worker.worker_id,
					'image': worker.image,
					'worker_name': worker.worker_name,
					'gender': worker.gender,
					'dob': worker.dob,
					'aadhar_number': worker.aadhar_number,
					'regis_date': worker.regis_date,
					'place': worker.place,
					'address': worker.address,
					'languages_known': worker.languages_known,
					'phone': worker.phone,
					'mobile': worker.mobile,
					'email': worker.email,
					'status': worker.status
				}
				list_data.append(dict_data)
			except tbl_worker.DoesNotExist:
				continue
				
		return render(request, 'worker/view_feedbackworker.html', {
			'list': list_data,
			'male_count': male_count,
			'female_count': female_count
		})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)
		
def editfeedbackworker1(request):
	"""Agency view: List workers to edit feedback using ORM"""
	try:
		emp_id = request.session.get('u_id')
		if not emp_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
			
		# Filter fixed workers for this employer
		my_workers = tbl_myworker.objects.filter(status='fixed', emp_id=str(emp_id))
		list_data = []
		
		for my_w in my_workers:
			try:
				worker = tbl_worker.objects.get(worker_id=str(my_w.worker_id))
				dict_data = {
					'worker_id': worker.worker_id,
					'image': worker.image,
					'worker_name': worker.worker_name,
					'gender': worker.gender,
					'dob': worker.dob,
					'aadhar_number': worker.aadhar_number,
					'regis_date': worker.regis_date,
					'place': worker.place,
					'address': worker.address,
					'languages_known': worker.languages_known,
					'phone': worker.phone,
					'mobile': worker.mobile,
					'email': worker.email
				}
				list_data.append(dict_data)
			except tbl_worker.DoesNotExist:
				continue
		
		return render(request, 'worker/editfeedbackworker1.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)
		
def editfeedbackworker2(request):
		"""Agency: open latest feedback for a worker scoped to current employer."""
		emp_id = request.session.get('u_id')
		worker_id = request.GET.get('worker_id', '').strip()
		if not emp_id or not worker_id:
			return HttpResponse("<script>alert('Missing worker details');window.location='/editfeedbackworker1/';</script>")
		
		feedback = tbl_feedback.objects.filter(
			worker_id=str(worker_id),
			emp_id=str(emp_id)
		).order_by('-feedback_id').first()
		
		if feedback:
			list_data = [{
				'feedback_id': feedback.feedback_id,
				'date': feedback.date,
				'emp_id': feedback.emp_id,
				'worker_id': feedback.worker_id,
				'feedback_title': feedback.feedback_title,
				'feedback_description': feedback.feedback_description
			}]
			return render(request, 'worker/edit_feedbackworker2.html', {'list': list_data})
		
		html = "<script>alert('No feedback added for this worker by your agency.');window.location='/editfeedbackworker1/';</script>"
		return HttpResponse(html)
def editfeedbackworker3(request):
		"""Agency: update feedback safely for own record only."""
		emp_id = request.session.get('u_id')
		feedback_id = request.GET.get('feedbackid', '').strip()
		feedback_title = request.GET.get('feedback_title', '').strip()
		feedback_description = request.GET.get('des', '').strip()
		
		if not emp_id or not feedback_id:
			return HttpResponse("<script>alert('Invalid feedback update request');window.location='/editfeedbackworker1/';</script>")
		
		try:
			feedback = tbl_feedback.objects.get(feedback_id=feedback_id, emp_id=str(emp_id))
		except tbl_feedback.DoesNotExist:
			return HttpResponse("<script>alert('Feedback not found for your agency');window.location='/editfeedbackworker1/';</script>")
		
		feedback.date = now
		feedback.feedback_title = feedback_title
		feedback.feedback_description = feedback_description
		feedback.save()
		return HttpResponse("<script>alert('successfully Editted!');window.location='/homeemp/';</script>")
def viewemydetailsworker(request):
	"""Worker self-profile edit view"""
	try:
		u_id = request.session.get('u_id')
		if not u_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")

		worker = tbl_worker.objects.get(worker_id=u_id)

		if request.method == 'POST':
			worker.worker_name = request.POST.get('worker_name', worker.worker_name).strip()
			worker.gender = request.POST.get('gender', worker.gender).strip()
			worker.dob = request.POST.get('dob', worker.dob).strip()
			worker.aadhar_number = request.POST.get('aadhar_number', worker.aadhar_number).strip()
			worker.languages_known = request.POST.get('languages_known', worker.languages_known).strip()
			worker.email = request.POST.get('email', worker.email).strip()
			worker.mobile = request.POST.get('mobile', worker.mobile).strip()
			worker.phone = request.POST.get('phone', worker.phone).strip()
			worker.address = request.POST.get('address', worker.address).strip()
			worker.place = request.POST.get('place', worker.place).strip()

			if request.FILES.get('image'):
				worker.image = request.FILES['image']

			worker.save()
			return HttpResponse("<script>alert('Profile updated successfully');window.location='/worker_profile/';</script>")

		return render(request, 'worker/view_mydetailsworker.html', {'worker': worker})
	except tbl_worker.DoesNotExist:
		return HttpResponse("<script>alert('Worker profile not found');window.location='/homeworker/';</script>")
	except Exception as e:
		return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='/worker_profile/';</script>")

def worker_profile(request):
	"""Display worker profile using ORM for stability"""
	try:
		u_id = request.session.get('u_id')
		if not u_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
			
		worker = tbl_worker.objects.get(worker_id=u_id)
		dict_data = {
			'worker_id': worker.worker_id,
			'image': worker.image,
			'worker_name': worker.worker_name,
			'gender': worker.gender,
			'dob': worker.dob,
			'age': worker.age,
			'aadhar_number': worker.aadhar_number,
			'regis_date': worker.regis_date,
			'place': worker.place,
			'address': worker.address,
			'languages_known': worker.languages_known,
			'phone': worker.phone,
			'mobile': worker.mobile,
			'email': worker.email,
			'status': worker.status
		}
		return render(request, 'worker/worker_profile.html', {'worker': dict_data})
	except tbl_worker.DoesNotExist:
		html = "<script>alert('Worker profile not found');window.location='/homeworker/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeworker/';</script>"
		return HttpResponse(html)
def viewmyworker(request):
	"""View my workers for the logged-in employer using ORM"""
	try:
		# Check session
		if 'u_id' not in request.session:
			html = "<script>alert('Please login first');window.location='/login/';</script>"
			return HttpResponse(html)
		
		emp_id = request.session['u_id']
		
		# Get all myworkers for this employer using ORM
		# Use str(emp_id) because emp_id is CharField in tbl_myworker
		myworkers = tbl_myworker.objects.filter(status='fixed', emp_id=str(emp_id))
		
		list_data = []
		for myworker in myworkers:
			try:
				worker = tbl_worker.objects.get(worker_id=myworker.worker_id)
				dict_data = {
					'worker_id': worker.worker_id,
					'image': worker.image,
					'worker_name': worker.worker_name,
					'gender': worker.gender,
					'dob': worker.dob,
					'aadhar_number': worker.aadhar_number,
					'regis_date': worker.regis_date,
					'place': worker.place,
					'address': worker.address,
					'languages_known': worker.languages_known,
					'phone': worker.phone,
					'mobile': worker.mobile,
					'email': worker.email,
					'status': worker.status
				}
				list_data.append(dict_data)
			except tbl_worker.DoesNotExist:
				continue
		
		return render(request, 'agency/view_myworker.html', {'list': list_data})
		
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)

def viewfeedback(request):
	"""Agency view: View feedback given by this agency using ORM"""
	try:
		emp_id = request.session.get('u_id')
		if not emp_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
			
		feedbacks = tbl_feedback.objects.filter(emp_id=str(emp_id))
		list_data = []
		
		for fb in feedbacks:
			try:
				worker = tbl_worker.objects.get(worker_id=fb.worker_id)
				dict_data = {
					'feedback_id': fb.feedback_id,
					'worker_id': fb.worker_id,
					'emp_id': fb.emp_id,
					'date': fb.date,
					'feedback_title': fb.feedback_title, # Corrected field name
					'feedback_description': fb.feedback_description, # Corrected field name
					'worker_name': worker.worker_name,
					'image': worker.image, # Added image
					'gender': worker.gender, # Added gender
					'address': worker.address, # Added address
					'mobile': worker.mobile, # Added mobile
					'email': worker.email # Added email
				}
				list_data.append(dict_data)
			except tbl_worker.DoesNotExist:
				continue
				
		return render(request, 'agency/view_feedback.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def viewadmin(request):
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='admin' and u_id='%s'"%(request.session['u_id'])
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_admin where admin_id='%s'"%(row1[3])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row1 in result:
					dict={'admin_id':row1[0],'name':row1[1],'country':row1[2],'state':row1[3],'phone':row1[4],'mobile':row1[5],'email':row1[6]}
					list.append(dict)
		return render(request,'admin/view_admin.html',{'list':list})
def editadmin1(request):
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='admin' and u_id='%s'"%(request.session['u_id'])
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_admin where admin_id='%s'"%(row1[3])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row1 in result:
					dict={'admin_id':row1[0],'name':row1[1],'country':row1[2],'state':row1[3],'phone':row1[4],'mobile':row1[5],'email':row1[6]}
					list.append(dict)
		return render(request,'admin/edit_admin1.html',{'list':list})
def editadmin2(request):
		cursor=connection.cursor()
		admin_id=request.GET['admin_id']
		sql1="select * from tbl_admin where admin_id=(select max(admin_id) from tbl_admin where admin_id='%s') " %(admin_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		list=[]
		for row1 in result:
			dict={'admin_id':row1[0],'name':row1[1],'country':row1[2],'state':row1[3],'phone':row1[4],'mobile':row1[5],'email':row1[6]}
			list.append(dict)
		return render(request,'admin/edit_admin2.html',{'list':list})
def editadmin3(request):
		
		admin_id=request.GET['admin_id']
		
		
		Name=request.GET['name'] 
		Country=request.GET['country']
		State=request.GET['state']
		Phone=request.GET['phone']
		Mobile=request.GET['mobile']
		Email=request.GET['email']
		
		cursor=connection.cursor()
	
		sql7="update tbl_admin set name='%s',country='%s',state='%s',phone='%s',mobile='%s',email='%s' where admin_id='%s'" %(Name,Country,State,Phone,Mobile,Email)
		cursor.execute(sql7)
		html="<script>alert('successfully Editted!');window.location='/homeadmin/';</script>"
def viewadminworker(request):
	"""Admin view: List all workers using ORM for stability"""
	try:
		workers = tbl_worker.objects.all().order_by('worker_id')
		list_data = []
		for row in workers:
			image_url = ''
			if row.image:
				try:
					image_url = row.image.url
				except Exception:
					raw_name = str(row.image).replace('\\', '/').strip()
					if raw_name:
						if raw_name.startswith('media/'):
							raw_name = raw_name[len('media/'):]
						candidate_names = [raw_name]
						base_name = os.path.basename(raw_name)
						if base_name:
							candidate_names.extend([f"workers/{base_name}", f"pictures/{base_name}"])
						for name in candidate_names:
							full_path = os.path.join(settings.MEDIA_ROOT, name)
							if os.path.exists(full_path):
								image_url = f"{settings.MEDIA_URL}{name}".replace('\\', '/')
								break
			dict_data = {
				'worker_id': row.worker_id,
				'image': row.image,
				'image_url': image_url,
				'worker_name': row.worker_name,
				'gender': row.gender,
				'dob': row.dob,
				'aadhar_number': row.aadhar_number,
				'regis_date': row.regis_date,
				'place': row.place,
				'address': row.address,
				'languages_known': row.languages_known,
				'phone': row.phone,
				'mobile': row.mobile,
				'email': row.email,
				'status': row.status
			}
			list_data.append(dict_data)
		return render(request, 'admin/view_adminworker.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeadmin/';</script>"
		return HttpResponse(html)
def editadminworker(request):
	"""Admin view: List all workers for editing using ORM"""
	try:
		workers = tbl_worker.objects.all().order_by('worker_id')
		list_data = []
		for row in workers:
			dict_data = {
				'worker_id': row.worker_id,
				'image': row.image,
				'worker_name': row.worker_name,
				'gender': row.gender,
				'dob': row.dob,
				'aadhar_number': row.aadhar_number,
				'regis_date': row.regis_date,
				'place': row.place,
				'address': row.address,
				'languages_known': row.languages_known,
				'phone': row.phone,
				'mobile': row.mobile,
				'email': row.email,
				'status': row.status
			}
			list_data.append(dict_data)
		return render(request, 'admin/edit_adminworker.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeadmin/';</script>"
		return HttpResponse(html)
def editadminworker2(request):
	"""Admin view: Individual worker details for editing using ORM"""
	try:
		worker_id = request.GET.get('worker_id')
		worker = tbl_worker.objects.get(worker_id=worker_id)
		dict_data = {
			'worker_id': worker.worker_id,
			'image': worker.image,
			'worker_name': worker.worker_name,
			'gender': worker.gender,
			'dob': worker.dob,
			'aadhar_number': worker.aadhar_number,
			'regis_date': worker.regis_date,
			'place': worker.place,
			'address': worker.address,
			'languages_known': worker.languages_known,
			'phone': worker.phone,
			'mobile': worker.mobile,
			'email': worker.email,
			'status': worker.status
		}
		return render(request, 'admin/edit_adminworker2.html', {'list': [dict_data]})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/editadminworker/';</script>"
		return HttpResponse(html)
def editadminworker3(request):
		worker_id=request.GET['worker_id']
		Name=request.GET['name']
		Gender=request.GET['gender']
		DOB=request.GET['dob']
		Aadhar_number=request.GET['aadhar_number']
		
		place=request.GET['place']
		address=request.GET['address']
		languages_known=request.GET['languages_known']
		phone=request.GET['phone']
		mobile=request.GET['mobile']
		email=request.GET['email']
		
		
		cursor=connection.cursor()
	
		sql7="update tbl_worker set worker_name='%s',gender='%s',dob='%s',aadhar_number='%s',regis_date='%s',place='%s',address='%s',languages_known='%s',phone='%s',mobile='%s',email='%s' where worker_id='%s' " %(Name,Gender,DOB,Aadhar_number,now,place,address,languages_known,phone,mobile,email,worker_id)
		cursor.execute(sql7)
		html="<script>alert('successfully Editted! ');window.location='/homeadmin/';</script>"
		return HttpResponse(html)
def viewempadmin(request):
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='employer' "
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_emp where emp_id='%s'"%(row1[3])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'emp_id':row[0],'name':row[1],'gender':row[2],'firm_name':row[3],'aadhar_no':row[4],'dob':row[5],'emp_address':row[6],'place':row[7],'phone':row[8],'mobile':row[9],'email':row[10],'status':row[12]}
					list.append(dict)
		return render(request,'admin/viewempadmin.html',{'list':list})


# Admin Employer Approval Views
def admin_view_pending_employers(request):
	"""Admin view: List all pending employer registrations using ORM"""
	try:
		# Keep this page accessible for legacy admin flows that may not set u_id,
		# but still block clearly non-admin logged-in users.
		session_user_type = request.session.get('user_type')
		if session_user_type and session_user_type != 'admin':
			return redirect('/login/')
			
		# Get pending logins for employers
		pending_logins = tbl_login.objects.filter(user_type='employer', status='false')
		list_data = []
		
		for login in pending_logins:
			try:
				emp = tbl_emp.objects.get(emp_id=str(login.u_id))
				dict_data = {
					'emp_id': emp.emp_id,
					'name': emp.name,
					'gender': emp.gender,
					'firm_name': emp.firm_name,
					'aadhar_no': emp.aadhar_no,
					'dob': emp.dob,
					'emp_address': emp.emp_address,
					'place': emp.place,
					'phone': emp.phone,
					'mobile': emp.mobile,
					'email': emp.email,
					'status': 'Pending'
				}
				list_data.append(dict_data)
			except tbl_emp.DoesNotExist:
				continue
				
		return render(request, 'admin/approve_employer.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeadmin/';</script>"
		return HttpResponse(html)


def admin_view_all_employers(request):
	"""Admin view: List all employer/agency details using ORM"""
	try:
		# Keep this page accessible for legacy admin flows that may not set u_id,
		# but still block clearly non-admin logged-in users.
		session_user_type = request.session.get('user_type')
		if session_user_type and session_user_type != 'admin':
			return redirect('/login/')
			
		# Get all employers from tbl_emp
		employers = tbl_emp.objects.all().order_by('emp_id')
		list_data = []
		
		for emp in employers:
			# Get status from tbl_login
			# Use filter().first() instead of get() to handle multiple login records
			login_entry = tbl_login.objects.filter(u_id=str(emp.emp_id)).first()
			if login_entry:
				status = 'Active' if login_entry.status == 'true' else 'pending'
			else:
				status = 'Unknown'
				
			dict_data = {
				'emp_id': emp.emp_id,
				'name': emp.name,
				'gender': emp.gender,
				'firm_name': emp.firm_name,
				'aadhar_no': emp.aadhar_no,
				'dob': emp.dob,
				'emp_address': emp.emp_address,
				'place': emp.place,
				'phone': emp.phone,
				'mobile': emp.mobile,
				'email': emp.email,
				'status': status
			}
			list_data.append(dict_data)
			
		return render(request, 'admin/view_all_employers.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeadmin/';</script>"
		return HttpResponse(html)


def admin_view_single_employer(request):
	"""Admin view: View individual employer/agency complete details"""
	try:
		emp_id = request.GET.get('emp_id')
		if not emp_id:
			html = "<script>alert('Employer ID missing');window.location='/admin_view_all_employers/';</script>"
			return HttpResponse(html)
			
		cursor = connection.cursor()
		sql1 = "SELECT * FROM tbl_emp WHERE emp_id='%s'" % (emp_id)
		cursor.execute(sql1)
		result = cursor.fetchall()
		
		list_data = []
		for row in result:
			dict_data = {
				'emp_id': row[0],
				'name': row[1],
				'gender': row[2],
				'firm_name': row[3],
				'aadhar_no': row[4],
				'dob': row[5],
				'emp_address': row[6],
				'place': row[7],
				'phone': row[8],
				'mobile': row[9],
				'email': row[10],
				'status': row[12]
			}
			list_data.append(dict_data)
		return render(request, 'admin/view_single_employer.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/admin_view_all_employers/';</script>"
		return HttpResponse(html)


def admin_view_employer_detail(request):
	"""Admin view: View individual employer details for approval"""
	try:
		emp_id = request.GET.get('emp_id')
		if not emp_id:
			html = "<script>alert('Employer ID missing');window.location='/admin_view_pending_employers/';</script>"
			return HttpResponse(html)
			
		cursor = connection.cursor()
		sql1 = "SELECT * FROM tbl_emp WHERE emp_id='%s'" % (emp_id)
		cursor.execute(sql1)
		result = cursor.fetchall()
		
		list_data = []
		for row in result:
			dict_data = {
				'emp_id': row[0],
				'name': row[1],
				'gender': row[2],
				'firm_name': row[3],
				'aadhar_no': row[4],
				'dob': row[5],
				'emp_address': row[6],
				'place': row[7],
				'phone': row[8],
				'mobile': row[9],
				'email': row[10],
				'status': row[12]
			}
			list_data.append(dict_data)
		return render(request, 'admin/approve_employer_detail.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/admin_view_pending_employers/';</script>"
		return HttpResponse(html)


def admin_approve_employer(request):
	"""Admin view: Approve an employer"""
	try:
		emp_id = request.GET.get('empid')
		if not emp_id:
			html = "<script>alert('Employer ID missing');window.location='/admin_view_pending_employers/';</script>"
			return HttpResponse(html)
			
		cursor = connection.cursor()
		# Update login status to approved
		sql5 = "UPDATE tbl_login SET status='true' WHERE u_id='%s' AND user_type='employer'" % (emp_id)
		cursor.execute(sql5)
		# Update employer status
		sql7 = "UPDATE tbl_emp SET status='Active' WHERE emp_id='%s'" % (emp_id)
		cursor.execute(sql7)
		
		html = "<script>alert('Employer approved successfully!');window.location='/admin_view_pending_employers/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/admin_view_pending_employers/';</script>"
		return HttpResponse(html)


def admin_reject_employer(request):
	"""Admin view: Reject an employer"""
	try:
		emp_id = request.GET.get('empid')
		if not emp_id:
			html = "<script>alert('Employer ID missing');window.location='/admin_view_pending_employers/';</script>"
			return HttpResponse(html)
			
		cursor = connection.cursor()
		# Update login status to rejected
		sql5 = "UPDATE tbl_login SET status='reject' WHERE u_id='%s' AND user_type='employer'" % (emp_id)
		cursor.execute(sql5)
		# Update employer status
		sql7 = "UPDATE tbl_emp SET status='Rejected' WHERE emp_id='%s'" % (emp_id)
		cursor.execute(sql7)
		
		html = "<script>alert('Employer rejected successfully!');window.location='/admin_view_pending_employers/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/admin_view_pending_employers/';</script>"
		return HttpResponse(html)
	

def viewfeedbackworkerhome(request):
	"""Worker view: View feedback received from employers using ORM"""
	try:
		u_id = request.session.get('u_id')
		if not u_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
			
		# Get feedback for this worker
		# Use str(u_id) for CharField column
		feedbacks = tbl_feedback.objects.filter(worker_id=str(u_id)).order_by('-date')
		list_data = []
		
		for fb in feedbacks:
			try:
				# Get employer details
				employer = tbl_emp.objects.get(emp_id=str(fb.emp_id))
				dict_data = {
					'feedback_id': fb.feedback_id,
					'date': fb.date,
					'emp_id': fb.emp_id,
					'emp_name': employer.name,
					'firm_name': employer.firm_name,
					'feedback_title': fb.feedback_title,
					'feedback_description': fb.feedback_description
				}
				list_data.append(dict_data)
			except tbl_emp.DoesNotExist:
				# If employer doesn't exist, show ID only
				dict_data = {
					'feedback_id': fb.feedback_id,
					'date': fb.date,
					'emp_id': fb.emp_id,
					'emp_name': f"Employer #{fb.emp_id}",
					'firm_name': "N/A",
					'feedback_title': fb.feedback_title,
					'feedback_description': fb.feedback_description
				}
				list_data.append(dict_data)
				
		return render(request, 'worker/view_feedbackworkerhome.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeworker/';</script>"
		return HttpResponse(html)
		
		
		'''def viewappliedvacancy(request):
		emp_id=request.session['u_id']
		cursor=connection.cursor()
		list=[]   
		sql="select * from tbl_vacancy where emp_id='%s'" %(request.session['u_id'])
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row in result1:
			sql1="select * from tbl_workerdetails INNER JOIN tbl_worker on tbl_workerdetails.worker_id=tbl_worker.worker_id where vacancy_id='%s' and status='Active'"%(row[0])
			cursor.execute(sql1)
			result=cursor.fetchall()
			for row1 in result:
				dict={'date':row[1],'emp_id':row[2],'vacancy':row[3],'vacancy_no':row[4],'description':row[5],'worker_id':row1[0],'vacancy_id':row1[1],'qualification':row1[2],'experience':row1[3]}
				list.append(dict)
		return render(request,'view_appliedvacancy.html',{'list':list})'''
def viewmyworker_jobsheddule(request):
		emp_id = request.session.get('u_id')
		if not emp_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
		cursor=connection.cursor()
		list=[]
		sql="select * from tbl_myworker where status='fixed' and emp_id='%s'"%(emp_id)
		
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_worker where worker_id='%s'"%(row1[2])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
					list.append(dict)
		return render(request,'worker/viewmyworker_jobsheddule.html',{'list':list})
def jobsheddule1(request):
		if not request.session.get('u_id'):
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
		worker_id=request.GET.get('worker_id')
		if not worker_id:
			return HttpResponse("<script>alert('Worker ID missing');window.location='/viewmyworker_jobsheddule/';</script>")
		return render(request,'worker/jobsheddule.html',{'worker_id':worker_id})
def jobsheddule2(request):
		Emp_id=request.session.get('u_id')
		if not Emp_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
		Worker_id=request.POST['worker_id']
		Job_details=request.POST['work'] 
		Salary=request.POST['salary']
		
		Working_houres=request.POST['working_houres']
		
		cursor=connection.cursor()
		
		sql4="insert into tbl_workershedule(emp_id,worker_id,job_details,salary,time_from,working_houres)values('%s','%s','%s','%s','%s','%s')"%(Emp_id,Worker_id,Job_details,Salary,now,Working_houres) 
		cursor.execute(sql4)
		
		# Send salary notification email to worker
		try:
			# Get worker details from tbl_worker
			sql_worker = "SELECT worker_name, email FROM tbl_worker WHERE worker_id='%s'" % (Worker_id)
			cursor.execute(sql_worker)
			worker_result = cursor.fetchone()
			
			if worker_result:
				worker_name = worker_result[0]
				worker_email = worker_result[1]
				
				# Parse month and year from the date (now is in format YYYY-MM-DD)
				month_dict = {
					'01': 'January', '02': 'February', '03': 'March', '04': 'April',
					'05': 'May', '06': 'June', '07': 'July', '08': 'August',
					'09': 'September', '10': 'October', '11': 'November', '12': 'December'
				}
				month_str = now[5:7]
				year_str = now[0:4]
				month_year = f"{month_dict.get(month_str, 'Unknown')} {year_str}"
				
				# Send the salary notification email
				send_salary_notification_email(
					worker_email=worker_email,
					worker_name=worker_name,
					salary_amount=Salary,
					month_year=month_year
				)
				print(f"Salary notification email triggered for worker {worker_name}")
		except Exception as e:
			# Log the error but don't interrupt the main flow
			print(f"Error sending salary notification email: {str(e)}")
		
		html="<script>alert('successfully inserted! ');window.location='/homeemp/';</script>"
		return HttpResponse(html)

def markattendance(request):
	"""Agency marks worker attendance for a schedule entry."""
	try:
		emp_id = request.session.get('u_id')
		if not emp_id or request.session.get('user_type') != 'employer':
			return HttpResponse("<script>alert('Please login as agency first');window.location='/login/';</script>")

		shedule_id = request.GET.get('shedule_id', '').strip()
		status = request.GET.get('status', '').strip()
		if not shedule_id or status not in ['Present', 'Absent']:
			return HttpResponse("<script>alert('Invalid attendance request');window.location='/viewjobshedule/';</script>")

		try:
			schedule = tbl_workershedule.objects.get(shedule_id=int(shedule_id), emp_id=int(emp_id))
		except (tbl_workershedule.DoesNotExist, ValueError):
			return HttpResponse("<script>alert('Schedule not found');window.location='/viewjobshedule/';</script>")

		schedule.attendance = status
		schedule.save()
		return HttpResponse("<script>alert('Attendance updated');window.location='/viewjobshedule2/?worker_id=%s';</script>" % schedule.worker_id)
	except Exception as e:
		return HttpResponse(f"<script>alert('Error: {str(e)}');window.location='/viewjobshedule/';</script>")

def viewjobshedule(request):
	"""Agency view: View job schedules for assigned workers using ORM"""
	try:
		emp_id = request.session.get('u_id')
		if not emp_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
			
		# 1. Get my workers first to filter schedules
		# Use str(emp_id) for CharField column
		my_worker_ids = list(tbl_myworker.objects.filter(emp_id=str(emp_id)).values_list('worker_id', flat=True))
		
		# 2. Get schedules for these workers
		# Convert string IDs back to integers as tbl_workershedule uses IntegerField for worker_id
		worker_ids_int = [int(wid) for wid in my_worker_ids if str(wid).isdigit()]
		schedules = tbl_workershedule.objects.filter(worker_id__in=worker_ids_int).order_by('-shedule_id')
		list_data = []
		
		for shed in schedules:
			try:
				worker = tbl_worker.objects.get(worker_id=shed.worker_id)
				dict_data = {
					'shedule_id': shed.shedule_id,
					'worker_id': shed.worker_id,
					'job_details': shed.job_details, # Corrected field name
					'salary': shed.salary,
					'time_from': shed.time_from,
					'working_houres': shed.working_houres,
					'attendance': shed.attendance,
					'worker_name': worker.worker_name,
					'image': worker.image,
					'gender': worker.gender,
					'dob': worker.dob,
					'aadhar_number': worker.aadhar_number,
					'regis_date': worker.regis_date,
					'place': worker.place,
					'address': worker.address,
					'languages_known': worker.languages_known,
					'phone': worker.phone,
					'mobile': worker.mobile,
					'email': worker.email
				}
				list_data.append(dict_data)
			except tbl_worker.DoesNotExist:
				continue
				
		return render(request, 'worker/viewjobshedule.html', {'list': list_data})

	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def viewjobshedule2(request):
		emp_id = request.session.get('u_id')
		if not emp_id or request.session.get('user_type') != 'employer':
			return HttpResponse("<script>alert('Please login as agency first');window.location='/login/';</script>")
		
		worker_id = request.GET.get('worker_id', '').strip()
		if not worker_id:
			return HttpResponse("<script>alert('Worker ID missing');window.location='/viewjobshedule/';</script>")
		
		schedules = tbl_workershedule.objects.filter(worker_id=worker_id, emp_id=emp_id).order_by('-shedule_id')
		list_data = []
		for row in schedules:
			list_data.append({
				'shedule_id': row.shedule_id,
				'emp_id': row.emp_id,
				'worker_id': row.worker_id,
				'job_details': row.job_details,
				'salary': row.salary,
				'time_from': row.time_from,
				'working_houres': row.working_houres,
				'attendance': getattr(row, 'attendance', 'Pending')
			})
		
		if list_data:
			return render(request, 'worker/viewjobshedule2.html', {'list': list_data})
		return HttpResponse("<script>alert('No job sheddule added. Please give any job !!! ');window.location='/viewjobshedule/';</script>")
def deletejobshedule1(request):
		cursor=connection.cursor()
		list=[]
		sql="select * from tbl_myworker where status='fixed' and emp_id='%s'"%(request.session['u_id'])
		
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_worker where worker_id='%s'"%(row1[2])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
					list.append(dict)
		return render(request,'worker/deletejobshedule1.html',{'list':list})
def deletejobshedule2(request):
		cursor=connection.cursor()
		worker_id=request.GET['worker_id']
		#sql="select worker_id from tbl_workershedule where time_from between '%s' and '%s' and emp_id='%s'"%(time_from,time_to)
		sql="select * from tbl_workershedule where ( worker_id='%s' and time_from = '%s')"%(worker_id,now)
		#sql1="select * from tbl_feedback where feedback_id=(select max(feedback_id) from tbl_feedback where worker_id='%s') " %(worker_id)
		cursor.execute(sql)
		result=cursor.fetchall()
		list=[]
		if 	(cursor.rowcount) > 0:
			for row in result:
				dict={'shedule_id':row[0],'emp_id':row[1],'worker_id':row[2],'job_details':row[3],'salary':row[4],'time_from':row[5],'working_houres':row[6]}
				list.append(dict)
			return render(request,'worker/deletejobshedule2.html',{'list':list})
		else:
			html="<script>alert('No job sheddule added. Please give any job !!! ');window.location='/deletejobshedule1/';</script>"
			return HttpResponse(html)
def deletejobshedule3(request):
		
		cursor=connection.cursor()
		shedule_id=request.GET['shedule_id']
		sql4="delete from tbl_workershedule where shedule_id='%s'"%(shedule_id)
		cursor.execute(sql4)
		html="<script>alert('successfully deleted! ');window.location='/homeemp/';</script>"
		return HttpResponse(html)
		
		
def changepaswd1 (request):
	cursor=connection.cursor()
	username=request.GET['user']
	old=request.GET['opass']
	new=request.GET['npass']
	re=request.GET['rpass']
	sql="select * from tbl_login where u_id='%s'"%(request.session['u_id'])
	cursor.execute(sql)
	result=cursor.fetchall()
	for row in result:
		p1=row[1]
	if((p1 == old) & ( new== re)):
		sql1="update tbl_login set password='%s' where u_id='%s' and user_type='%s'"%(re,request.session['u_id'],request.session['user_type'])
		cursor.execute(sql1)
		html="<script>alert('successfully changed password! ');window.location='/login/';</script>"
	else:
		html="<script>alert('Cannot be changed! ');window.location='/login/';</script>"
	return HttpResponse(html)
def viewadminpolice(request):
	"""Admin view: List all registered police units using ORM"""
	try:
		# Keep this page accessible for legacy admin flows that may not set u_id,
		# but still block clearly non-admin logged-in users.
		session_user_type = request.session.get('user_type')
		if session_user_type and session_user_type != 'admin':
			return redirect('/login/')
			
		stations = tbl_policestation.objects.all().order_by('branch')
		list_data = []
		
		for ps in stations:
			dict_data = {
				'station_id': ps.station_id,
				'branch': ps.branch,
				'address': ps.address,
				'phone': ps.phone,
				'mobile': ps.mobile,
				'email': ps.email,
				'district': ps.district,
				'city': ps.city,
				'state': ps.state
			}
			list_data.append(dict_data)
			
		return render(request, 'admin/viewadminpolice.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeadmin/';</script>"
		return HttpResponse(html)
def viewpolice(request):
	"""View logged-in police station details only."""
	if not _ensure_police_session(request):
		return HttpResponse("<script>alert('Please login as Police Station first');window.location='/login/';</script>")

	cursor = connection.cursor()
	station_id = request.session['u_id']
	sql = "select * from tbl_policestation where station_id='%s'" % (station_id)
	list = []
	cursor.execute(sql)
	result = cursor.fetchall()
	for row in result:
		dict = {
			'station_id': row[0],
			'branch': row[1],
			'address': row[2],
			'phone': row[3],
			'mobile': row[4],
			'email': row[5],
			'district': row[6],
			'city': row[7],
			'state': row[8],
			'password': row[9],
		}
		list.append(dict)
	return render(request, 'police/viewpolice.html', {'list': list})
def editpolice1(request):
		if not _ensure_police_session(request):
			return HttpResponse("<script>alert('Please login as Police Station first');window.location='/login/';</script>")

		cursor = connection.cursor()
		station_id = request.session['u_id']
		sql = "select * from tbl_policestation where station_id='%s'" % (station_id)
		list = []
		cursor.execute(sql)
		result = cursor.fetchall()
		for row in result:
			dict = {
				'station_id': row[0],
				'branch': row[1],
				'address': row[2],
				'phone': row[3],
				'mobile': row[4],
				'email': row[5],
				'district': row[6],
				'city': row[7],
				'state': row[8],
				'password': row[9],
			}
			list.append(dict)
		return render(request, 'police/editpolice1.html', {'list': list})
def editpolice2(request):
		station = _get_logged_police_station(request)

		# Fallback for legacy links like /editpolice2/?stationid=3 where
		# session->station mapping may be stale.
		if not station:
			q_station_id = request.GET.get('stationid', '').strip()
			if q_station_id:
				station = tbl_policestation.objects.filter(station_id=q_station_id).first()
				if station:
					request.session['u_id'] = station.station_id
					request.session['user_type'] = 'police'

		if not station:
			return HttpResponse("<script>alert('Please login as Police Station first');window.location='/login/';</script>")

		station_data = {
			'station_id': station.station_id,
			'branch': station.branch,
			'address': station.address,
			'phone': station.phone,
			'mobile': station.mobile,
			'email': station.email,
			'district': station.district,
			'city': station.city,
			'state': station.state,
		}
		return render(request, 'police/editpolice2.html', {'station': station_data, 'list': [station_data]})
def editpolice3(request):
		if not _ensure_police_session(request):
			return HttpResponse("<script>alert('Please login as Police Station first');window.location='/login/';</script>")

		station_id = request.session['u_id']
		data = request.POST if request.method == 'POST' else request.GET

		Branch = data.get('branch', '').strip()
		Address = data.get('address', '').strip()
		Phone = data.get('phone', '').strip()
		Mobile = data.get('mobile', '').strip()
		Email = data.get('email', '').strip()
		District = data.get('district', '').strip()
		City = data.get('city', '').strip()
		State = data.get('state', '').strip()

		if not all([Branch, Address, Phone, Mobile, Email, District, City, State]):
			return HttpResponse("<script>alert('All fields are required');window.location='/editpolice2/';</script>")

		cursor = connection.cursor()
		sql7 = "update tbl_policestation set branch='%s',address='%s',phone='%s',mobile='%s',email='%s',district='%s',city='%s',state='%s' where station_id='%s'" % (
			Branch, Address, Phone, Mobile, Email, District, City, State, station_id
		)
		cursor.execute(sql7)
		html = "<script>alert('Successfully edited profile!');window.location='/viewpolice/';</script>"
		return HttpResponse(html)
def deletenoc1(request):
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='worker' "
		#sql="select * from tbl_login where user_type='worker' and status='true' "
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				#sql1="select * from tbl_worker where worker_id='%s'"%(row1[3])
				sql1="select * from tbl_worker where worker_id='%s'"%(row1[3])
				sql1="select * from tbl_worker where worker_id='%s' and worker_id in(select worker_id from tbl_noc)"%(row1[3])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
					list.append(dict)
		return render(request,'police/deletenoc1.html',{'list':list})
def deletenoc2(request):
		cursor=connection.cursor()
		list=[]
		worker_id=request.GET['worker_id']
		sql1="select * from tbl_noc where worker_id='%s' "%(worker_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		for row in result:
			dict={'noc_id':row[0],'worker_id':row[1],'station_id':row[2],'date':row[3],'crime':row[4],'crime_details':row[5]}
			list.append(dict)
		return render(request,'police/deletenoc2.html',{'list':list})
def deletenoc3(request):
		
		cursor=connection.cursor()
		noc_id=request.GET['noc_id']
		sql4="delete from tbl_noc where noc_id='%s'"%(noc_id)
		cursor.execute(sql4)
		html="<script>alert('successfully deleted! ');window.location='/homepolice/';</script>"
		return HttpResponse(html)
def deletevacancy1(request):
		cursor=connection.cursor()
		list=[]
		sql="select * from tbl_emp where emp_id='%s'"%(request.session['u_id'])
		
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row in result1:
			sql1="select * from tbl_vacancy where emp_id='%s'"%(row[0])
			cursor.execute(sql1)
			result=cursor.fetchall()
			for row1 in result:
				dict={'vacancy_id':row1[0],'date':row1[1],'emp_id':row1[2],'vacancy':row1[3],'vacancy_no':row1[4],'description':row1[5],'emp_id':row[0],'name':row[1],'gender':row[2],'firm_name':row[3],'aadhar_no':row[4],'dob':row[5],'emp_address':row[6],'place':row[7],'phone':row[8],'mobile':row[9],'email':row[10],'password':row[11],'status':row[12]}
				list.append(dict)
		return render(request,'agency/deletevacancy1.html',{'list':list})
def deletevacancy2(request):
		
		cursor=connection.cursor()
		vacancy_id=request.GET['vacancy_id']
		sql4="delete from tbl_vacancy where vacancy_id='%s'"%(vacancy_id)
		cursor.execute(sql4)
		html="<script>alert('successfully deleted! ');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def deletefeedback1(request):
		cursor=connection.cursor()
		list=[]
		sql1="select * from tbl_feedback INNER JOIN tbl_worker on tbl_feedback.worker_id=tbl_worker.worker_id INNER JOIN tbl_emp on tbl_feedback.emp_id=tbl_emp.emp_id where tbl_feedback.emp_id='%s'"%(request.session['u_id'])
		cursor.execute(sql1)
		result=cursor.fetchall()
		#return HttpResponse(result)
		for row1 in result:
			dict={'feedback_id':row1[0],'date':row1[1],'emp_id':row1[2],'worker_id':row1[3],'feedback_title':row1[4],'feedback_description':row1[5],'worker_name':row1[8],'gender':row1[9],'address':row1[14],'mobile':row1[16],'email':row1[17]}
			list.append(dict)
			#return HttpResponse(row1)
		return render(request,'agency/deletefeedback1.html',{'list':list})
def deletefeedback2(request):
		
		cursor=connection.cursor()
		feedback_id=request.GET['feedback_id']
		sql4="delete from tbl_feedback where feedback_id='%s'"%(feedback_id)
		cursor.execute(sql4)
		html="<script>alert('successfully deleted! ');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def view_feedbackemp(request):
		cursor=connection.cursor()
		sql="select * from tbl_myworker where  worker_id='%s'"%(request.session['u_id'])
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
			sql1="select * from tbl_emp where emp_id='%s'"%(row1[1])
			cursor.execute(sql1)
			result=cursor.fetchall()
			for row in result:
				dict={'emp_id':row[0],'name':row[1],'gender':row[2],'firm_name':row[3],'aadhar_no':row[4],'dob':row[5],'emp_address':row[6],'place':row[7],'phone':row[8],'mobile':row[9],'email':row[10],'status':row[12]}
				list.append(dict)
		return render(request,'agency/view_feedbackemp.html',{'list':list})

def feedbackinsertworker(request):
		now=datetime.datetime.today()
		Worker_id=request.session['u_id']
		Emp_id=request.GET['emp_id']
		Feedback_title=request.GET['title'] 
		Feedback_description=request.GET['description']
		cursor=connection.cursor()
		
		sql4="insert into tbl_feedback(date,emp_id,worker_id,feedback_title,feedback_description)values('%s','%s','%s','%s','%s')"%(now,Emp_id,Worker_id,Feedback_title,Feedback_description) 
		cursor.execute(sql4)
		html="<script>alert('successfully inserted! ');window.location='/homeemp/';</script>"
		return HttpResponse(html)		
def addfeedbackworker(request):
		Emp_id=request.GET['emp_id']
		return render(request,'worker/feedbackworker.html',{'emp_id':Emp_id})	
def viewfeedbackemp(request):
		cursor=connection.cursor()
		list=[]
		sql1="select * from tbl_feedback where emp_id='%s'"%(request.session['u_id'])
		cursor.execute(sql1)
		result=cursor.fetchall()
		#return HttpResponse(result)
		for row1 in result:
			dict={'feedback_id':row1[0],'date':row1[1],'emp_id':row1[2],'worker_id':row1[3],'feedback_title':row1[4],'feedback_description':row1[5]}
			list.append(dict)
			#return HttpResponse(row1)
		return render(request,'agency/view_empfeedback.html',{'list':list})	

def perdayjob(request):
		"""Worker view: show all schedules assigned by agency."""
		u_id = request.session.get('u_id')
		if not u_id or request.session.get('user_type') != 'worker':
			return HttpResponse("<script>alert('Please login as worker first');window.location='/login/';</script>")
		
		# tbl_workershedule.worker_id is IntegerField; normalize session id safely.
		if str(u_id).isdigit():
			schedules = tbl_workershedule.objects.filter(worker_id=int(u_id)).order_by('-shedule_id')
		else:
			schedules = tbl_workershedule.objects.none()
		
		list_data = []
		for s in schedules:
			list_data.append({
				'shedule_id': s.shedule_id,
				'emp_id': s.emp_id,
				'worker_id': s.worker_id,
				'job_details': s.job_details,
				'salary': s.salary,
				'time_from': s.time_from,
				'working_houres': s.working_houres,
				'attendance': s.attendance
			})
		return render(request, 'worker/perdayjob.html', {'list': list_data})	

def my_salary(request):
	"""Worker view: monthly salary summary based on Present attendance."""
	u_id = request.session.get('u_id')
	if not u_id or request.session.get('user_type') != 'worker':
		return HttpResponse("<script>alert('Please login as worker first');window.location='/login/';</script>")

	today = datetime.date.today()
	month = int(request.GET.get('month', today.month))
	year = int(request.GET.get('year', today.year))
	month_key = f"{year}-{str(month).zfill(2)}"

	if str(u_id).isdigit():
		rows = tbl_workershedule.objects.filter(
			worker_id=int(u_id),
			attendance='Present',
			time_from__startswith=month_key
		).order_by('-shedule_id')
	else:
		rows = tbl_workershedule.objects.none()

	total_salary = sum(int(r.salary or 0) for r in rows)
	list_data = []
	for r in rows:
		list_data.append({
			'shedule_id': r.shedule_id,
			'job_details': r.job_details,
			'salary': r.salary,
			'time_from': r.time_from,
			'working_houres': r.working_houres,
			'attendance': r.attendance,
		})

	return render(request, 'worker/my_salary.html', {
		'list': list_data,
		'total_salary': total_salary,
		'month': month,
		'year': year,
		'months': range(1, 13),
		'years': range(2020, 2031),
	})
	
def viewnoc(request):
	"""View a worker's own latest NOC using ORM"""
	try:
		u_id = request.session.get('u_id')
		if not u_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
			
		# Get latest NOC for the logged-in worker
		noc = tbl_noc.objects.filter(worker_id=u_id).order_by('-noc_id').first()
		
		if noc:
			try:
				worker = tbl_worker.objects.get(worker_id=noc.worker_id)
				dict_data = {
					'noc_id': noc.noc_id,
					'worker_id': noc.worker_id,
					'station_id': noc.station_id,
					'date': noc.date,
					'crime': noc.crime,
					'crime_details': noc.crime_details,
					'image': worker.image,
					'worker_name': worker.worker_name,
					'gender': worker.gender,
					'dob': worker.dob,
					'aadhar_number': worker.aadhar_number,
					'regis_date': worker.regis_date,
					'place': worker.place,
					'address': worker.address,
					'languages_known': worker.languages_known,
					'phone': worker.phone,
					'mobile': worker.mobile,
					'email': worker.email,
					'status': worker.status
				}
				return render(request, 'police/view_noc.html', {'list': [dict_data]})
			except tbl_worker.DoesNotExist:
				html = "<script>alert('Worker profile not found for this NOC.');window.location='/homeworker/';</script>"
				return HttpResponse(html)
		else:
			html = "<script>alert('No NOC added. Please contact police station !! ');window.location='/homeworker/';</script>"
			return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeworker/';</script>"
		return HttpResponse(html)
def addcomplaint(request):
	"""List NOCs for the worker to provide a complaint context using ORM"""
	try:
		u_id = request.session.get('u_id')
		# Use ORM to fetch all NOCs for the logged-in worker
		noc_records = tbl_noc.objects.filter(worker_id=u_id)
		
		if noc_records.exists():
			list_data = []
			for row in noc_records:
				dict_data = {
					'noc_id': row.noc_id,
					'worker_id': row.worker_id,
					'station_id': row.station_id,
					'date': row.date,
					'crime': row.crime,
					'crime_details': row.crime_details
				}
				list_data.append(dict_data)
			return render(request, 'police/complaint1.html', {'list': list_data})
		else:
			html = "<script>alert('No NOC added. Please contact police station !! ');window.location='/homeworker/';</script>"
			return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeworker/';</script>"
		return HttpResponse(html)
def complaint2(request):
	"""Worker: Submit a complaint linked to a NOC using ORM"""
	try:
		u_id = request.session.get('u_id')
		if not u_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
			
		noc_id = request.GET.get('noc_id', '').strip()
		complaint_text = request.GET.get('complaint', '').strip()
		
		if not noc_id or not complaint_text:
			return HttpResponse("<script>alert('Complaint text and NOC ID are required');history.back();</script>")
		
		# Verify the NOC belongs to this worker before allowing complaint
		try:
			noc = tbl_noc.objects.get(noc_id=noc_id, worker_id=str(u_id))
		except tbl_noc.DoesNotExist:
			return HttpResponse("<script>alert('Invalid NOC reference. This NOC does not belong to you.');window.location='/addcomplaint/';</script>")
		
		# Use ORM to create complaint safely
		from Track.models import tbl_noccomplaint
		tbl_noccomplaint.objects.create(
			worker_id=str(u_id),
			noc_id=str(noc_id),
			complaint=complaint_text[:500],  # Enforce max length
			complaint_date=now
		)
		
		html = "<script>alert('Complaint submitted successfully! The police authority has been notified.');window.location='/homeworker/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error submitting complaint: {str(e)}');window.location='/addcomplaint/';</script>"
		return HttpResponse(html)

def addcomplaint3(request):
	"""Worker: Open complaint writing form for a specific NOC"""
	try:
		u_id = request.session.get('u_id')
		if not u_id:
			return HttpResponse("<script>alert('Please login first');window.location='/login/';</script>")
			
		noc_id = request.GET.get('noc_id', '')
		if not noc_id:
			return HttpResponse("<script>alert('NOC ID missing');window.location='/addcomplaint/';</script>")
		
		# Verify the NOC belongs to this worker
		try:
			noc = tbl_noc.objects.get(noc_id=noc_id, worker_id=str(u_id))
		except tbl_noc.DoesNotExist:
			return HttpResponse("<script>alert('Invalid NOC ID or you do not have access to this NOC.');window.location='/addcomplaint/';</script>")
		
		return render(request, 'police/complaint.html', {'noc_id': noc_id})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/addcomplaint/';</script>"
		return HttpResponse(html)
'''def viewcomplaints(request):
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='worker' and status='true' "
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_worker where worker_id='%s'"%(row1[3])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'worker_id':row[0],'worker_name':row[1],'gender':row[2],'dob':row[3],'aadhar_number':row[4],'regis_date':row[5],'place':row[6],'address':row[7],'languages_known':row[8],'phone':row[9],'mobile':row[10],'email':row[11]}
					list.append(dict)
		return render(request,'police/view_complaint1.html',{'list':list})
def viewcomplaints1(request):
		cursor=connection.cursor()
		list=[]
		
		sql1="select * from tbl_noccomplaint where worker_id='%s'"%(request.session['u_id'])
		cursor.execute(sql1)
		#return HttpResponse(now)
		result1=cursor.fetchall()
		if 	(cursor.rowcount) > 0:
			for row in result1:
				dict={'noc_id':row[0],'worker_id':row[1],'station_id':row[2],'date':row[3],'crime':row[4],'crime_details':row[5]}
				list.append(dict)
			return render(request,'police/view_noc.html',{'list':list})
		else:
			html="<script>alert('No NOC added. Please contact police station !! ');window.location='/homeworker/';</script>"
			return HttpResponse(html)'''
def editnoc1(request):
	"""List workers for NOC editing using ORM"""
	try:
		if not _ensure_police_session(request):
			return HttpResponse("<script>alert('Please login as Police Station first');window.location='/login/';</script>")

		# Show workers that have at least one NOC. Handle legacy string ids safely.
		raw_ids = tbl_noc.objects.values_list('worker_id', flat=True)
		noc_worker_ids_int = []
		for wid in raw_ids:
			w = str(wid or '').strip()
			if not w:
				continue
			try:
				noc_worker_ids_int.append(int(w))
			except ValueError:
				continue

		workers = tbl_worker.objects.filter(worker_id__in=noc_worker_ids_int).order_by('-worker_id')

		# Fallback: if mapping is dirty, do manual match so page never becomes blank.
		if not workers.exists():
			workers = []
			all_workers = tbl_worker.objects.all().order_by('-worker_id')
			allowed = {str(i).strip() for i in raw_ids if str(i).strip()}
			for w in all_workers:
				if str(w.worker_id) in allowed:
					workers.append(w)
		
		list_data = []
		for worker in workers:
			dict_data = {
				'worker_id': worker.worker_id,
				'image': worker.image,
				'worker_name': worker.worker_name,
				'gender': worker.gender,
				'dob': worker.dob,
				'aadhar_number': worker.aadhar_number,
				'regis_date': worker.regis_date,
				'place': worker.place,
				'address': worker.address,
				'languages_known': worker.languages_known,
				'phone': worker.phone,
				'mobile': worker.mobile,
				'email': worker.email,
				'status': worker.status
			}
			list_data.append(dict_data)
			
		return render(request, 'police/editnoc1.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homepolice/';</script>"
		return HttpResponse(html)
def editnoc2(request):
	"""List all NOCs for a specific worker for editing"""
	try:
		worker_id = (request.GET.get('worker_id') or '').strip()
		if not worker_id:
			return HttpResponse("<script>alert('Worker ID missing');window.location='/editnoc1/';</script>")

		# First try exact match with the worker_id
		noc_records = tbl_noc.objects.filter(worker_id=worker_id).order_by('-noc_id')
		
		# If no exact match, try with integer conversion
		if not noc_records.exists():
			try:
				worker_id_int = str(int(worker_id))
				noc_records = tbl_noc.objects.filter(worker_id=worker_id_int).order_by('-noc_id')
			except ValueError:
				pass
		
		# If still no match, try with all NOCs and manual comparison
		if not noc_records.exists():
			all_nocs = tbl_noc.objects.all().order_by('-noc_id')
			noc_records = []
			for noc in all_nocs:
				noc_worker_id_str = str(noc.worker_id).strip() if noc.worker_id else ''
				if noc_worker_id_str == worker_id or noc_worker_id_str == str(worker_id).strip():
					noc_records.append(noc)
		else:
			noc_records = list(noc_records)
			
		list_data = []
		for row in noc_records:
			dict_data = {
				'noc_id': row.noc_id,
				'worker_id': row.worker_id,
				'station_id': row.station_id,
				'date': row.date,
				'crime': row.crime,
				'crime_details': row.crime_details
			}
			list_data.append(dict_data)
			
		return render(request, 'police/editnoc2.html', {'list': list_data, 'worker_id': worker_id})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/viewnoc1/';</script>"
		return HttpResponse(html)

def editnoc3(request):
	"""Render edit form for a specific NOC record"""
	try:
		noc_id = (request.GET.get('noc_id') or '').strip()
		worker_id = (request.GET.get('worker_id') or '').strip()

		noc = None
		if noc_id:
			noc = tbl_noc.objects.filter(noc_id=noc_id).first()
		elif worker_id:
			# Open latest NOC for this worker directly from editnoc1 flow.
			candidates = {worker_id, worker_id.strip()}
			try:
				candidates.add(str(int(worker_id)))
			except ValueError:
				pass
			noc = tbl_noc.objects.filter(worker_id__in=list(candidates)).order_by('-noc_id').first()

		if not noc:
			html = "<script>alert('No NOC record found to edit.');window.location='/editnoc1/';</script>"
			return HttpResponse(html)

		dict_data = {
			'noc_id': noc.noc_id,
			'worker_id': noc.worker_id,
			'station_id': noc.station_id,
			'date': noc.date,
			'crime': noc.crime,
			'crime_details': noc.crime_details
		}
		return render(request, 'police/editnoc3.html', {'list': [dict_data]})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homepolice/';</script>"
		return HttpResponse(html)

def editnoc4(request):
	"""Update an existing NOC record"""
	try:
		noc_id = request.GET.get('noc_id')
		crime = request.GET.get('crime')
		crime_details = request.GET.get('crime_details')
		
		tbl_noc.objects.filter(noc_id=noc_id).update(
			date=now,
			crime=crime,
			crime_details=crime_details
		)
		
		html = "<script>alert('successfully Editted! ');window.location='/homepolice/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homepolice/';</script>"
		return HttpResponse(html)
def viewpoliceworker(request):
	"""Police view: List all workers using ORM for stability"""
	try:
		# Get all worker IDs from login table
		worker_ids = tbl_login.objects.filter(user_type='worker').values_list('u_id', flat=True)
		workers = tbl_worker.objects.filter(worker_id__in=worker_ids).order_by('worker_id')
		
		list_data = []
		for worker in workers:
			dict_data = {
				'worker_id': worker.worker_id,
				'image': worker.image,
				'worker_name': worker.worker_name,
				'gender': worker.gender,
				'dob': worker.dob,
				'aadhar_number': worker.aadhar_number,
				'regis_date': worker.regis_date,
				'place': worker.place,
				'address': worker.address,
				'languages_known': worker.languages_known,
				'phone': worker.phone,
				'mobile': worker.mobile,
				'email': worker.email,
				'status': worker.status
			}
			list_data.append(dict_data)
		return render(request, 'police/view_police_worker.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homepolice/';</script>"
		return HttpResponse(html)
def viewfeedbackworker1(request):
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='employer' and status='true'"
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_emp where emp_id='%s'"%(row1[3])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'emp_id':row[0],'name':row[1],'gender':row[2],'firm_name':row[3],'aadhar_no':row[4],'dob':row[5],'emp_address':row[6],'place':row[7],'phone':row[8],'mobile':row[9],'email':row[10],'password':row[11],'status':row[12]}
					list.append(dict)
		return render(request,'worker/viewfeedbackworker1.html',{'list':list})
def viewfeedbackworker2(request):
		cursor=connection.cursor()
		list=[]
		emp_id=request.GET['emp_id']
		sql1="select * from tbl_myworker where emp_id='%s' "%(emp_id)
		cursor.execute(sql1)
		result1=cursor.fetchall()
		if 	(cursor.rowcount) > 0:
			for row1 in result1:
				sql1="select * from tbl_worker where worker_id='%s'"%(row1[2])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'paswd':row[13],'status':row[14]}
					list.append(dict)
			return render(request,'worker/viewfeedbackworker2.html',{'list':list})
		else:
				html="<script>alert('No workers added. ');window.location='/viewfeedbackworker1/';</script>"
		return HttpResponse(html)
def viewfeedbackworker3(request):
		cursor=connection.cursor()
		list=[]
		worker_id=request.GET['worker_id']
		sql1="select * from tbl_feedback where worker_id='%s' "%(worker_id)
		cursor.execute(sql1)
		result1=cursor.fetchall()
		if 	(cursor.rowcount) > 0:
			for row in result1:
				dict={'feedback_id':row[0],'date':row[1],'emp_id':row[2],'worker_id':row[3],'feedback_title':row[4],'feedback_description':row[5]}
				list.append(dict)
			return render(request,'worker/viewfeedbackworker3.html',{'list':list})
		else:
				html="<script>alert('No Feedback added. ');window.location='/viewfeedbackworker1/';</script>"
		return HttpResponse(html)
def viewworkercomplaint(request):
	"""View complaints filed against workers (Police View) using ORM"""
	try:
		station_id = request.session.get('u_id')
		# 1. Get all NOCs issued by this police station
		station_nocs = tbl_noc.objects.filter(station_id=station_id)
		noc_ids = [str(n.noc_id) for n in station_nocs]
		
		# 2. Get complaints filed against those specific NOCs
		complaints = tbl_noccomplaint.objects.filter(noc_id__in=noc_ids)
		
		list_data = []
		for comp in complaints:
			try:
				# Fetch related details for the dictionary
				noc = tbl_noc.objects.get(noc_id=comp.noc_id)
				worker = tbl_worker.objects.get(worker_id=comp.worker_id)
				
				dict_data = {
					'image': worker.image,
					'worker_name': worker.worker_name,
					'aadhar_number': worker.aadhar_number,
					'mobile': worker.mobile,
					'date': noc.date,
					'crime': noc.crime,
					'crime_details': noc.crime_details,
					'complaint': comp.complaint,
					'complaint_date': comp.complaint_date
				}
				list_data.append(dict_data)
			except (tbl_noc.DoesNotExist, tbl_worker.DoesNotExist):
				continue
				
		return render(request, 'police/view_noccomplaint.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homepolice/';</script>"
		return HttpResponse(html)
def insurencejoin1(request):
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='worker' and u_id='%s'"%(request.session['u_id'])
		list=[]
		cursor.execute(sql)
		result=cursor.fetchall()
		for row in result:
			sql1="select * from tbl_worker where worker_id='%s'"%(row[3])
			cursor.execute(sql1)
			result1=cursor.fetchall()
			for row1 in result1:
				dict={'worker_id':row[0]}
				list.append(dict)
		return render(request,'insurance/insurencejoin.html',{'list':'list'})
		
def insurencejoin2(request):
		worker_id=request.GET['worker_id']
		emp_id=request.session['emp_id']
		myworker_id=request.session['myworker_id']
		Insurence_type=request.GET['insurence_type']
		Insurence_period=request.GET['period']
		Insurence_rupee=request.GET['insurence_rupee']
		Currently_insured=reqest.GET['insured']
		Details=request.GET['details']
		Nominee_name=request.GET['name']
		cursor=connection.cursor()
		sql="insert into tbl_insurence(worker_id,emp_id,myworker_id,date,insurence_type,insurence_period,insurence_rupee,currently_insured,details,nominee_name)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(worker_id,emp_id,myworker_id,now,Insurence_type,Insurence_period,Insurence_rupee,Currently_insured,Details,Nominee_name)
		cursor.execute(sql)
		html="<script>alert('Thank you for requesting information about our insurance services. One of our experienced agents will be in contact with you shortly to discuss your needs and options.If you need immediate assistance, please give us a call 619-758-9696.');window.location='/home_worker/';</script>"
		return HttpResponse(html)
def view_workershedduledetails1(request):
		return render(request,'worker/workersheddule1.html')
def workersheddule2(request):
		cursor=connection.cursor()
		time_from=request.GET['start']
		time_to=request.GET['end']
		#sql="select worker_id from tbl_workershedule where time_from between '%s' and '%s' and emp_id='%s'"%(time_from,time_to)
		sql="select * from tbl_workershedule where time_from between '%s' and '%s' "%(time_from,time_to)
		cursor.execute(sql)
		list=[]
		result=cursor.fetchall()
		for row in result:
			sql1="select * from tbl_worker where worker_id='%s'" %(row[2])
			cursor.execute(sql1)
			result1=cursor.fetchall()
			for row1 in result1:
				dict={'shedule_id':row[0],'emp_id':row[1],'worker_id':row[2],'job_details':row[3],'salary':row[4],'time_from':row[5],'working_houres':row[6],'worker_id':row1[0],'image':row1[1],'worker_name':row1[2],'gender':row1[3],'dob':row1[4],'aadhar_number':row1[5],'regis_date':row1[6],'place':row1[7],'address':row1[8],'languages_known':row1[9],'phone':row1[10],'mobile':row1[11],'email':row1[12]}
				list.append(dict)
		return render(request,'worker/workersheddule2.html',{'list':list})
def idcard(request):
		cursor=connection.cursor()
		sql="select * from tbl_worker where worker_id='%s'"%(request.session['u_id']) 
		#sql="select * from tbl_worker INNER JOIN tbl_noc on tbl_worker.worker_id=tbl_noc.worker_id INNER JOIN tbl_myworker on tbl_myworker.worker_id=tbl_worker.worker_id INNER JOIN tbl_emp on tbl_myworker.emp_id=tbl_emp.emp_id where tbl_worker.worker_id='%s' "%(request.session['u_id'])
		cursor.execute(sql)
		worker=[]
		result=cursor.fetchall()
		#return HttpResponse(result)
		for row in result:
			#dict={'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'paswd':row[13],'status':row[14],'date':row[18],'crime':row[19],'crime_details':row[20],'name':row[28],'gender':row[29],'firm_name':row[30],'emp_address':row[33],'place':row[34],'phone':row[35],'mobile':row[36],'email':row[37]}
			wo={'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'paswd':row[13],'status':row[14]}
			worker.append(wo)
		noc=[]
		sql2="select * from tbl_noc where worker_id='%s'"%(request.session['u_id'])
		cursor.execute(sql2)
		result2=cursor.fetchall()
		for row2 in result2:
			no={'date':row2[3],'crime':row2[4],'crime_details':row2[5]}
			noc.append(no)
		list=[]
		sql3="select * from tbl_emp INNER JOIN tbl_myworker on  tbl_myworker.emp_id=tbl_emp.emp_id where tbl_myworker.worker_id='%s'"%(request.session['u_id'])
		cursor.execute(sql3)
		result3=cursor.fetchall()
		for row3 in result3:
			emp={'name':row3[1],'gender':row3[2],'firm_name':row3[3],'emp_address':row3[6],'place':row3[7],'phone':row3[8],'mobile':row3[9],'email':row3[10]}
			list.append(emp)
		return render(request,'common/idcard2.html',{'worker':worker,'noc':noc,'list':list})
def searchvaccancy(request):
	"""Search vacancies with proper template and ORM"""
	try:
		# Check session
		if 'u_id' not in request.session:
			html = "<script>alert('Please login first');window.location='/login/';</script>"
			return HttpResponse(html)
		
		search = request.GET.get('search1', '')
		
		# Use ORM to get all vacancies
		if search:
			vacancies = tbl_vacancy.objects.filter(vacancy__icontains=search)
		else:
			vacancies = tbl_vacancy.objects.all()
		
		list_data = []
		for vacancy in vacancies:
			dict_data = {
				'vacancy_id': vacancy.vacancy_id,
				'date': vacancy.date,
				'emp_id': vacancy.emp_id,
				'vacancy': vacancy.vacancy,
				'vacancy_no': vacancy.vacancy_no,
				'description': vacancy.description,
				'place': vacancy.place
			}
			list_data.append(dict_data)
		
		return render(request, 'agency/searchvaccancy.html', {'list': list_data})
		
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
		return HttpResponse(html)

def view1(request):
	search=request.GET.get('search1')
	cursor = connection.cursor()
	e="select * from tbl_vacancy where  vacancy LIKE '%s%%'" % (search)
	cursor.execute(e)
	result = cursor.fetchall()
	list = []
	for row in result:
		w = {'vacancy_id': row[0], 'date': row[1], 'emp_id': row[2], 'vacancy': row[3], 'vacancy_no': row[4] ,'description': row[5], 'status': row[4]}
		list.append(w)
	return render(request,'common/table123.html', {'list': list})
def view2(request):
	"""Search workers using ORM for reliable filtering and indexing"""
	try:
		search = request.GET.get('search1', '')
		if search:
			workers = tbl_worker.objects.filter(worker_name__icontains=search).order_by('worker_id')
		else:
			workers = tbl_worker.objects.all().order_by('worker_id')
			
		list_data = []
		for row in workers:
			dict_data = {
				'worker_id': row.worker_id,
				'image': row.image,
				'worker_name': row.worker_name,
				'gender': row.gender,
				'dob': row.dob,
				'aadhar_number': row.aadhar_number,
				'regis_date': row.regis_date,
				'place': row.place,
				'address': row.address,
				'languages_known': row.languages_known,
				'phone': row.phone,
				'mobile': row.mobile,
				'email': row.email,
				'status': row.status
			}
			list_data.append(dict_data)
		return render(request, 'common/table1234.html', {'list': list_data})
	except Exception as e:
		return HttpResponse(f"Search error: {str(e)}")
def forgot_password(request):
	"""Forgot password: reset password using only email + new password (no old password needed)."""
	if request.method == 'POST':
		username = request.POST.get('user', '').strip()
		npass = request.POST.get('npass', '').strip()
		rpass = request.POST.get('rpass', '').strip()

		if not username or not npass or not rpass:
			return render(request, 'common/forgotpassword.html', {
				'message': 'All fields are required.',
				'message_type': 'error'
			})

		if npass != rpass:
			return render(request, 'common/forgotpassword.html', {
				'message': 'New passwords do not match. Please try again.',
				'message_type': 'error'
			})

		if len(npass) < 6:
			return render(request, 'common/forgotpassword.html', {
				'message': 'Password must be at least 6 characters long.',
				'message_type': 'error'
			})

		# Check if email/username exists in tbl_login
		try:
			login_record = tbl_login.objects.get(username=username)
		except tbl_login.DoesNotExist:
			return render(request, 'common/forgotpassword.html', {
				'message': 'No account found with that email/username.',
				'message_type': 'error'
			})

		# Update password in tbl_login
		login_record.password = npass
		login_record.save()

		# Also update password in the respective user table
		user_type = login_record.user_type
		u_id = login_record.u_id
		try:
			if user_type == 'worker':
				tbl_worker.objects.filter(worker_id=u_id).update(paswd=npass)
			elif user_type == 'employer':
				tbl_emp.objects.filter(emp_id=u_id).update(pswd=npass)
			elif user_type == 'police':
				tbl_policestation.objects.filter(station_id=u_id).update(password=npass)
		except Exception:
			pass  # Login password already updated; profile table update is secondary

		return render(request, 'common/forgotpassword.html', {
			'message': 'Password reset successfully! You can now login with your new password.',
			'message_type': 'success'
		})

	# GET request — show the form
	return render(request, 'common/forgotpassword.html', {})

def changepassword (request):
	cursor=connection.cursor()
	username=request.GET['user']
	old=request.GET['opass']
	new=request.GET['npass']
	re=request.GET['rpass']
	sql="select * from tbl_login where username='%s' and u_id='%s' and user_type='%s' "%(username,request.session['u_id'],request.session['user_type'])
	cursor.execute(sql)
	result=cursor.fetchall()
	#return HttpResponse(result)
	if 	(cursor.rowcount) > 0:
		for row in result:
			p1=row[1]
		if((p1 == old) & ( new== re)):
			sql1="update tbl_login set password='%s' where u_id='%s' and user_type='%s'"%(re,request.session['u_id'],request.session['user_type'])
			cursor.execute(sql1)
			html="<script>alert('successfully changed password! ');window.location='/home/';</script>"
		else:
			if(request.session['user_type']=='employer'):
				html="<script>alert('Cannot be changed!  ');window.location='/emphome/';</script>"
			elif (request.session['user_type']=='police'):
				html="<script>alert('Cannot be changed! ');window.location='/policehome/';</script>"
			elif (request.session['user_type']=='worker'):
				html="<script>alert('Cannot be changed! ');window.location='/workerhome/';</script>"
	else:
		if(request.session['user_type']=='employer'):
			html="<script>alert('Cannot be changed!  ');window.location='/emphome/';</script>"
		elif (request.session['user_type']=='police'):
			html="<script>alert('Cannot be changed! ');window.location='/policehome/';</script>"
		elif (request.session['user_type']=='worker'):
			html="<script>alert('Cannot be changed! ');window.location='/workerhome/';</script>"
	return HttpResponse(html)

def vacancy_search(request):
	search=request.GET.get('search', '')
	cursor = connection.cursor()
	if search:
		e="select * from tbl_vacancy where vacancy LIKE '%%%s%%'" % (search)
		cursor.execute(e)
	else:
		e="select * from tbl_vacancy"
		cursor.execute(e)
	result = cursor.fetchall()
	list = []
	for row in result:
		w = {'vacancy_id': row[0], 'date': row[1], 'emp_id': row[2], 'vacancy': row[3], 'vacancy_no': row[4] ,'description': row[5], 'status': row[4]}
		list.append(w)
	return render(request,'worker/vacancy_search.html', {'list': list})
def landing(request):
	return render(request,'common/landing.html')
