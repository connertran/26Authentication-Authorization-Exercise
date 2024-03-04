from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,EmailField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    """Register Form """
    username = StringField("Username", validators=[InputRequired(message="Username cannot be blank")])
    password = PasswordField("Password", validators=[InputRequired(message="Enter your password.")])
    email = EmailField("Email", validators=[InputRequired(message="Enter your email.")])
    first_name = StringField("First Name", validators=[InputRequired(message="First name cannot be empty.")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Last name cannot be empty.")])