from flask import Flask,request,render_template,url_for,redirect,\
make_response,session,flash

from forms import StudentForm
from UserModule import User,UserList,is_auth
from students import Student,StudentList,get_student_by_email

app = Flask('__name__')
app.secret_key="flask-key"


@app.route('/')
def hello():
    #if session['username']:
        #return 'hello'+' '+session['username']
    #return 'hello guest'
     response = make_response(render_template('hello.html'))
     return response

@app.route('/<name>')
def hello_name(name):
    #return f'Hello {name}'
     return render_template('hello.html',content=name)

@app.route('/login',methods=['GET','POST'])
def login():
       if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if is_auth(username,password):
               #session['username'] = request.form['username']
               flash(f'{username} your are now logged in')
               return redirect(url_for('hello'))
            else:
                 return 'User Not exist'
            
       elif request.method == 'GET':
            return render_template('login.html')

       

#@app.route('/register',methods=['GET','POST'])
def register():
       if request.method == 'POST':
            user = User(username=request.form['username'],password=request.form['password'])
            UserList.append(user)
            return redirect(url_for('login'))
       elif request.method == 'GET':
            return render_template('register.html')
       
@app.route('/logout')
def logout():
     session.pop('username','')
     return redirect(url_for('login'))

@app.route('/grades',methods=['GET','POST'])       
def grades():
    if request.method == 'POST':
         grades = request.form
         return render_template('grades.html',grades=grades)
    grades = request.args
    return render_template('grades_form.html',grades=grades)

@app.route('/student',methods=['GET','POST'])
def student():
     form = StudentForm()
     if request.method == 'POST':
          first_name = request.form['first_name']
          last_name = request.form['last_name']
          email = request.form['email']
          age = request.form['age']
          phone = request.form['phone']
          #student_id = request.form['student_id']
          student = Student(first_name,last_name,email,age,phone)
          StudentList.append(student)  
          return redirect(url_for('students_list'))
          
     return render_template('student.html',form=form)

@app.route('/studentSignup',methods=['GET','POST'])
def student_signup():
     if request.method == 'GET':
          form = StudentForm(request.args)
          return render_template('student_info.html',form=form)
     elif request.method == 'POST':
          form = StudentForm(request.form)
          return render_template('student_info.html',form=form)

@app.route('/students_list')
def students_list():
     students_list = StudentList
     return render_template('students_list.html',students_list=students_list)

@app.route('/student/<mail>',methods=['GET','POST'])
def student_update(mail):
    student = get_student_by_email(mail)
    form = StudentForm(student,request.form)
    render_template(url_for('student_signup'),form=form)


    

app.add_url_rule('/register','register',register,methods=['GET','POST'])

if __name__ == "__main__":
     app.run(debug=True)  





