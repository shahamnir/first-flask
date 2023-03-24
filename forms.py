from flask_wtf import Form
from wtforms.fields import EmailField,IntegerField,StringField

class StudentForm(Form):
    first_name = StringField(label='First Name')
    last_name = StringField(label='Last Name')
    email = EmailField(label='email')
    age = IntegerField(label='Age')
    phone = StringField(label='Phone')
    student_id = IntegerField(label='Student ID')