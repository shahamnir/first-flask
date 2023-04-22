from flask import Flask,request,render_template,url_for,redirect,\
make_response,session,flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from forms import StudentForm,CourseForm
from UserModule import User,UserList,is_auth
#from students import Student,StudentList,get_student_by_email
from flask_restful import Api, Resource,fields,marshal_with
import json

app = Flask('__name__')
app.secret_key="flask-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.sqlite3'
db = SQLAlchemy(app=app)
app.app_context().push()
api = Api(app=app)




students_fields = {
    'id' : fields.Integer, 
    'first_name' : fields.String, 
    'last_name' : fields.String, 
    'email' : fields.String,  
    'age' : fields.Integer, 
    'phone' : fields.String
}


class StudentsList(Resource):
     @marshal_with(students_fields)
     def get(self):
          students = Student.query.all()
          return students
     
     @marshal_with(students_fields)
     def post(self):
          data = request.json
          first_name= data['first_name']
          last_name= data['last_name']
          email= data['email']
          age = data['age']
          phone= data['phone']
          student = Student(first_name,last_name,email,age,phone)
          db.session.add(student)
          db.session.commit()
          return student

class StudentApi(Resource):
     @marshal_with(students_fields)
     def get(self,pk):
          student = Student.query.get(pk)
          return student
     
     @marshal_with(students_fields)
     def put(self,pk):
          student = Student.query.get(pk)
          data = request.json
          student.first_name= data['first_name']
          student.last_name = data['last_name']
          student.email = data['email']
          student.phone = data['phone']
          student.age = data['age']
          db.session.commit()
          return student
     
     @marshal_with(students_fields)
     def delete(self,pk):
          student = Student.query.get(pk)
          db.session.delete(student)
          db.session.commit()
          


fake_database = {
     1:{'name':'danny'},
     2:{'name':'shalom'},
     3:{'name':'ruth'},
     }     

class Names(Resource):
     def get(self):
         return fake_database


     def post(self):
        data = request.json
        nameID = len(fake_database.keys())+1
        fake_database[nameID] = {'name':data['name']}
        return fake_database
     
class Name(Resource):
     def get(self,pk):
          return fake_database[pk]
     
     def put(self,pk):
          data = request.json
          fake_database[pk] = {'name':data['name']} 
          return fake_database[pk]
     
     def delete(self,pk):
         fake_database.pop(pk)
         return fake_database
     



courses = db.Table('Courses',
        db.Column('student_id',db.Integer, db.ForeignKey('student.student_id'),primary_key=True),
        db.Column('course_id',db.Integer, db.ForeignKey('course.course_id'),primary_key=True)
                   )

class Student(db.Model):
    id = db.Column('student_id', db.Integer,primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(100))
    courses = db.relationship('Course',secondary=courses, backref=db.backref('students', lazy=True))

    def __init__(self,first_name,last_name,email,age,phone,courses= []) -> None: 
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.phone = phone
        self.courses = courses

class Course(db.Model):
     id = db.Column('course_id',db.Integer,primary_key = True)
     name = db.Column(db.String(100))

     def __init__(self,name):
          self.name = name
          

@app.route('/')
def home():
    #if session['username']:
        #return 'hello'+' '+session['username']
    #return 'hello guest'
     response = make_response(render_template('home.html'))
     return response



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


@app.route('/courses',methods=['GET','POST'])
def courses():     
    if request.method == 'POST':
          name = request.form['name']
          course = Course(name=name)
          db.session.add(course)
          db.session.commit()
          return redirect(url_for('courses'))
    else:
          courses=Course.query.all()
          return render_template('courses.html',courses=courses)
     
@app.route('/course/<int:id>',methods=['GET','POST'])
def course(id):
     course = Course.query.get(id)
     if request.method == 'GET':
        form = CourseForm(obj=course)
        return render_template('course.html',form=form)
     
     else:
          course.name = request.form['name']
          db.session.commit()
          return redirect(url_for('courses'))
     
