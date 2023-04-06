# WTF stands for WT Forms. It's a built-in module (or plugin) of FLask that facilitates
# ...the designing of web forms in Flask web applications
# FlaskForm is a class that we are importing from the flask_wtf module
# QUESTION: is it possible to look at the actual code for these things that we're accessing,
# ...like the FlaskForm class, for example?
from flask_wtf import FlaskForm
# These fields are all functions within the wtforms module
# QUESTION: What's the difference between wtofrms and flask_wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
# A validator takes an input, verifies it fulfills some criterion, and returns. Or if
# ...the input fails the validation, it returns a ValidationError.
# QUESTION: Is "validators" a class within wtforms? Are ValidationError, DataRequired, Email,
# ... EqualTo, and Length all instances of the validator class?
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
# User is a class within the models module of my microblog app. We are importing the User class
# ...to use it here in the forms module.
from app.models import User

# QUESTION: Is this correct?--> All of the classes below are child classes that inherit 
# ...the functionality of the parent class, FlaskForm, which was imported above.
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
            
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
