from flask import Flask,request,render_template,url_for,redirect,\
make_response,session,flash
from flask_sqlalchemy import SQLAlchemy

from forms import StudentForm
from UserModule import User,UserList,is_auth
from students import Student,StudentList,get_student_by_email

app = Flask('__name__')
app.secret_key="flask-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.sqlite3'
db = SQLAlchemy(app=app)
app.app_context().push()


class Student(db.Model):
    id = db.Column('student_id', db.Integer,primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    age = db.Column(db.Integer)

    def __init__(self,first_name,last_name,email,age,phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.age = age


@app.route('/')
def home():
    #if session['username']:
        #return 'hello'+' '+session['username']
    #return 'hello guest'
     response = make_response(render_template('home.html'))
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
     if request.method == 'POST':
          first_name = request.form['first_name']
          last_name = request.form['last_name']
          email = request.form['email']
          phone = request.form['phone']
          age = request.form['age']
          student = Student(first_name,last_name,email,phone,age)
          db.session.add(student) 
          db.session.commit() 
          return redirect(url_for('students_list'))
     else:
          student = request.args
          form = StudentForm(student)
          return render_template('student.html',form=form)

@app.route('/studentDetails/<id>',methods=['GET','POST'])
def student_details(id):
     student = Student.query.get(id)
     if request.method == 'POST':
          form = request.form
          student.first_name = form['first_name']
          student.last_name = form['last_name']
          student.email = form['email']
          student.phone = form['phone']
          student.age = form['age']
          db.session.commit() 
          return redirect(url_for('students_list'))

     return render_template('student_update',form = StudentForm(obj=student))



@app.route('/students_list')
def students_list():
     students_list = Student.query.all()
     return render_template('students_list.html',students_list=students_list)

@app.route('/search/<name>',methods=['POST','GET'])
def search_name(name):
     if request.method == 'POST':
          name = request.form['name']
          students_list = Student.query.filter(Student.first_name == name)
          return render_template('students_list.html',students_list=students_list)
     elif request.method == 'GET':
          students_list = Student.query.filter(Student.first_name == name)
          return render_template('students_list.html',students_list=students_list) 

@app.route('/studentUpdate/<id>',methods=['GET','POST'])
def student_update(id):
     student = Student.query.get(id)
     form = StudentForm(obj = student)
     if request.method == 'POST':
          student.first_name = request.form['first_name']
          student.last_name = request.form['last_name']
          student.email = request.form['email']
          student.phone = request.form['phone']
          student.age = request.form['age']
          db.session.commit() 
          return render_template('student_update.html',form=form)
     
     elif request.method == 'GET':
          return render_template('student_update.html',form=form)

     
@app.route('/studentDelete/<id>',methods=['POST'])   
def student_delete(id):
     student = Student.query.get(id)
     db.session.delete(student)
     db.session.commit()
     return redirect(url_for('students_list'))

     

app.add_url_rule('/register','register',register,methods=['GET','POST'])
#db.create_all()

if __name__ == "__main__":
     app.run(debug=True)  





