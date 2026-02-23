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
from Track.models import (
    tbl_worker, tbl_login, tbl_admin, tbl_emp, 
    tbl_policestation, tbl_vacancy, tbl_myworker, tbl_noc
)
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from datetime import date
from django.db import IntegrityError
now=str(date.today())

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
				return render(request, 'admin/home_admin.html')
			elif user_type == 'employer':
				return render(request, 'agency/home_emp.html')
			elif user_type == 'police':
				return render(request, 'police/home_police.html')
			elif user_type == 'worker':
				return render(request, 'worker/home_worker.html')
			else:
				html = "<script>alert('Invalid user type');window.location='/login/';</script>"
				return HttpResponse(html)
		else:
			html = "<script>alert('Invalid username or password');window.location='/login/';</script>"
			return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Login error: {str(e)}');window.location='/login/';</script>"
		return HttpResponse(html)
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
	"""Register employee/agency using ORM"""
	try:
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
		
		# Validate inputs
		if not all([name, email_id, password, re_password]):
			html = "<script>alert('Required fields missing');window.location='/reg_emp/';</script>"
			return HttpResponse(html)
		
		# Check password match
		if password != re_password:
			html = "<script>alert('Passwords do not match');window.location='/reg_emp/';</script>"
			return HttpResponse(html)
		
		# Check if email already registered
		if tbl_login.objects.filter(username=email_id).exists():
			html = "<script>alert('Email already registered');window.location='/reg_emp/';</script>"
			return HttpResponse(html)
		
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
	"""Register police station using ORM"""
	try:
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
		
		# Validate inputs
		if not all([branch, email_id, password, re_password]):
			html = "<script>alert('Required fields missing');window.location='/reg_police/';</script>"
			return HttpResponse(html)
		
		# Check password match
		if password != re_password:
			html = "<script>alert('Passwords do not match');window.location='/reg_police/';</script>"
			return HttpResponse(html)
		
		# Check if email already registered
		if tbl_login.objects.filter(username=email_id).exists():
			html = "<script>alert('Email already registered');window.location='/reg_police/';</script>"
			return HttpResponse(html)
		
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
    if request.method == "POST":
        form = WorkerForm(request.POST, request.FILES)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['paswd']

            # Check email already exists
            if tbl_login.objects.filter(username=email).exists():
                return HttpResponse(
                    "<script>alert('Email already registered');window.location='/reg_worker/';</script>"
                )

            # Save worker
            worker = form.save(commit=False)
            worker.regis_date = str(date.today())   # ✅ FIXED
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

        else:
            # 🔥 THIS LINE WILL SHOW THE REAL PROBLEM
            print("FORM ERRORS =>", form.errors)

            return HttpResponse(
                "<script>alert('Form validation failed');window.location='/reg_worker/';</script>"
            )

    return render(request, 'common/reg_worker.html', {'form': WorkerForm()})
		
