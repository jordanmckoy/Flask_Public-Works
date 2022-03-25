from app.employee import blueprint
from flask import render_template
from flask_login import login_required
from app.models import Employee, Assigned, TempEmployee, RegEmployee, Phone, Job, Users
from flask_login import current_user

@blueprint.route('/employee-index')
@login_required
def employee_index():
    user = Users.query.filter_by(TRN=current_user.TRN).first()
    if user.manager == True:
        manager_button = True
    else: 
        manager_button = False
    user = current_user.TRN
    jobs_assigned = Assigned.query.filter(
        Assigned.fk_employee == current_user.TRN)
    current_job = Assigned.query.filter(
        Assigned.fk_employee == current_user.TRN, Assigned.end_date == None)
    temp_employee = TempEmployee.query.filter_by(fk_trn=user).first()
    reg_employee = RegEmployee.query.filter_by(fk_trn=user).first()
    if reg_employee:
        regemployee = RegEmployee.query.filter_by(fk_trn=user).first()
        pay = f'${regemployee.yearly_salary}'
        employee = Employee.query.filter_by(trn=user).first()
        name = f'{employee.first_name} {employee.last_name}'
        auditorID = f'ID:{employee.auditor}'
        
        auditor = employee.auditor
        paytype = 'Salary'
        current_user_auditor = Employee.query.filter_by(trn=auditor).first()
        if auditor != None:
            auditor_name = f'{current_user_auditor.first_name} {current_user_auditor.last_name}'
            return render_template('home/employee-index.html', segment='index', name=name, jobs_assigned=jobs_assigned, pay=pay, current_job=current_job, auditorID=auditorID, auditor_name=auditor_name, manager_button=manager_button)
        else:
            auditorID = 'No Auditor Assigned'
            return render_template('home/employee-index.html', segment='index', paytype=paytype, name=name, jobs_assigned=jobs_assigned, pay=pay, current_job=current_job, auditorID=auditorID,manager_button=manager_button)

    elif temp_employee:
        tempemployee = TempEmployee.query.filter_by(fk_trn=user).first()
        pay = f'${tempemployee.hr_wage}'
        employee = Employee.query.filter_by(trn=user).first()
        auditorID = f'ID:{employee.auditor}'
        name = f'{employee.first_name} {employee.last_name}'
        auditor = employee.auditor
        paytype = 'Hourly Wage'
        current_user_auditor = Employee.query.filter_by(trn=auditor).first()
        if auditor != None:
            auditor_name = f'{current_user_auditor.first_name} {current_user_auditor.last_name}'
            return render_template('home/employee-index.html', segment='index', paytype=paytype, name=name, jobs_assigned=jobs_assigned, pay=pay, current_job=current_job, auditorID=auditorID, auditor_name=auditor_name)
        else:
            auditorID = 'No Auditor Assigned'
            return render_template('home/employee-index.html', segment='index', paytype=paytype, name=name, jobs_assigned=jobs_assigned, pay=pay, current_job=current_job, auditorID=auditorID)

@blueprint.route('/my-jobs')
@login_required
def jobs():
    jobs_assigned = Assigned.query.filter(
        Assigned.fk_employee == current_user.TRN)
    return render_template('home/job.html', segment='index', jobs_assigned=jobs_assigned)


@blueprint.route('/employee/profile')
@login_required
def profile():
    # user = current_user.TRN
    # employee = Employee.query.filter_by(trn=user).first()
    # first_name = employee.first_name
    # last_name = employee.last_name
    # address = f'{employee.street_num} {employee.street_name}'
    # city = employee.city
    # parish = employee.parish
    # phone = Phone.query.filter(Phone.fk_trn == current_user.TRN)
    # if employee.street_num == None:
    #     address = f'{employee.street_name}'
    #     return render_template('home/profile.html', segment='index', phone=phone, user=user, employee=employee, first_name=first_name, last_name=last_name, address=address, parish=parish, city=city)
    # return render_template('home/profile.html', segment='index', phone=phone, user=user, employee=employee, first_name=first_name, last_name=last_name, address=address, parish=parish, city=city)
    return render_template('employee/profile.html', segment='settings')

@blueprint.route('/view-job/<string:id>')
@login_required
def view_my_job(id):
    job = Job.query.filter_by(ref_number=id).first()
    if job.street_num:
        address = f'{job.street_num} {job.street_name} {job.city} {job.parish}'
    else:
        address = f'{job.street_name} {job.city} {job.parish}'
    return render_template('home/view-job.html', job=job, address=address)

@blueprint.route('/supervisor-portal')
@login_required
def supervisor_view():
    job = Job.query.filter_by(fk_supervisor= current_user.TRN).first()
    if job:
        return render_template('home/supervisor-view.html',msg='Below are a list of jobs you are supervising', job=job)
    else:
        return render_template('home/supervisor-view.html', msg='You are not currently a supervisor',job=job)
