
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SubmitField, StringField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email


class CreateEmployee(FlaskForm):
    trn = StringField('trn', id='trn_create', validators=[DataRequired()])

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

    auditor = StringField('auditor', id='auditor_create')

    hiring_date = DateField('start_date', validators=[DataRequired()])

    yearly_salary = DecimalField('yearly_salary', validators=[DataRequired()])

    hr_wage = DecimalField('hr_wage', validators=[DataRequired()])

    contract = StringField('contract', validators=[DataRequired()])


class CreateJob(FlaskForm):
    job_start = DateField('start_date', validators=[DataRequired()])

    street_number = StringField(
        'street number', id='street_number_create')

    street_name = StringField(
        'street name', id='street_name_create', validators=[DataRequired()])

    city = StringField('city', id='city_create', validators=[DataRequired()])

    parish = StringField('parish', id='last_name_create',
                         validators=[DataRequired()])

    description = StringField(
        'description', id='job_description', validators=[DataRequired()])

    supervisor = StringField(
        'supervisor', id='supervisor_create', validators=[DataRequired()])

    original_job = StringField(
        'original job', id='job_description')


class EndJob(FlaskForm):
    end_date = DateField('end_date', validators=[DataRequired()])
    # Password recovery form


class PasswordRecoveryForm(FlaskForm):
    password_1 = PasswordField(label='Password')
    password_2 = PasswordField(label='Confirm Password')


class PromoteRegularForm(FlaskForm):
    yearly_salary = DecimalField('yearly_salary', validators=[DataRequired()])


class PromoteTemporaryForm(FlaskForm):
    hr_wage = DecimalField('hr_wage', validators=[DataRequired()])
    contract = StringField('contract', validators=[DataRequired()])
