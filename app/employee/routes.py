from app.employee import blueprint
from flask import render_template
from flask_login import login_required
from app.models import Employee, Assigned, TempEmployee, RegEmployee, Users
from flask_login import current_user
import sys
import inspect
# Employee Dashboard Routes


@blueprint.route('/employee/dashboard')
@login_required
def employee_index():
        
    # print(current_user.trn, file=sys.stderr)
    # user = current_user.trn
    # jobs_assigned = Assigned.query.filter(
    #     Assigned.fk_employee == user)
    # current_job = Assigned.query.filter(
    #     Assigned.fk_employee == user, Assigned.end_date == None)
    # temp_employee = TempEmployee.query.filter_by(fk_trn=user).first()
    # reg_employee = RegEmployee.query.filter_by(fk_trn=user).first()
    # if reg_employee:
    #     pay = f'${reg_employee.yearly_salary}'
    #     employee = Employee.query.filter_by(trn=user).first()
    #     name = f'{employee.first_name} {employee.last_name}'
    #     auditor_id = f'trn:{employee.auditor}'
    #     auditor = employee.auditor
    #     current_user_auditor = Employee.query.filter_by(trn=auditor).first()
    return render_template('employee/dashboard.html', segment='dashboard')
    #     if auditor != None:
    #         auditor_name = f'{current_user_auditor.first_name} {current_user_auditor.last_name}'
    #         return render_template('employee/dashboard.html', segment='index', 
    #         paytype='Salary', name=name, jobs_assigned=jobs_assigned, pay=pay, 
    #         current_job=current_job, auditor_id=auditor_id, auditor_name=auditor_name, 
    #         manager_button=manager_button)
    #     else:
    #         auditor_id = 'No Auditor Is Assigned'
    #         return render_template('employee/dashboard.html', segment='index', paytype='Salary', 
    #         name=name, jobs_assigned=jobs_assigned, pay=pay, current_job=current_job, 
    #         auditor_id=auditor_id, manager_button=manager_button)

    # elif temp_employee:
    #     tempemployee = TempEmployee.query.filter_by(fk_trn=user).first()
    #     pay = f'${tempemployee.hr_wage}'
    #     employee = Employee.query.filter_by(trn=user).first()
    #     auditor_id = f'trn:{employee.auditor}'
    #     name = f'{employee.first_name} {employee.last_name}'
    #     auditor = employee.auditor
    #     current_user_auditor = Employee.query.filter_by(trn=auditor).first()
    #     if auditor != None:
    #         auditor_name = f'{current_user_auditor.first_name} {current_user_auditor.last_name}'
    #         return render_template('employee/dashboard.html', segment='index', paytype='Hourly Wage', 
    #         name=name, jobs_assigned=jobs_assigned, pay=pay, current_job=current_job, 
    #         auditor_id=auditor_id, auditor_name=auditor_name)
    #     else:
    #         auditor_id = 'No Auditor Is Assigned'
    #         return render_template('employee/dashboard.html', segment='index', paytype='Hourly Wage', 
    #         name=name, jobs_assigned=jobs_assigned, pay=pay, current_job=current_job, 
    #         auditor_id=auditor_id)

# # Employee's Jobs
# @blueprint.route('/employee/jobs')
# @login_required
# def jobs():
#     jobs_assigned = Assigned.query.filter(
#         Assigned.fk_employee == current_user.trn)
#     return render_template('home/job.html', segment='index', jobs_assigned=jobs_assigned)

# # Employee Profile
# @blueprint.route('/employee/profile')
# @login_required
# def profile():
#     user = current_user.trn
#     employee = Employee.query.filter_by(trn=user).first()
#     first_name = employee.first_name
#     last_name = employee.last_name
#     address = f'{employee.street_num} {employee.street_name}'
#     city = employee.city
#     parish = employee.parish
#     phone = Phone.query.filter(Phone.fk_trn == current_user.trn)
#     if employee.street_num == None:
#         address = f'{employee.street_name}'
#         return render_template('home/profile.html', segment='index', phone=phone, user=user, employee=employee, first_name=first_name, last_name=last_name, address=address, parish=parish, city=city)
#     return render_template('home/profile.html', segment='index', phone=phone, user=user, employee=employee, first_name=first_name, last_name=last_name, address=address, parish=parish, city=city)
#     return render_template('employee/profile.html', segment='settings')

# # Emplyoee View Job Function
# @blueprint.route('/view-job/<string:trn>')
# @login_required
# def view_my_job(trn):
#     job = Job.query.filter_by(ref_number=trn).first()
#     if job.street_num:
#         address = f'{job.street_num} {job.street_name} {job.city} {job.parish}'
#     else:
#         address = f'{job.street_name} {job.city} {job.parish}'
#     return render_template('home/view-job.html', job=job, address=address)

# # EMployee Supervisor Portal
# @blueprint.route('/supervisor-portal')
# @login_required
# def supervisor_view():
#     job = Job.query.filter_by(fk_supervisor= current_user.trn).first()
#     if job:
#         return render_template('home/supervisor-view.html',msg='Below are a list of jobs you are supervising', job=job)
#     else:
#         return render_template('home/supervisor-view.html', msg='You are not currently a supervisor',job=job)
