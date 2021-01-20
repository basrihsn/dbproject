import psycopg2 as dbapi2
from config import config
from user import User

url = "dbname='mentorapp' user='postgres' host='localhost' password='postgres'"

def insert_user(f_name, s_name, surname, email, password):
    query = """INSERT INTO users (f_name, s_name, surname, email, password)
    VALUES ('%s', '%s', '%s', '%s', '%s');""" % (f_name, s_name, surname, email, password)
    conn = None
    try:
        params = config()
        conn = dbapi2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        cur.close()
        conn.commit()
    except (Exception, dbapi2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def search_email(email):
    query = """SELECT * FROM Users WHERE email = '%s'""" % (email,) 
    conn = None
    try:
        params = config()
        conn = dbapi2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        cur.close()
        conn.commit()
        user = cur.fetchall()
        if user is not None:
            return True
        else:
            return False
    except (Exception, dbapi2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()   

# def get_user(email):
#     query = """SELECT * FROM users WHERE email = '%s'""" % (email,) 
#     conn = None
#     try:
#         params = config()
#         conn = dbapi2.connect(**params)
#         cur = conn.cursor()
#         cur.execute(query)
#         conn.commit()
#         f_name = None 
#         s_name = None
#         surname = None
#         email = None 
#         password = None
#         for row in cur.fetchall():
#             f_name = row[1]
#             s_name = row[2]
#             surname = row[3]
#             email = row[4]
#             password = row[5]

#         user = User(f_name, s_name, surname, email, password)
#         cur.close()
#         if email is None:
#             return None
#         else:
#             return user
#     except (Exception, dbapi2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()   

def get_user(email):
    statement = """SELECT * FROM users WHERE email = '%s'""" % (email,)
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement)
            user = cursor.fetchall()
            if user is not None:
                for row in user:
                    user = User(row[1], row[2], row[3], row[4], row[5])
                    return user
            else:
                return None