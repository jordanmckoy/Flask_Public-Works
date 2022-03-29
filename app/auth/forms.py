from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, StringField, IntegerField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    trn = StringField('trn',
                      id='trn_login',
                      validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    trn = IntegerField('trn',
                      id='trn_create',
                      validators=[DataRequired()])
    email = StringField('Email',
                        id='email_create',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])

class OtpForm(FlaskForm):
    otp = IntegerField('otp',
                      id='otp',
                      validators=[DataRequired()])