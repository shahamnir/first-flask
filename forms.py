from flask_wtf import Form
from wtforms.fields import EmailField,IntegerField,StringField,HiddenField,SelectField,BooleanField

class StudentForm(Form):
    id = HiddenField()
    first_name = StringField(label='First Name')
    last_name = StringField(label='Last Name')
    email = EmailField(label='email')
    age = IntegerField(label='Age')
    phone = StringField(label='Phone')
    #courses = SelectField(label='Courses')


class CourseForm(Form):
    id = HiddenField()
    name = StringField(label='Course Name')


class LangForm(Form):
    id = HiddenField()
    name = StringField(label='Language name')
