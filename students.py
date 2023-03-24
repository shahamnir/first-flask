
class Student():
    def __init__(self,first_name,last_name,email,age,phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.phone = phone

        
StudentList = []

def get_student_by_email(email):
    for student in StudentList:
        if student.email == email:
            return student

