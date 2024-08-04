from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, InputRequired, ValidationError

roles = [
    ('Collector' , 'Collector'),
    ('Household' , 'Household')
]

class RegisterForm(FlaskForm):
    firstname = StringField("First Name", validators=[InputRequired()])
    secondname = StringField("Second Name", validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField("What type of user are you?", choices=roles, coerce=str)
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    role = SelectField("What type of user are you?", choices=roles, coerce=str)
    submit = SubmitField('Login')

class VerifyEmailForm(FlaskForm):
    otp = StringField('Verify your email', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify')
class ResendConfirmationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Resend Confirmation Email')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField('Reset Password')