def vacancyinsert(request):
	"""Insert vacancy using ORM"""
	try:
		if 'u_id' not in request.session:
			html = "<script>alert('Please login first');window.location='/login/';</script>"
			return HttpResponse(html)
		
		emp_id = request.session['u_id']
		vacancy = request.GET.get('vacancy', '').strip()
		vacancy_num = request.GET.get('num', '').strip()
		description = request.GET.get('description', '').strip()
		
		if not all([vacancy, vacancy_num, description]):
			html = "<script>alert('All fields are required');window.location='/homeemp/';</script>"
			return HttpResponse(html)
		
		tbl_vacancy.objects.create(
			date=now,
			emp_id=str(emp_id),
			vacancy=vacancy,
			vacancy_no=vacancy_num,
			description=description
		)
		
		html = "<script>alert('Vacancy created successfully!');window.location='/homeemp/';</script>"
		return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeemp/';</script>"
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
	worker_id=request.GET['worker_id']
	return render(request,'police/noc.html',{'worker_id':worker_id})
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
		return render(request,'worker/addworkerdetails.html',{'vacancy_id':vacancy_id})
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
	cursor=connection.cursor()
	list=[]
	sql="select * from tbl_login where user_type='worker' and status='false'"
	cursor.execute(sql)
	result1=cursor.fetchall()
	for row1 in result1:
		sql6="select * from tbl_worker where worker_id='%s'"%(row1[3])
		cursor.execute(sql6)
		result=cursor.fetchall()
		for row in result:
			dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
			list.append(dict)
	return render(request,'police/viewworkeraccept.html',{'list':list})
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
		cursor=connection.cursor()
		worker_id=request.GET['worker_id']
		sql1="select * from tbl_worker where worker_id='%s'" %(worker_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		list=[]
		for row in result:
			dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
			list.append(dict)
		return render(request,'worker/view_individual_worker.html',{'list':list})
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
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='employer' and u_id='%s'"%(request.session['u_id'])
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
		return render(request,'agency/edit_view_emp.html',{'list':list})
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
		cursor=connection.cursor()
		list=[]
		
		sql1="select * from tbl_workerdetails"
		cursor.execute(sql1)
		result=cursor.fetchall()
		for row1 in result:
			dict={'worker_id':row1[0],'vacancy_id':row1[1],'qualification':row1[2],'experience':row1[3]}
			list.append(dict)
		return render(request,'worker/view_shedduled_workerdetails.html',{'list':list})
def viewworker(request):
		cursor=connection.cursor()
		worker_id=request.GET['worker_id']
		list=[]
		sql1="select * from tbl_worker where worker_id='%s'"%(worker_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		for row1 in result:
			dict={'worker_id':row1[0],'name':row1[1],'gender':row1[2],'dob':row1[3],'aadhar_number':row1[4],'regis_date':row1[5],'place':row1[6],'address':row1[7],'languages_known':row1[8],'phone':row1[9],'mobile':row1[10],'email':row1[11]}
			list.append(dict)
		return render(request,'worker/viewsheduledworker2.html',{'list':list})
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
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='employer' and u_id='%s'"%(request.session['u_id'])
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
		return render(request,'agency/view_mydetails.html',{'list':list})
def viewempworker(request):
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
		return render(request,'agency/view_empworker.html',{'list':list})
def viewnoc1(request):
		cursor=connection.cursor()
		
		#sql="select * from tbl_login where user_type='worker' and status='true' "
		sql="select * from tbl_login where user_type='worker' "
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				#sql1="select * from tbl_worker where worker_id='%s'"%(row1[3])
				sql1="select * from tbl_worker where worker_id='%s'"%(row1[3])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
					list.append(dict)
		return render(request,'police/view_noc1.html',{'list':list})
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
def view_feedbackworker(request):
		cursor=connection.cursor()
		sql="select * from tbl_myworker where status='fixed' and emp_id='%s'"%(request.session['u_id'])
		list=[]
		male_count = 0
		female_count = 0
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_worker where worker_id='%s'"%(row1[2])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					gender = row[3]
					# Count male and female workers
					if gender.lower() == 'male':
						male_count += 1
					elif gender.lower() == 'female':
						female_count += 1
					dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
					list.append(dict)
		return render(request,'worker/view_feedbackworker.html',{'list':list, 'male_count': male_count, 'female_count': female_count})

def viewvacancy(request):
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
		return render(request,'agency/view_vacancy2.html',{'list':list})
def editvacancy1(request):
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
		return render(request,'agency/edit_vacancy1.html',{'list':list})
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
	"""View applied workers for employer's vacancies"""
	try:
		emp_id = request.session.get('u_id')
		if not emp_id:
			html = "<script>alert('Please login first');window.location='/login/';</script>"
			return HttpResponse(html)
		
		cursor = connection.cursor()
		list_data = []
		
		# Get all vacancies created by this employer
		sql = "SELECT vacancy_id, date, vacancy, vacancy_no, description, emp_id FROM tbl_vacancy WHERE emp_id='%s'" % (emp_id)
		cursor.execute(sql)
		result1 = cursor.fetchall()
		
		for row in result1:
			vacancy_id = row[0]
			# Get workers who applied to this vacancy (from tbl_workerdetails)
			# Join with tbl_worker to get worker details and filter by status='Active'
			sql1 = """
				SELECT wd.worker_id, wd.vacancy_id, wd.qualification, wd.experience,
					   w.worker_name, w.gender, w.dob, w.aadhar_number, w.place, w.address, 
					   w.phone, w.mobile, w.email, w.status
				FROM tbl_workerdetails wd
				INNER JOIN tbl_worker w ON wd.worker_id = w.worker_id
WHERE wd.vacancy_id='%s'
			""" % (vacancy_id)
			cursor.execute(sql1)
			result = cursor.fetchall()
			
			for row1 in result:
				dict_data = {
					'date': row[1],
					'vacancy': row[2],
					'vacancy_no': row[3],
					'description': row[4],
					'worker_id': row1[0],
					'vacancy_id': row1[1],
					'qualification': row1[2],
					'experience': row1[3],
					'worker_name': row1[4],
					'gender': row1[5],
					'dob': row1[6],
					'aadhar_number': row1[7],
					'place': row1[8],
					'address': row1[9],
					'phone': row1[10],
					'mobile': row1[11],
					'email': row1[12],
					'status': row1[13]
				}
				list_data.append(dict_data)
		
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
		v_id=request.GET['vacid']
		w_id=request.GET['worid']
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
def editfeedbackworker1(request):
		cursor=connection.cursor()
		sql="select * from tbl_myworker where status='fixed' and emp_id='%s'"%(request.session['u_id'])
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_worker where worker_id='%s'"%(row1[2])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12]}
					list.append(dict)
		return render(request,'worker/editfeedbackworker1.html',{'list':list})
		
		
def editfeedbackworker2(request):
		cursor=connection.cursor()
		worker_id=request.GET['worker_id']
		sql1="select * from tbl_feedback where feedback_id=(select max(feedback_id) from tbl_feedback where worker_id='%s') " %(worker_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		list=[]
		if 	(cursor.rowcount) > 0:
			for row1 in result:
				dict={'feedback_id':row1[0],'date':row1[1],'emp_id':row1[2],'worker_id':row1[3],'feedback_title':row1[4],'feedback_description':row1[5]}
				list.append(dict)
			return render(request,'worker/edit_feedbackworker2.html',{'list':list})
		else:
			html="<script>alert('No feedback added. Please add your feedback about this worker!!! ');window.location='/editfeedbackworker1/';</script>"
			return HttpResponse(html)
def editfeedbackworker3(request):
		
		feedback_id=request.GET['feedbackid']
		#now=datetime.datetime.today()
		
		Feedback_title=request.GET['feedback_title'] 
		Feedback_description=request.GET['des']
		
		cursor=connection.cursor()
	
		sql7="update tbl_feedback set date='%s',feedback_title='%s',feedback_description='%s' where feedback_id='%s'" %(now,Feedback_title,Feedback_description,feedback_id)
		cursor.execute(sql7)
		html="<script>alert('successfully Editted!');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def viewemydetailsworker(request):
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='worker' and u_id='%s'"%(request.session['u_id'])
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_worker where worker_id='%s'"%(row1[3])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12]}
					list.append(dict)
		return render(request,'worker/view_mydetailsworker.html',{'list':list})

def worker_profile(request):
	"""Display worker profile view - used for cancel button in edit profile"""
	cursor=connection.cursor()
	sql="select * from tbl_login where user_type='worker' and u_id='%s'"%(request.session['u_id'])
	list=[]
	cursor.execute(sql)
	result1=cursor.fetchall()
	for row1 in result1:
		sql1="select * from tbl_worker where worker_id='%s'"%(row1[3])
		cursor.execute(sql1)
		result=cursor.fetchall()
		for row in result:
			dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[6],'regis_date':row[7],'place':row[8],'address':row[9],'languages_known':row[10],'phone':row[11],'mobile':row[12],'email':row[13],'status':row[15]}
			list.append(dict)
	return render(request,'worker/worker_profile.html',{'worker':list[0] if list else None})
def viewmyworker(request):
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
					dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12]}
					list.append(dict)
		return render(request,'worker/view_myworker.html',{'list':list})
