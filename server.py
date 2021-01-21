from user import get_user_id
from flask import request, render_template, url_for, redirect, abort, flash
from flask.app import Flask
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from psycopg2 import extensions
import os
import psycopg2
from passlib.hash import pbkdf2_sha256
from db_init import init_db
from db_operations import *

app = Flask(__name__)
app.secret_key = b'\x1d\xdd\xe8\xf1i\xaa\x961\xeb\x9b\xf5\xbd\x89W\xd3L'
url = "dbname='mentorapp' user='postgres' host='localhost' password='postgres'"

heroku_debug = True

if not heroku_debug: # If app works in local computer
    os.environ['DATABASE_URL'] = "dbname='mentorapp' user='postgres' host='localhost' password='postgres'"
    init_db(os.environ.get('DATABASE_URL'))

extensions.register_type(extensions.UNICODE)       # With setting these PostgreSQL will gets easier to 
extensions.register_type(extensions.UNICODEARRAY)  # ... handle with Turkish characters

login = LoginManager()
login.init_app(app)
login.login_view = "login"

@login.user_loader
def load_user(user_id):
    return get_user_id(user_id)

@app.route('/')
def home_page():
    return render_template('index.html')

@login_required
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if request.method == 'GET':
        query = """SELECT * FROM users WHERE email = '%s'""" % (current_user.email,)
        with psycopg2.connect(url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                for row in cursor.fetchall():
                    f_name = row[1]
                    s_name = row[2]
                    surname = row[3]
                    email = row[4]
                    return render_template('profile2.html', f_name=f_name, s_name=s_name, surname=surname,
                                       email=email)
    else:
        return render_template("update_profile.html")



@login_required
@app.route('/profile_users', methods=['GET'])
def profile_users():
    if not current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if request.method == 'GET':
        query = """SELECT * FROM users WHERE email = '%s'""" % (current_user.email,)
        with psycopg2.connect(url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                for row in cursor.fetchall():
                    f_name = row[1]
                    s_name = row[2]
                    surname = row[3]
                    email = row[4]
                    return render_template('profile2.html', f_name=f_name, s_name=s_name, surname=surname,
                                       email=email)
    # elif request.method == 'POST':
    #     query = """SELECT user_id FROM users WHERE email = '%s'""" % (current_user.email,)
    #     user_id = ""
    #     with psycopg2.connect(url) as connection:
    #         with connection.cursor() as cursor:
    #             cursor.execute(query)
    #             for row in cursor.fetchall():
    #                 user_id = row[0]
    #     f_name = request.form.get('f_name') 
    #     s_name = request.form.get('s_name')     
    #     surname = request.form.get('surname')
    #     email = request.form.get('email')

    #     query = """UPDATE users SET f_name = '%s', s_name = '%s',surname = '%s', email = '%s' WHERE id = %s""" % (f_name, s_name, surname, email, user_id)
    #     cursor.execute(query)
    #     connection.commit()
    #     return redirect(url_for('profile'))
    # else:
    #     return redirect(url_for('page_not_found'))


@login_required
@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if request.method == 'GET':
        return render_template("update_profile.html")
    else:
        query = """SELECT user_id FROM users WHERE email = '%s'""" % (current_user.email,)
        user_id = ""
        with psycopg2.connect(url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                for row in cursor.fetchall():
                    user_id = row[0]
                f_name = request.form.get('f_name') 
                s_name = request.form.get('s_name')     
                surname = request.form.get('surname')
                email = request.form.get('email')

                query = """UPDATE users SET f_name = '%s', s_name = '%s',surname = '%s', email = '%s' WHERE user_id = %s""" % (f_name, s_name, surname, email, user_id)
                cursor.execute(query)
                connection.commit()
        return redirect(url_for('profile'))



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        email = request.form.get('email')
        passwordInput = request.form.get('password')

        user = get_user(email)
        if user is not None:
                password = user.password
                if pbkdf2_sha256.verify(passwordInput, password):
                    login_user(user)
                    flash("You've entered successfully!")
                    return redirect(url_for('home_page'))
        return render_template("login.html", error_msg = "Please try again. Login informations are wrong!")

@login_required
@app.route("/logout")
def logout():
    if current_user.is_authenticated == False:
        return redirect(url_for('home_page'))
    logout_user()
    #return render_template("homepage.html", message="You have logged out.")
    return redirect(url_for('home_page'))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        s_name = request.form.get('s_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = pbkdf2_sha256.hash(request.form.get('password'))

        flag = True
        query = """SELECT * FROM users WHERE email = '%s'""" % (email,)        
        with psycopg2.connect(url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                user = cursor.fetchall()
                if user is not None:
                    for row in user:
                        db_email = row[4]
                        if (db_email != email):
                            flag = True
                        else:
                            flag = False
        if flag == True:
            insert_user(f_name, s_name, surname, email, password)
            flash("You're successfully registered!", 'success')
            return redirect(url_for('login'))
        else:
            flash("Email has been taken by other user!", 'error')
            return redirect(url_for('signup'))
        # if search_email(email):
        #     flash("Email has been taken by other user!", 'error')
        #     return redirect(url_for('signup'))
        # else:
        #     insert_user(f_name, s_name, surname, email, password)
        #     flash("You're successfully registered!", 'success')
        #     return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@login_required
@app.route('/delete')
def delete():
    if not current_user.is_authenticated:
        return redirect("/")
    query = """SELECT user_id FROM users WHERE email = '%s'""" % (current_user.email,)
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                user_id = row[0]
            query = """DELETE FROM users WHERE user_id = %s""" % (user_id)
            cursor.execute(query)
            logout_user()
            connection.commit()
            flash("You're successfully delete your account!", 'success')
            return redirect("/")   

@app.errorhandler(404) # Returning 404 page for not found URLs 
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    if not heroku_debug: # if app works in localhost
        app.run(debug=True)
    else:  # if app works in HEROKU
        app.run()