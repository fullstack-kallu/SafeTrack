from django.db import models

class tbl_admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    pasw = models.CharField(max_length=50)

    class Meta:
        db_table = 'tbl_admin'
        managed = True

    def __str__(self):
        return self.name


class tbl_login(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50)
    u_id = models.IntegerField()
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'tbl_login'
        managed = True


class tbl_emp(models.Model):
    emp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    firm_name = models.CharField(max_length=100)
    aadhar_no = models.CharField(max_length=20)
    dob = models.CharField(max_length=50)
    emp_address = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    pswd = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'tbl_emp'
        managed = True


class tbl_complaint(models.Model):
    cmp_id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField()
    complaint = models.CharField(max_length=500)
    cmp_date = models.CharField(max_length=50)

    class Meta:
        db_table = 'tbl_complaint'
        managed = True


class tbl_feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=50)
    emp_id = models.CharField(max_length=10)
    worker_id = models.CharField(max_length=10)
    feedback_title = models.CharField(max_length=50)
    feedback_description = models.CharField(max_length=500)

    class Meta:
        db_table = 'tbl_feedback'
        managed = True


class tbl_jobdetails(models.Model):
    job_id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField()
    job_details = models.CharField(max_length=100)

    class Meta:
        db_table = 'tbl_jobdetails'
        managed = True


class tbl_myworker(models.Model):
    myworker_id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField()
    worker_id = models.IntegerField()
    vacancy_id = models.IntegerField()
    date = models.DateField()
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'tbl_myworker'
        managed = True


class tbl_noc(models.Model):
    noc_id = models.AutoField(primary_key=True)
    worker_id = models.CharField(max_length=10)
    station_id = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    crime = models.CharField(max_length=50)
    crime_details = models.CharField(max_length=1000)

    class Meta:
        db_table = 'tbl_noc'
        managed = True


class tbl_noccomplaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    worker_id = models.CharField(max_length=10)
    noc_id = models.CharField(max_length=10)
    complaint = models.CharField(max_length=50)
    complaint_date = models.CharField(max_length=50)

    class Meta:
        db_table = 'tbl_noccomplaint'
        managed = True


class tbl_policestation(models.Model):
    station_id = models.AutoField(primary_key=True)
    branch = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'tbl_policestation'
        managed = True


class tbl_vacancy(models.Model):
    vacancy_id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=50)
    emp_id = models.CharField(max_length=150)
    vacancy = models.CharField(max_length=50)
    vacancy_no = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    place = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'tbl_vacancy'
        managed = True

class tbl_worker(models.Model):
    worker_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='workers/', blank=True, null=True)
    worker_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.CharField(max_length=50)
    age = models.IntegerField(default=0)
    aadhar_number = models.CharField(max_length=50)
    regis_date = models.CharField(max_length=50, blank=True)
    place = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    languages_known = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, blank=True)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    paswd = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Pending')

    class Meta:
        db_table = 'tbl_worker'



class tbl_workerdetails(models.Model):
    detail_id = models.AutoField(primary_key=True)
    worker_id = models.CharField(max_length=10)
    vacancy_id = models.CharField(max_length=10)
    qualification = models.CharField(max_length=50)
    experience = models.CharField(max_length=100)

    class Meta:
        db_table = 'tbl_workerdetails'
        managed = True


class tbl_workershedule(models.Model):
    shedule_id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField()
    worker_id = models.IntegerField()
    job_details = models.CharField(max_length=100)
    salary = models.IntegerField()
    time_from = models.CharField(max_length=50)
    working_houres = models.CharField(max_length=50)

    class Meta:
        db_table = 'tbl_workershedule'
        managed = True


class tbl_insurence(models.Model):
    insurence_id = models.AutoField(primary_key=True)
    worker_id = models.IntegerField()
    emp_id = models.IntegerField()
    myworker_id = models.IntegerField()
    date = models.CharField(max_length=50)
    insurence_type = models.CharField(max_length=100)
    insurence_period = models.CharField(max_length=50)
    insurence_rupee = models.DecimalField(max_digits=10, decimal_places=2)
    currently_insured = models.CharField(max_length=10)
    details = models.TextField()
    nominee_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'tbl_insurence'
        managed = True
		
		
		
		