def viewfeedback(request):
		cursor=connection.cursor()
		list=[]
		sql1="select * from tbl_feedback INNER JOIN tbl_worker on tbl_feedback.worker_id=tbl_worker.worker_id INNER JOIN tbl_emp on tbl_feedback.emp_id=tbl_emp.emp_id where tbl_feedback.emp_id='%s'"%(request.session['u_id'])
		cursor.execute(sql1)
		result=cursor.fetchall()
		#return HttpResponse(result)
		for row1 in result:
			dict={'feedback_id':row1[0],'date':row1[1],'emp_id':row1[2],'worker_id':row1[3],'feedback_title':row1[4],'feedback_description':row1[5],'image':row1[7],'worker_name':row1[8],'gender':row1[9],'address':row1[14],'mobile':row1[16],'email':row1[17]}
			list.append(dict)
			#return HttpResponse(row1)
		#return HttpResponse(list)
		return render(request,'agency/view_feedback.html',{'list':list})
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
		cursor=connection.cursor()
		list=[]
		sql1="select * from tbl_worker "
		cursor.execute(sql1)
		result=cursor.fetchall()
		for row in result:
			dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
			list.append(dict)
		return render(request,'admin/view_adminworker.html',{'list':list})
def editadminworker(request):
		cursor=connection.cursor()
		list=[]
		sql1="select * from tbl_worker "
		cursor.execute(sql1)
		result=cursor.fetchall()
		for row in result:
					dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
					list.append(dict)
		return render(request,'admin/edit_adminworker.html',{'list':list})
