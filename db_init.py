import os
import sys

import psycopg2 as dbapi2

INIT_DB = [
    """CREATE TABLE if not exists users ( 
        user_id serial NOT NULL PRIMARY KEY,
        f_name VARCHAR(30) NOT NULL,
        s_name VARCHAR(30),
        surname VARCHAR(30) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password TEXT NOT NULL,
        age INT,
        country VARCHAR (30),
        faculty VARCHAR (255),
        department VARCHAR (255),
        school VARCHAR (255),
        grade FLOAT );        
    """,
    """CREATE TABLE if not exists mentors (
		mentor_id serial NOT NULL PRIMARY KEY,
		user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE);
    """,
    """CREATE TABLE if not exists mentor_applicants (
		applicant_id serial NOT NULL PRIMARY KEY,
		user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE); 
    """,
    """CREATE TABLE if not exists mentorships (
		mentorship_id serial NOT NULL PRIMARY KEY,
		mentor_id INTEGER REFERENCES mentors(mentor_id) ON DELETE CASCADE,
		applicant_id INTEGER REFERENCES mentor_applicants(applicant_id) ON DELETE CASCADE);
    """,
    """CREATE TABLE if not exists messages (
		message_id serial NOT NULL PRIMARY KEY,
		user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
        content TEXT NOT NULL,
		date DATE );
    """,
    """CREATE TABLE if not exists categories (
		  category_id  serial NOT NULL PRIMARY KEY,
      category_names VARCHAR NOT NULL );
    """,
    """CREATE TABLE if not exists skills (
		    skill_id serial NOT NULL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
        category_id INTEGER REFERENCES categories(category_id),
        skill_name VARCHAR (255) NOT NULL,
        experience_year INT NOT NULL,
        projects VARCHAR (255) NOT NULL,
        skill_level INT NOT NULL );
    """

]
#	    skill_id INTEGER REFERENCES skills(skill_id) ON DELETE CASCADE,
#		  is_valid BOOL );

category_id = [1, 2, 3] # Programming Languages (1)
                        # Frameworks (2)
                        # Libraries & Technologies (3)

skill_arr_1 = ["C", "C++", "Python", "PHP", "Java", "Haskell", "JavaScript", "C#", "Go", "Dart", 
                "SQL", "Fortran", "R", "Swift", "Kotlin"]
skill_arr_2 = ["Django", "Flask", "Laravel", "VueJS", "ReactJS", "AngularJS", "Flutter", 
                 "React Native", "Hadoop", "Bottle", "Ruby on Rails", "Bootstrap", "ASP.NET", "NodeJS"]
skill_arr_3 = ["Docker", "IBM Watson", "Numpy", "Linux", "Tensorflow", "PyTorch", "Blockchain", "Data Science", "Git", "HTML", "SAP", "LaTeX"]

INIT_SKILLS = """INSERT INTO SKILLS """

def init_db(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_DB:
            cursor.execute(statement)
        cursor.close()

if __name__ == "__main__":
  url = os.getenv('DATABASE_URL')
  if url is None:
      print("Usage: DATABASE_URL=url python db_init.py")
      sys.exit(1)
  init_db(url)

