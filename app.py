from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# PostgreSQL Configuration (change DB info as needed)
app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql://postgres:ndubuisi@localhost:5555/desmond'
                                         '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date, nullable=False)

# Home route (Login page is the homepage)
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['login']
        password = request.form['password']

        user = User.query.filter((User.username == login_input) | (User.email == login_input)).first()

        if user and check_password_hash(user.password, password):
            return f"Welcome {user.username}!"
        else:
            flash("Invalid login details!")
            return redirect(url_for('login'))

    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        password = request.form['password']

        # Check if user exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("User already exists.")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, phone=phone, dob=dob, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!")
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