def editadminworker2(request):
		cursor=connection.cursor()
		worker_id=request.GET['worker_id']
		sql1="select * from tbl_worker where worker_id='%s'" %(worker_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		list=[]
		for row in result:
			dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
			list.append(dict)
		return render(request,'admin/edit_adminworker2.html',{'list':list})
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
	"""Admin view: List all pending employer registrations"""
	try:
		cursor = connection.cursor()
		# Get employers with status='false' (pending) or not yet approved
		sql = "SELECT * FROM tbl_login WHERE user_type='employer' AND status='false'"
		cursor.execute(sql)
		result1 = cursor.fetchall()
		
		list_data = []
		for row1 in result1:
			sql1 = "SELECT * FROM tbl_emp WHERE emp_id='%s'" % (row1[3])
			cursor.execute(sql1)
			result = cursor.fetchall()
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
		return render(request, 'admin/approve_employer.html', {'list': list_data})
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/homeadmin/';</script>"
		return HttpResponse(html)


def admin_view_all_employers(request):
	"""Admin view: List all employer/agency details"""
	try:
		cursor = connection.cursor()
		# Get all employers
		sql = "SELECT * FROM tbl_login WHERE user_type='employer'"
		cursor.execute(sql)
		result1 = cursor.fetchall()
		
		list_data = []
		for row1 in result1:
			sql1 = "SELECT * FROM tbl_emp WHERE emp_id='%s'" % (row1[3])
			cursor.execute(sql1)
			result = cursor.fetchall()
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
		cursor=connection.cursor()
		list=[]
		sql1="select * from tbl_feedback where worker_id='%s'"%(request.session['u_id'])
		cursor.execute(sql1)
		result1=cursor.fetchall()
		for row1 in result1:
			
			dict={'feedback_id':row1[0],'date':row1[1],'emp_id':row1[2],'worker_id':row1[3],'feedback_title':row1[4],'feedback_description':row1[5]}
			list.append(dict)
		return render(request,'worker/view_feedbackworkerhome.html',{'list':list})
		
		
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
		return render(request,'worker/viewmyworker_jobsheddule.html',{'list':list})
def jobsheddule1(request):
		worker_id=request.GET['worker_id']
		return render(request,'worker/jobsheddule.html',{'worker_id':worker_id})
def jobsheddule2(request):
		Emp_id=request.session['u_id']
		Worker_id=request.GET['worker_id']
		Job_details=request.GET['work'] 
		Salary=request.GET['salary']
		
		Working_houres=request.GET['working_houres']
		
		cursor=connection.cursor()
		
		sql4="insert into tbl_workershedule(emp_id,worker_id,job_details,salary,time_from,working_houres)values('%s','%s','%s','%s','%s','%s')"%(Emp_id,Worker_id,Job_details,Salary,now,Working_houres) 
		cursor.execute(sql4)
		html="<script>alert('successfully inserted! ');window.location='/homeemp/';</script>"
		return HttpResponse(html)
def viewjobshedule(request):
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
		return render(request,'worker/viewjobshedule.html',{'list':list})
def viewjobshedule2(request):
		cursor=connection.cursor()
		worker_id=request.GET['worker_id']
		#sql="select worker_id from tbl_workershedule where time_from between '%s' and '%s' and emp_id='%s'"%(time_from,time_to)
		sql="select * from tbl_workershedule where worker_id='%s'"%(worker_id)
		cursor.execute(sql)
		result=cursor.fetchall()
		list=[]
		if 	(cursor.rowcount) > 0:
			for row in result:
				dict={'shedule_id':row[0],'emp_id':row[1],'worker_id':row[2],'job_details':row[3],'salary':row[4],'time_from':row[5],'working_houres':row[6]}
				list.append(dict)
			return render(request,'worker/viewjobshedule2.html',{'list':list})
		else:
			html="<script>alert('No job sheddule added. Please give any job !!! ');window.location='/viewjobshedule/';</script>"
			return HttpResponse(html)
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
		cursor=connection.cursor()
		sql="select * from tbl_login where user_type='police'"
		list=[]
		cursor.execute(sql)
		result1=cursor.fetchall()
		for row1 in result1:
				sql1="select * from tbl_policestation where station_id='%s'"%(row1[3])
				cursor.execute(sql1)
				result=cursor.fetchall()
				for row in result:
					dict={'station_id':row[0],'branch':row[1],'address':row[2],'phone':row[3],'mobile':row[4],'email':row[5],'district':row[6],'city':row[7],'state':row[8],'password':row[9]}
					list.append(dict)
		return render(request,'admin/viewadminpolice.html',{'list':list})
def viewpolice(request):
	"""View all police stations - fetches all police station records"""
	cursor=connection.cursor()
	# Fetch ALL police stations from tbl_policestation table
	sql="select * from tbl_policestation"
	list=[]
	cursor.execute(sql)
	result=cursor.fetchall()
	for row in result:
		dict={'station_id':row[0],'branch':row[1],'address':row[2],'phone':row[3],'mobile':row[4],'email':row[5],'district':row[6],'city':row[7],'state':row[8],'password':row[9]}
		list.append(dict)
	return render(request,'police/viewpolice.html',{'list':list})
def editpolice1(request):
		cursor=connection.cursor()
		# Fetch ALL police stations from tbl_policestation table
		sql="select * from tbl_policestation"
		list=[]
		cursor.execute(sql)
		result=cursor.fetchall()
		for row in result:
			dict={'station_id':row[0],'branch':row[1],'address':row[2],'phone':row[3],'mobile':row[4],'email':row[5],'district':row[6],'city':row[7],'state':row[8],'password':row[9]}
			list.append(dict)
		return render(request,'police/editpolice1.html',{'list':list})
def editpolice2(request):
		cursor=connection.cursor()
		station_id=request.GET['stationid']
		sql1="select * from tbl_policestation where station_id='%s' " %(station_id)
		cursor.execute(sql1)
		result=cursor.fetchall()
		list=[]
		for row in result:
			dict={'station_id':row[0],'branch':row[1],'address':row[2],'phone':row[3],'mobile':row[4],'email':row[5],'district':row[6],'city':row[7],'state':row[8],'password':row[9]}
			list.append(dict)
		return render(request,'police/editpolice2.html',{'list':list})
def editpolice3(request):
		
		station_id=request.GET['stationid']
		
		
		Branch=request.GET['branch'] 
		Address=request.GET['address']
		
		Phone=request.GET['phone']
		Mobile=request.GET['mobile']
		Email=request.GET['email']
		District=request.GET['district']
		City=request.GET['city']
		State=request.GET['state']
		cursor=connection.cursor()
	
		sql7="update tbl_policestation set branch='%s',address='%s',phone='%s',mobile='%s',email='%s',district='%s',city='%s',state='%s' where station_id='%s'" %(Branch,Address,Phone,Mobile,Email,District,City,State,station_id)
		cursor.execute(sql7)
		html="<script>alert('successfully Editted!');window.location='/homepolice/';</script>"
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
		cursor=connection.cursor()
		list=[]
		
		sql1="select * from tbl_workershedule where worker_id='%s' and time_from='%s' "%(request.session['u_id'],now)
		cursor.execute(sql1)
		#return HttpResponse(now)
		result1=cursor.fetchall()
		for row1 in result1:
			dict={'shedule_id':row1[0],'emp_id':row1[1],'worker_id':row1[2],'job_details':row1[3],'salary':row1[4],'time_from':row1[5],'working_houres':row1[6]}
			list.append(dict)
		return render(request,'police/perdayjob.html',{'list':list})	
	
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
		#now=datetime.datetime.today()
		Worker_id=request.session['u_id']
		Noc_id=request.GET['noc_id']
		
		Complaint=request.GET['complaint'] 
		
		cursor=connection.cursor()
		
		sql4="insert into tbl_noccomplaint(worker_id,noc_id,complaint,complaint_date)values('%s','%s','%s','%s')"%(Worker_id,Noc_id,Complaint,now) 
		cursor.execute(sql4)
		html="<script>alert('successfully inserted! ');window.location='/homeworker/';</script>"
		return HttpResponse(html)
def addcomplaint3(request):
		Noc_id=request.GET['noc_id']
		return render(request,'police/complaint.html',{'noc_id':Noc_id})
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
		# Get all worker IDs from login table
		worker_ids = tbl_login.objects.filter(user_type='worker').values_list('u_id', flat=True)
		workers = tbl_worker.objects.filter(worker_id__in=worker_ids)
		
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
		worker_id = request.GET.get('worker_id')
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
			return render(request, 'police/editnoc2.html', {'list': list_data})
		else:
			html = "<script>alert('No NOC added. Please find the details and add it !! ');window.location='/viewnoc1/';</script>"
			return HttpResponse(html)
	except Exception as e:
		html = f"<script>alert('Error: {str(e)}');window.location='/viewnoc1/';</script>"
		return HttpResponse(html)

def editnoc3(request):
	"""Render edit form for a specific NOC record"""
	try:
		noc_id = request.GET.get('noc_id')
		noc = tbl_noc.objects.get(noc_id=noc_id)
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
	cursor=connection.cursor()
	list=[]
	sql="select * from tbl_login where user_type='worker'"
	cursor.execute(sql)
	result1=cursor.fetchall()
	for row1 in result1:
		sql6="select * from tbl_worker where worker_id='%s'"%(row1[3])
		cursor.execute(sql6)
		result=cursor.fetchall()
		for row in result:
			dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
			list.append(dict)
	return render(request,'police/view_police_worker.html',{'list':list})
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
	search=request.GET.get('search1')
	cursor = connection.cursor()
	e="select * from tbl_vacancy "
	cursor.execute(e)
	result = cursor.fetchall()
	list = []
	for row in result:
		w = {'vacancy_id': row[0], 'date': row[1], 'emp_id': row[2], 'vacancy': row[3], 'vacancy_no': row[4] ,'description': row[5], 'status': row[4]}
		list.append(w)
	return render(request,'common/view_users.html', {'list': list})
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
	search=request.GET.get('search1')
	cursor = connection.cursor()
	e="select * from tbl_worker where  worker_name  LIKE '%s%%'" % (search)
	cursor.execute(e)
	result = cursor.fetchall()
	list = []
	for row in result:
		w = {'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12],'status':row[14]}
		list.append(w)
	return render(request,'common/table1234.html', {'list': list})
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

		
	
	
		
	

		
		
	








