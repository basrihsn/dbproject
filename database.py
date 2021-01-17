import psycopg2 as dbapi2

app_url = "dbname='dfgtstyn' user='dfgtstyn' host='hattie.db.elephantsql.com' password='1JGHpOdnYEde4PsbIac5BV5VmaV7bxed'"

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = ("""
        CREATE TABLE if not exists users ( 
            user_id SERIAL PRIMARY KEY,
            f_name VARCHAR(30) NOT NULL,
            s_name VARCHAR(30),
            surname VARCHAR(30) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password TEXT NOT NULL )       
        """)
    with dbapi2.connect(app_url) as connect:
        with connect.cursor() as cursor:
            cursor.execute(commands)
            connect.commit()

def hello():
    print("Hello")