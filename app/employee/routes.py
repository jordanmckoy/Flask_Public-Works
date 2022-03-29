from itertools import count
from app.employee import blueprint
from flask import render_template
from flask_login import login_required
from app.models import Employee, Assigned, Job, Phone, TempEmployee, RegEmployee, Users
from flask_login import current_user
# Employee Dashboard Routes


@blueprint.route('/employee/dashboard')
@login_required
def employee_index():
    users = Users.query.filter_by(id=current_user.id).first()
    if users.manager == True:
        manager_button = True
    else:
        manager_button = False
    user = current_user.id
    jobs_assigned = Assigned.query.filter(
        Assigned.fk_employee == user)
    current_job = Assigned.query.filter(
        Assigned.fk_employee == user, Assigned.end_date == None)
    count = Assigned.query.filter(
        Assigned.fk_employee == user, Assigned.end_date == None).count()
    temp_employee = TempEmployee.query.filter_by(fk_trn=user).first()
    reg_employee = RegEmployee.query.filter_by(fk_trn=user).first()
    if reg_employee:
        pay = f'${int(reg_employee.yearly_salary)}'
        employee = Employee.query.filter_by(trn=user).first()
        auditor_id = f'TRN:{employee.auditor}'
        auditor = employee.auditor
        user_auditor = Employee.query.filter_by(trn=auditor).first()
        if auditor != None:
            auditor_name = f'{user_auditor.first_name} {user_auditor.last_name}'
            return render_template('employee/dashboard.html', segment='Dashboard',
                                   paytype='Salary', jobs_assigned=jobs_assigned, pay=pay,
                                   current_job=current_job, auditor_id=auditor_id, auditor_name=auditor_name,
                                   manager_button=manager_button, count=count)
        else:
            auditor_id = 'No Auditor Is Assigned'
            return render_template('employee/dashboard.html', segment='Dashboard', paytype='Salary',
                                   jobs_assigned=jobs_assigned, pay=pay, current_job=current_job,
                                   auditor_id=auditor_id, manager_button=manager_button, count=count)

    elif temp_employee:
        tempemployee = TempEmployee.query.filter_by(fk_trn=user).first()
        pay = f'${int(tempemployee.hr_wage)}'
        employee = Employee.query.filter_by(trn=user).first()
        auditor_id = f'trn:{employee.auditor}'
        auditor = employee.auditor
        user_auditor = Employee.query.filter_by(trn=auditor).first()
        if auditor != None:
            auditor_name = f'{user_auditor.first_name} {auditor.last_name}'
            return render_template('employee/dashboard.html', segment='Dashboard', paytype='Hourly Wage',
                                   jobs_assigned=jobs_assigned, pay=pay, current_job=current_job,
                                   auditor_id=auditor_id, auditor_name=auditor_name, count=count)
        else:
            auditor_id = 'No Auditor Is Assigned'
            return render_template('employee/dashboard.html', segment='Dashboard', paytype='Hourly Wage',
                                   jobs_assigned=jobs_assigned, pay=pay, current_job=current_job,
                                   auditor_id=auditor_id, count=count)

# Employee's Jobs


@blueprint.route('/employee/jobs')
@login_required
def jobs():
    jobs_assigned = Assigned.query.filter(
        Assigned.fk_employee == current_user.id)
    return render_template('employee/job.html', segment='index', jobs_assigned=jobs_assigned)

# Employee Profile


@blueprint.route('/employee/profile')
@login_required
def profile():
    user = current_user.id
    employee = Employee.query.filter_by(trn=user).first()
    first_name = employee.first_name
    last_name = employee.last_name
    city = employee.city
    parish = employee.parish
    phone = Phone.query.filter(Phone.fk_trn == current_user.id)
    if employee.street_num == None:
        return render_template('employee/profile.html', segment='index', phone=phone, user=user, employee=employee, first_name=first_name, last_name=last_name, parish=parish, city=city)
    return render_template('employee/profile.html', segment='index', phone=phone, user=user, employee=employee, first_name=first_name, last_name=last_name, parish=parish, city=city)

# Emplyoee View Job Function


@blueprint.route('/employee/view-job/<string:id>')
@login_required
def view_job(id):
    job = Job.query.filter_by(ref_number=id).first()
    return render_template('employee/view-job.html', job=job, segment='View Job')

# Employee Supervisor Portal


@blueprint.route('/employee/supervisor-portal')
@login_required
def supervisor_portal():
    job = Job.query.filter_by(fk_supervisor=current_user.id).first()
    if job:
        return render_template('employee/supervisor.html', msg='Below are a list of jobs you are supervising', job=job, segment='Supervisor Portal')
    else:
        return render_template('employee/supervisor.html', msg='You are not currently a supervisor', job=job, segment='Supervisor Portal')



@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('error/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('error/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('error/page-500.html'), 500