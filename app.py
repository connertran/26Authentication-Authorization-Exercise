from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///authentication_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'chicken123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def redirect_to_register():
    """redirect to register page"""

    return redirect('/register')


@app.route('/register', methods=["GET","POST"])
def show_register():
    """show register page"""
    form= RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        hashed_password = User.register(password)
        hashed_password = hashed_password.password
        
        new_user = User(username=username, password=hashed_password, email=email, first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')

        # session['user_username'] = new_user.username
        # flash('Welcome! Successfully Created Your Account!', "success")

        return redirect('/secret')
    else:
        return render_template('register.html', form=form)


@app.route('/secret')
def show_secret():
    """show secret page"""
    return "shhhhh secret"