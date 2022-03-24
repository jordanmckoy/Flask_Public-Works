# from email.policy import default
from flask_login import UserMixin

from app import db, login_manager

from app.auth.util import hash_pass


class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    trn = db.Column(db.String(length=9), db.ForeignKey(
        'employee.trn', ondelete='CASCADE'), primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    manager = db.Column(db.Boolean, default=False, nullable=False)
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.trn)


class Employee(db.Model):
    trn = db.Column(db.String(length=9), primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    street_num = db.Column(db.Integer(), nullable=True)
    street_name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    parish = db.Column(db.String(), nullable=False)
    auditor = db.Column(db.String(length=9), db.ForeignKey(
        'employee.trn', ondelete='CASCADE'), nullable=True)
    phone_numbers = db.relationship(
        'Phone', backref='owned_employee', cascade="all, delete", lazy=True)
    regular_employees = db.relationship(
        'RegEmployee', backref='regular_employee', cascade="save-update, merge, "
        "delete, delete-orphan", lazy=True)
    temporary_employees = db.relationship(
        'TempEmployee', backref='temporary_employee', cascade="all, delete", lazy=True)
    job_assigned = db.relationship(
        'Assigned', backref='assigned_employee', cascade="all, delete", lazy=True)
    users = db.relationship(
        'Users', backref='user_accounts', cascade="all, delete")

    def __repr__(self):
        return f'{self.trn} {self.first_name} {self.last_name}'


class Phone(db.Model):
    fk_trn = db.Column(db.String(length=9), db.ForeignKey(
        'employee.trn', ondelete='CASCADE'), primary_key=True)
    phone_number = db.Column(db.Integer(), primary_key=True)


class TempEmployee(db.Model):
    fk_trn = db.Column(db.String(length=9), db.ForeignKey(
        'employee.trn', ondelete='CASCADE'), primary_key=True)
    hr_wage = db.Column(db.DECIMAL(), nullable=False)
    contract_description = db.Column(db.Text(), nullable=False)


class RegEmployee(db.Model):
    fk_trn = db.Column(db.String(length=9), db.ForeignKey(
        'employee.trn', ondelete='CASCADE'), primary_key=True)
    hiring_date = db.Column(db.Date(), nullable=False)
    yearly_salary = db.Column(db.DECIMAL(), nullable=False)
    jobs = db.relationship('Job', backref='job_supervisor',
                           cascade="all, delete", lazy=True)


class Job(db.Model):
    ref_number = db.Column(db.Integer(), primary_key=True)
    job_start_date = db.Column(db.Date(), nullable=False)
    job_end_date = db.Column(db.Date(), nullable=True)
    street_num = db.Column(db.Integer(), nullable=True)
    street_name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    parish = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    fk_supervisor = db.Column(db.String(length=9), db.ForeignKey(
        'reg_employee.fk_trn'), nullable=False,)
    fk_job = db.Column(db.Integer(), db.ForeignKey(
        'job.ref_number', ondelete='CASCADE'), nullable=True)
    assigned = db.relationship(
        'Assigned', backref='assigned_job', cascade="all, delete", lazy=True)
    job_complaints = db.relationship(
        'Complaint', backref='job_complaints', cascade="all, delete", lazy=True)


class Assigned(db.Model):
    fk_employee = db.Column(db.String(length=9), db.ForeignKey(
        'employee.trn'), primary_key=True)
    fk_job = db.Column(db.Integer(), db.ForeignKey(
        'job.ref_number', ondelete='CASCADE'), primary_key=True)
    date_assigned = db.Column(db.Date(), nullable=True)
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=True)


class Resident(db.Model):
    email = db.Column(db.String(), primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    street_num = db.Column(db.Integer(), nullable=True)
    street_name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    parish = db.Column(db.String(), nullable=False)
    complaints = db.relationship('Complaint', backref='resident_complaints', cascade="all, delete",
                                 lazy=True, primaryjoin="Resident.email==Complaint.fk_resident")


class Complaint(db.Model):
    fk_resident = db.Column(db.String(), db.ForeignKey(
        'resident.email'), primary_key=True)
    fk_job = db.Column(db.Integer(), db.ForeignKey(
        'job.ref_number'), nullable=True,primary_key=True)
    date = db.Column(db.Date(), nullable=False,primary_key=True)
    content = db.Column(db.Text(), nullable=False)

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    trn = request.form.get('trn')
    user = Users.query.filter_by(trn=trn).first()
    return user if user else None