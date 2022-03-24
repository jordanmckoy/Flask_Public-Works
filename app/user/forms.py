from flask_wtf import FlaskForm
from wtforms import StringField, DateField, StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email


class ComplaintForm(FlaskForm):
    email_address = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])

    first_name = StringField(
        'first name', id='first_name_create', validators=[DataRequired()])

    last_name = StringField('Last Name', id='last_name_create',
                            validators=[DataRequired()])

    street_number = StringField(
        'street number', id='street_number_create')

    street_name = StringField(
        'street name', id='street_name_create', validators=[DataRequired()])

    city = StringField('city', id='city_create', validators=[DataRequired()])

    phone = IntegerField('phone', id='phone_create',
                         validators=[DataRequired()])

    parish = StringField('parish', id='last_name_create',
                         validators=[DataRequired()])

    job_id = StringField(label='Job ID', validators=[DataRequired()])

    date = DateField('date', validators=[DataRequired()])

    complaint = TextAreaField(label='Complaint Content',
                            validators=[DataRequired()])

# Kingston
# Saint Andrew
# Portland 
# Saint Thomas
# Saint Catherine
# SaintMary
# Saint Ann
# Manchester
# Clarendon
# Hanover
# Westmoreland
# Saint James
# Trelawny
# Saint Elizabeth