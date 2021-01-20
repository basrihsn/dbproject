from flask_login import UserMixin
import psycopg2 as dbapi2

app_url = "dbname='mentorapp' user='postgres' host='localhost' password='postgres'"

class User(UserMixin):
    def __init__(self,f_name, s_name, surname, email, password):
        self.f_name=f_name
        self.s_name=s_name
        self.surname=surname
        self.password = password
        self.email = email
        self.user_active = True
        self.is_admin = False
        self.is_user_authenticated = True

    def get_id(self):
        return self.email
    
    def is_authenticated(self):
        return self.is_user_authenticated

    @property
    def is_active(self):
        return self.user_active

def get_user_id(email):
    query = """ 
        SELECT * FROM users WHERE email = '%s'
    """ % (email,)
    with dbapi2.connect(app_url) as connect:
        with connect.cursor() as cursor:
            cursor.execute(query)
            returned_user = cursor.fetchall()
            if returned_user is not None:
                for row in returned_user:
                    returned_user = User(row[1], row[2], row[3], row[4], row[5])
                    return returned_user
            else:
                return None


