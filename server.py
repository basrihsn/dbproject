from user import get_user_id
from flask import request, render_template, url_for, redirect, abort, flash
from flask.app import Flask
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import psycopg2 as dbapi2
from passlib.hash import pbkdf2_sha256
from database import create_tables

app = Flask(__name__)
app.secret_key = b'\x1d\xdd\xe8\xf1i\xaa\x961\xeb\x9b\xf5\xbd\x89W\xd3L'

login = LoginManager()
login.init_app(app)
login.login_view = "login"

@login.user_loader
def load_user(user_id):
    return get_user_id(user_id)

@app.route('/')
def home_page():
    create_tables()
    return render_template('index.html')

@login_required
@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('home_page'))
    return render_template('profile.html', value = current_user)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        email = request.form.get('email')
        passwordInput = request.form.get('password')
        user = get_user_id(email)
        if user is not None:
            password = user.password
            if pbkdf2_sha256.verify(passwordInput, password) == True:
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
    return render_template("homepage.html", message="You have logged out.")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        s_name = request.form.get('s_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')

        #insert_user(f_name, s_name, surname, email, password)
        #insert_user(f_name, s_name, surname, email, password)
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)