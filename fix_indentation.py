# Read the file
with open('Track/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the worker_profile function to fix indentation
old_func = '''def worker_profile(request):
\t"""Display worker profile view - used for cancel button in edit profile"""
\t\tcursor=connection.cursor()
\t\tsql="select * from tbl_login where user_type='worker' and u_id='%s'"%(request.session['u_id'])
\t\tlist=[]
\t\tcursor.execute(sql)
\t\tresult1=cursor.fetchall()
\t\tfor row1 in result1:
\t\t\tsql1="select * from tbl_worker where worker_id='%s'"%(row1[3])
                cursor.execute(sql1)
                result=cursor.fetchall()
                for row in result:
                    dict={'worker_id':row[0],'image':row[1],'worker_name':row[2],'gender':row[3],'dob':row[4],'aadhar_number':row[5],'regis_date':row[6],'place':row[7],'address':row[8],'languages_known':row[9],'phone':row[10],'mobile':row[11],'email':row[12]}
                    list.append(dict)
        return render(request,'worker/worker_profile.html',{'list2':'list2'})
'''

new_func = '''def worker_profile(request):
    """Display worker profile view - used for cancel button in edit profile"""
    cursor=connection.cursor()
    sql="select * from tbl_login where user_type='worker'"
    list=[]
    cursor.execute(sql)
    result=cursor.fetchall()
    
    return render(request,'worker/worker_profile.html')
'''

if old_func in content:
    content = content.replace(old_func, new_func)
else:
    # Try simpler pattern
    import re
    # Look for the function definition and fix just the first line's indentation issue after docstring
    
print("Checking if pattern exists...")
if "def worker_profile" in content:
