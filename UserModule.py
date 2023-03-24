
class User():
    def __init__(self,username,password):
        self.username = username
        self.password = password
        
UserList = [User(username="admin", password='1234')]

def is_auth(user_name,pass_word):
    for user in UserList:
        if user.username == user_name and user.password == pass_word:
            return True
    

