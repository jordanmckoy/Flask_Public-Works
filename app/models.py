# from email.policy import default
from sys import audit
from flask_login import UserMixin
from sqlalchemy import event
from app import db, login_manager

from app.auth.util import hash_pass
from sqlalchemy.schema import DDL

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.String(length=9), db.ForeignKey(
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
        return str(self.id)


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
    hr_wage = db.Column(db.NUMERIC(), nullable=False)
    contract_description = db.Column(db.Text(), nullable=False)


class RegEmployee(db.Model):
    fk_trn = db.Column(db.String(length=9), db.ForeignKey(
        'employee.trn', ondelete='CASCADE'), primary_key=True)
    hiring_date = db.Column(db.Date(), nullable=False)
    yearly_salary = db.Column(db.NUMERIC(), nullable=False)
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
        'reg_employee.fk_trn', ondelete='CASCADE'), nullable=False,)
    fk_job = db.Column(db.Integer(), db.ForeignKey(
        'job.ref_number', ondelete='CASCADE'), nullable=True)
    assigned = db.relationship(
        'Assigned', backref='assigned_job', cascade="all, delete", lazy=True)
    job_complaints = db.relationship(
        'Complaint', backref='job_complaints', cascade="all, delete", lazy=True)


class Assigned(db.Model):
    fk_employee = db.Column(db.String(length=9), db.ForeignKey(
        'employee.trn', ondelete='CASCADE'), primary_key=True)
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
        'resident.email', ondelete='CASCADE'), primary_key=True)
    fk_job = db.Column(db.Integer(), db.ForeignKey(
        'job.ref_number', ondelete='CASCADE'), nullable=True, primary_key=True)
    date = db.Column(db.Date(), nullable=False, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    resolved = db.Column(db.Boolean, default=False, nullable=False)
    comment = db.Column(db.Text(), nullable=True)

audit_employee_trig = DDL('''/
CREATE TRIGGER Employee
AFTER DELETE
    ON employee
    FOR EACH ROW
EXECUTE  PROCEDURE AuditEmployee();

''')
audit_employee_func = DDL(
    '''/
    CREATE OR REPLACE FUNCTION AuditEmployee()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
		 INSERT INTO employee_audit(trn, first_name, last_name, street_num, street_name, city, parish, auditor,"date deleted")
		 VALUES(old.trn,old.first_name,old.last_name,old.street_num,old.street_name,old.city,old.parish,old.auditor,now());
	RETURN NEW;
    END;
    $$;
    '''
)


audit_regemployee_trig = DDL(
    '''/
    CREATE TRIGGER RegEmployee
    AFTER DELETE
    ON reg_employee
    FOR EACH ROW
    EXECUTE  PROCEDURE AuditRegEmployee();  
    '''
)

audit_regemployee_func = DDL(
    '''/
    CREATE OR REPLACE FUNCTION AuditRegEmployee()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
		 INSERT INTO reg_employee_audit(fk_trn, hiring_date, yearly_salary,date_deleted)
		 VALUES(old.fk_trn,old.hiring_date,old.yearly_salary,now());
	RETURN NEW;
    END
    $$;
    '''
)
audit_tempemployee_trig = DDL(
    '''/
    CREATE TRIGGER TempEmployee
    AFTER DELETE
    ON temp_employee
    FOR EACH ROW
    EXECUTE  PROCEDURE AuditRegEmployee();
    '''
)

audit_tempemployee_func = DDL(
    '''
    CREATE OR REPLACE FUNCTION AuditTempEmployee()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
		 INSERT INTO temp_employee_audit(fk_trn, hr_wage, contract_description,date_deleted)
		 VALUES(old.fk_trn,old.hr_wage,old.contract_description,old.now());
	RETURN NEW;
    END
    $$;

    '''
)

audit_phone_trig = DDL(
    '''/
    CREATE TRIGGER Phone
    AFTER DELETE
    ON phone
    FOR EACH ROW
    EXECUTE  PROCEDURE AuditPhone();
'''
)

audit_phone_func = DDL(
    '''/
    CREATE OR REPLACE FUNCTION AuditPhone()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
		 INSERT INTO phone_audit(fk_trn, phone_number,date_deleted)
		 VALUES(old.fk_trn,old.phone_number,now());
	RETURN NEW;
    END
    $$;
    '''
)


audit_job_trig = DDL(
    '''/
    CREATE TRIGGER Job
    AFTER DELETE
    ON job
    FOR EACH ROW
    EXECUTE  PROCEDURE AuditJob();
    '''
)

audit_job_func = DDL(
    '''/
    CREATE OR REPLACE FUNCTION AuditJob()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
		 INSERT INTO job_audit(ref_number, job_start_date, job_end_date, street_num, street_name, city, parish, description,fk_supervisor,fk_job,date_deleted)
		 VALUES(old.ref_number,old.job_start_date,old.job_end_date,old.street_num,old.street_name,old.city,old.parish,old.description,old.fk_supervisor,old.fk_job,now());
	RETURN NEW;
    END
    $$;
    '''
)

audit_assigned_trig= DDL(
    '''/
    CREATE TRIGGER Assigned
    AFTER DELETE
    ON Assigned
    FOR EACH ROW
    EXECUTE  PROCEDURE AuditAssigned();
    '''
)

audit_assigned_func= DDL(
    '''/
    CREATE OR REPLACE FUNCTION AuditAssigned()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
		 INSERT INTO assigned_audit(fk_employee, fk_job, date_assigned, start_date, end_date, date_deleted)
		 VALUES(old.fk_employee,old.fk_job,old.date_assigned,old.start_date,old.end_date,now());
	RETURN NEW;
    END
    $$;
    '''
)

audit_complaint_trig = DDL(
    '''/
    CREATE TRIGGER Complaint
    AFTER DELETE
    ON complaint
    FOR EACH ROW
    EXECUTE  PROCEDURE AuditComplaint();
    '''
)

audit_complaint_func = DDL(
    '''/
    CREATE OR REPLACE FUNCTION AuditComplaint()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
    $$
    BEGIN
		 INSERT INTO complaint_audit(fk_resident, fk_job, date, content, resolved, comment, date_deleted)
		 VALUES(old.fk_resident,old.fk_job,old.date,old.content,old.resolved,comment,now());
	RETURN NEW;
    END
    $$;
    '''
)

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    trn = request.form.get('trn')
    user = Users.query.filter_by(id=trn).first()
    return user if user else None

event.listen(Employee,"after_delete", audit_employee_trig)
event.listen(RegEmployee,"after_delete", audit_regemployee_trig)
event.listen(TempEmployee,"after_delete", audit_tempemployee_trig)
event.listen(Phone,"after_delete", audit_phone_trig)
event.listen(Job,"after_delete", audit_job_trig)
event.listen(Assigned,"after_delete", audit_assigned_trig) 
event.listen(Complaint,"after_delete", audit_complaint_trig)