@app.route('/add_course')
def add_course():
     form = CourseForm()
     return render_template('course.html',form=form)

@app.route('/courses_delete',methods=['POST'])
def delete_courses():
     courses_ids = request.form.getlist('courses')
     for course_id in courses_ids:
          course = Course.query.get(course_id)
          db.session.delete(course)
     db.session.commit()
     return redirect(url_for('courses'))
 

@app.route('/student',methods=['GET','POST'])
def student():
     if request.method == 'POST':
          first_name = request.form['first_name']
          last_name = request.form['last_name']
          email = request.form['email']
          age = request.form['age']
          phone = request.form['phone']
          courses_ids = [int(id) for id in request.form.getlist('courses')]
          courses = Course.query.filter(Course.id.in_(courses_ids)).all()
          student = Student(first_name,last_name,email,age,phone)
          student.courses.extend(courses)
          db.session.add(student) 
          db.session.commit() 
          return redirect(url_for('students_list'))
     else:
          form = StudentForm()
          courses = Course.query.all()
          return render_template('student.html',form=form, courses = courses)

@app.route('/studentDetails/<id>',methods=['GET','POST'])
def student_details(id):
     student = Student.query.get(id)
     if request.method == 'POST':
          form = request.form
          student.first_name = form['first_name']
          student.last_name = form['last_name']
          student.email = form['email']
          student.age = form['age']
          student.phone = form['phone']
          courses_ids = [int(id) for id in request.form.getlist('courses')]
          courses = Course.query.filter(Course.id.in_(courses_ids)).all()
          student.courses.extend(courses)
          db.session.commit() 
          return redirect(url_for('students_list'))

     return render_template('student_update',form = StudentForm(obj=student))



@app.route('/students_list')
def students_list():
     students_list = Student.query.all()
     # with sqlite3.connect("instance/college.sqlite3") as con:
     #       cur= con.cursor()
     #       cur.execute("select * from student;")
     #       rows = cur.fetchall()
          #  my_students_list = [{'id': t[0], 'first_name': t[1], 'last_name': t[2],
          #                    'email': t[3], 'age': t[4], 'phone': t[5]} for t in rows]
     #       my_students_list = []
     #       for student in rows:
     #           student_dict = {}
     #           student_dict['id'] = student[0]
     #           student_dict['first_name'] = student[1]
     #           student_dict['last_name'] = student[2]
     #           student_dict['email'] = student[3]
     #           student_dict['age'] = student[4]
     #           student_dict['phone'] = student[5]
     #           my_students_list.append(student_dict)
     # return render_template('students_list.html' , students_list=my_students_list)

     return render_template('students_list.html',students_list=students_list)

@app.route('/search/',methods=['POST','GET'])
def search_name():
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
          courses_ids = [int(id) for id in request.form.getlist('courses')]
          courses = Course.query.filter(Course.id.in_(courses_ids)).all()
          student.courses.extend(courses)
          db.session.commit()
          return redirect(url_for('students_list'))
     
     elif request.method == 'GET':
          courses = Course.query.all()
          return render_template('student_update.html',form=form, courses=courses)

     
@app.route('/studentDelete/<id>',methods=['POST'])   
def student_delete(id):
     student = Student.query.get(id)
     db.session.delete(student)
     db.session.commit()
     return redirect(url_for('students_list'))

@app.route('/studentsDelete',methods=['POST'])
def students_delete():
     students_ids = request.form.getlist('students')
     for student_id in students_ids:
          student = Student.query.get(student_id)
          db.session.delete(student)
     db.session.commit()
     return redirect(url_for('students_list'))    



app.add_url_rule('/register','register',register,methods=['GET','POST'])
app.app_context().push()
db.create_all()
api.add_resource(Names,'/api/names')
api.add_resource(Name,'/api/name/<int:pk>')
api.add_resource(StudentsList,'/api/students')
api.add_resource(StudentApi,'/api/student/<int:pk>')


if __name__ == "__main__":
     app.run(debug=True)  





