from flask_login import UserMixin
import psycopg2 as dbapi2

app_url = "dbname='dfgtstyn' user='dfgtstyn' host='hattie.db.elephantsql.com' password='1JGHpOdnYEde4PsbIac5BV5VmaV7bxed'"

class User(UserMixin):
    def __init__(self,fname, sname, surname, email, password):
        self.fname=fname
        self.sname=sname
        self.surname=surname
        self.password = password
        self.email = email
        self.is_active = True
        self.is_admin = False
        self.is_user_authenticated = True

    def get_id(self):
        return self.email
    
    def is_authenticated(self):
        return self.is_user_authenticated

    @property
    def is_active(self):
        return self.is_active

def get_user_id(email):
    query = """ 
        SELECT * from users WHERE email = '%s'
    """
    arg = email
    with dbapi2.connect(app_url) as connect:
        with connect.cursor() as cursor:
            cursor.execute(query, arg)
            returned_user = cursor.fetchall()
            if returned_user is not None:
                for row in returned_user:
                    returned_user = User(row[1], row[2], row[3], row[4], row[5])
                    return returned_user
            else:
                return None

