from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm
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

        session['user_username'] = new_user.username
        # flash('Welcome! Successfully Created Your Account!', "success")

        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods =["GET", "POST"])
def show_login():
    """show the users the login page"""
    if 'user_username' in session:
        username = session.get('user_username')
        return redirect(f'/users/{username}')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            # flash(f"Welcome Back, {user.username}!", "primary")
            session['user_username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    """log out the user"""
    session.pop("user_username")
    return redirect('/')


@app.route('/users/<username>')
def show_users_page(username):
    """show user's page"""
    if 'user_username' not in session:
        return redirect('/login')
    user_username = session.get('user_username')
    if username != user_username:
        return redirect(f'/users/{user_username}')
    
    user= User.query.filter_by(username = username).first()
    feedback= Feedback.query.all()
    return render_template("users_page.html", user=user, feedback=feedback)

@app.route('/users/<username>/feedback/add')
def add_new_feedback(username):
    """show add feedback form"""
    if 'user_username' not in session:
        return redirect('/login')
    user_username = session.get('user_username')
    if username != user_username:
        return redirect(f'/users/{user_username}')
    return render_template('add_feedback.html')
@app.route('/users/<username>/feedback/add', methods=["POST"])
def save_feedback(username):
    """save feedback to db"""
    title = request.form['title']
    content = request.form['content']
    f = Feedback(title=title, content=content, username=username)
    db.session.add(f)
    db.session.commit()
    return redirect(f'/users/{username}')

@app.route('/feedback/<int:feedback_id>/update')
def show_feedback_form_for_update(feedback_id):
    """display a form to edit feedback"""
    if 'user_username' not in session:
        return redirect('/login')
    user_username = session.get('user_username')
    f = Feedback.query.filter_by(id=feedback_id).first()
    if f.user.username != user_username:
        return redirect(f'/users/{user_username}')
    return render_template('update_feedback.html', feedback= f)
@app.route('/feedback/<int:feedback_id>/update', methods=["POST"])
def save_feedback_updates(feedback_id):
    """saving feedback updates to db"""
    title = request.form['title']
    content = request.form['content']
    feedback = Feedback.query.get_or_404(feedback_id)
    feedback.title= title
    feedback.content= content
    db.session.commit()
    return redirect(f'/users/{feedback.user.username}')
