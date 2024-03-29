from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()

# models go below here
class User(db.Model):
    """User."""
    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True,
                         unique=True,
                         nullable=False)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique = True)
    first_name= db.Column(db.String(30),
                          nullable= False)
    last_name= db.Column(db.String(30),
                          nullable= False)
    feedback = db.relationship('Feedback', backref= 'user', cascade='all, delete-orphan')
    
    def greet(self):
        return f"username: {self.username}; email: {self.email}; first_name: {self.first_name}; last_name: {self.last_name}"
    
    @classmethod
    def register(cls, user_password):
        """Register user with hased password & return hashed password"""
        hashed = bcrypt.generate_password_hash(user_password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(password=hashed_utf8)
    
    @classmethod
    def authenticate(cls, username,pwd):
        """validate that user exists & password is correct
        Return user if valid;else return False"""
        u = User.query.filter_by(username= username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
        
class Feedback(db.Model):
    """Feedback."""
    __tablename__="feedback"

    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    title =db.Column(db.String(100),
                     nullable=False)
    content=db.Column(db.Text,
                      nullable=False)
    username=db.Column(db.String(20), db.ForeignKey('users.username', ondelete='CASCADE'), nullable=False)