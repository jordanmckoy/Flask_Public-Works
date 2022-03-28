from flask_mail import Message
from flask_wtf import FlaskForm
from sqlalchemy import false
from app.manager import blueprint
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from app.models import Complaint, Employee, Assigned,TempEmployee, RegEmployee, Phone, Job, Users
from flask_login import current_user
from app import db
from wtforms import DateField, RadioField
from wtforms.validators import DataRequired
from app.manager.forms import CreateEmployee, CreateJob, EndJob, PromoteRegularForm, PromoteTemporaryForm


@blueprint.route('/manager/dashboard')
@login_required
def manager():
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        limit = 4
        employee = Employee.query.filter(Employee.trn != None).all()
        employee_count = Employee.query.count()
        job_count = Job.query.filter_by(job_end_date=None).count()
        complaint_count = Complaint.query.filter_by(resolved=0).count()
        job = Job.query.filter(Job.job_end_date==None).all()
        return render_template('manager/dashboard.html', segment='dashboard',limit=limit,job=job,employee_count=employee_count, job_count=job_count,complaint_count=complaint_count, employee=employee )
    else:
        return redirect(url_for('employee_blueprint.employee_index'))

@blueprint.route('/manager/jobs')
@login_required
def manage_jobs():
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        jobs = Job.query.filter(Job.ref_number != None).all()
        return render_template('manager/job.html', segment='jobs', jobs=jobs)
    else:
        return redirect(url_for('employee_blueprint.employee_index'))

@blueprint.route('/manager/supervisors')
@login_required
def supervisors():
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        jobs = Job.query.filter(Job.ref_number != None)
        return render_template('manager/supervisor.html',segment='supervisor', jobs=jobs)
    else:
        return redirect(url_for('employee_blueprint.employee_index'))   

@blueprint.route('/manager/assigned')
@login_required
def assigned():
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        jobs_assigned = Assigned.query.filter(Assigned.fk_employee != None)
        return render_template('manager/assigned.html', segment='index', jobs_assigned=jobs_assigned)
    else:
        return redirect(url_for('employee_blueprint.employee_index')) 

@blueprint.route('/manager/employees')
@login_required
def manage_employees():
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        all_employees = Employee.query.filter(Employee.trn != None).all()
        return render_template('manager/manage-employees.html', segment='employees', all_employees=all_employees)
    else:
        return redirect(url_for('employee_blueprint.employee_index'))

@blueprint.route('/manager/promote-employee/<string:trn>')
@login_required
def promote_employee(trn):
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        regemployee = RegEmployee.query.filter_by(fk_trn=trn).first()
        if regemployee:
            return redirect(url_for('manager_blueprint.promote_regular_employee', trn=trn, segment='employees'))

        else:
            return redirect(url_for('manager_blueprint.promote_temporary_employee', trn=trn, segment='employees'))
    else:
        return redirect(url_for('employee_blueprint.employee_index'))


@blueprint.route('/manager/promote-temporary-employee/<string:trn>', methods=['GET', 'POST'])
@login_required
def promote_temporary_employee(trn):
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        form = PromoteTemporaryForm(request.form)
        tempemployee = TempEmployee.query.filter_by(fk_trn=trn).first()
        if 'add' in request.form:
            wage = request.form['hr_wage']
            contract = request.form['contract']
            employee = TempEmployee.query.filter_by(fk_trn=trn).update(
                dict(hr_wage=wage, contract_description=contract))
            db.session.commit()
            return redirect(url_for('manager_blueprint.manage_employees'))
        return render_template('manager/promote-temporary.html', form=form, segment='employees')
    else:
        return redirect(url_for('employee_blueprint.employee_index'))


@blueprint.route('/manager/promote-regular-employee/<string:trn>',  methods=['GET', 'POST'])
@login_required
def promote_regular_employee(trn):
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        regemployee = RegEmployee.query.filter_by(fk_trn=trn).first()
        form = PromoteRegularForm(request.form)
        if 'add' in request.form:
            salary = request.form['yearly_salary']
            employee = RegEmployee.query.filter_by(fk_trn=trn).update(
                dict(yearly_salary=salary))
            db.session.commit()
            return redirect(url_for('manager_blueprint.manage_employees'))
        return render_template('manager/promote-regular.html', form=form, segment='employees')

    else:
        return redirect(url_for('employee_blueprint.employee_index'))


@blueprint.route('/manager/view-employee/<string:trn>')
@login_required
def view_employee(trn):
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        regemployee = RegEmployee.query.filter_by(fk_trn=trn).first()
        if regemployee:
            return redirect(url_for('manager_blueprint.view_regular_employee', trn=trn))

        else:
            return redirect(url_for('manager_blueprint.view_temporary_employee', trn=trn))
    else:
        return redirect(url_for('employee_blueprint.employee_index'))

@blueprint.route('/manager/view-job/<string:id>')
@login_required
def view_jobs(id):
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        jobs = Job.query.filter_by(ref_number=id).first()
        return render_template('manager/view-jobs.html', jobs=jobs, segment='jobs')
    else:
        return redirect(url_for('employee_blueprint.employee_index'))


@blueprint.route('/manager/view-regular-employee/<string:trn>')
@login_required
def view_regular_employee(trn):
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        regemployee = RegEmployee.query.filter_by(fk_trn=trn).first()
        employee = Employee.query.filter_by(trn=trn).first()
        email = Users.query.filter_by(id=trn).first()
        trn = employee.trn
        first_name = employee.first_name
        last_name = employee.last_name
        street_number = employee.street_num
        street_name = employee.street_name
        city = employee.city
        parish = employee.parish
        auditor = employee.auditor
        hiring_date = regemployee.hiring_date
        salary = int(regemployee.yearly_salary)
        phone = Phone.query.filter(Phone.fk_trn == trn)
        if email:
            return render_template('manager/regular-employee-profile.html', segment='employee', email=email, phone=phone, trn=trn, employee=employee, first_name=first_name, last_name=last_name, street_number=street_number, street_name=street_name, parish=parish, city=city, auditor=auditor, salary=salary, hiring_date=hiring_date)
        else:
            return render_template('manager/regular-employee-profile.html', segment='employee', email='Employee Has Not Created Their Account', phone=phone, trn=trn, employee=employee, first_name=first_name, last_name=last_name, street_number=street_number, street_name=street_name, parish=parish, city=city, auditor=auditor, salary=salary, hiring_date=hiring_date)
    else:
        return redirect(url_for('employee_blueprint.employee_index'))


@blueprint.route('/manager/view-temporary-employee/<string:trn>')
@login_required
def view_temporary_employee(trn):
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        tempemployee = TempEmployee.query.filter_by(fk_trn=trn).first()
        employee = Employee.query.filter_by(trn=trn).first()
        email = Users.query.filter_by(id=trn).first()
        trn = employee.trn
        first_name = employee.first_name
        last_name = employee.last_name
        street_number = employee.street_num
        street_name = employee.street_name
        city = employee.city
        parish = employee.parish
        auditor = employee.auditor
        hr_wage = int(tempemployee.hr_wage)
        contract = tempemployee.contract_description
        phone = Phone.query.filter(Phone.fk_trn == trn)
        if email:
            return render_template('manager/temporary-employee-profile.html', segment='employee', email=email, phone=phone, trn=trn, employee=employee, first_name=first_name, last_name=last_name, street_number=street_number, street_name=street_name, parish=parish, city=city, auditor=auditor, hr_wage=hr_wage, contract=contract)
        else:
            return render_template('manager/temporary-employee-profile.html', segment='employee', email='Employee Has Not Created Their Account', phone=phone, trn=trn, employee=employee, first_name=first_name, last_name=last_name, street_number=street_number, street_name=street_name, parish=parish, city=city, auditor=auditor, hr_wage=hr_wage, contract=contract)
    else:
        return redirect(url_for('employee_blueprint.employee_index'))


@ blueprint.route('/manager/delete-employee/<string:trn>')
@ login_required
def delete_employee(trn):
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        user_to_delete = Employee.query.filter_by(trn=trn).first()
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('manager_blueprint.manage_employees'))
    else:
        return redirect(url_for('manager_blueprint.employee_index'))


@ blueprint.route('/manager/add-employees/temporary', methods=['GET', 'POST'])
@ login_required
def tempemployee():
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        employeeform = CreateEmployee(request.form)
        if request.method == "POST":
            iftrn = int(request.form['trn'])
            trn = request.form['trn']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            street_num = request.form['street_number']
            street_name = request.form['street_name']
            city = request.form['city']
            parish = request.form['parish']
            ifauditor = int(request.form['auditor'])
            auditor = request.form['auditor']
            phone = request.form['phone']
            ifphone = int(request.form['phone'])
            wage = request.form['hr_wage']
            contract = request.form['contract']
            employee_trn = Employee.query.filter_by(trn=trn).first()

            if employee_trn:
                return render_template('manager/new-employee-temp.html',
                                       msg='Employee is Already Added',
                                       success=False,
                                       form=employeeform, segment='employee')

            if iftrn > 999999999:
                return render_template('manager/new-employee-temp.html',
                                       msg='Please Enter A Valid TRN',
                                       success=false,
                                       form=employeeform, segment='employee')
            if ifauditor > 999999999:
                return render_template('manager/new-employee-temp.html',
                                       msg='Please Enter A Valid Auditor TRN',
                                       success=false,
                                       form=employeeform, segment='employee')

            if ifphone > 9999999999:
                return render_template('manager/new-employee-temp.html',
                                       msg='Please Enter A Valid Phone Number',
                                       success=false,
                                       form=employeeform, segment='employee')

            if street_num == '':
                employee = Employee(trn=trn, first_name=first_name, last_name=last_name,
                                    street_name=street_name, city=city, parish=parish, auditor=auditor)

            elif street_num != None:
                employee = Employee(trn=trn, first_name=first_name, last_name=last_name, street_num=street_num,
                                    street_name=street_name, city=city, parish=parish, auditor=auditor)

            phone_num = Phone(fk_trn=trn, phone_number=phone)
            temp_employee = TempEmployee(
                fk_trn=trn, hr_wage=wage, contract_description=contract)
            db.session.add(employee)
            db.session.add(temp_employee)
            db.session.add(phone_num)
            db.session.commit()

            return render_template('manager/new-employee-temp.html',
                                   msg='Employee Created',
                                   success=True, form=employeeform, segment='employee')

        else:
            return render_template('manager/new-employee-temp.html', form=employeeform, segment='employee')
    else:
        return redirect(url_for('employee_blueprint.employee_index'))


@ blueprint.route('/manager/add-employees/regular', methods=['GET', 'POST'])
@ login_required
def regemployees():
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        employeeform = CreateEmployee(request.form)
        if request.method == "POST":
            iftrn = int(request.form['trn'])
            trn = request.form['trn']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            street_num = request.form['street_number']
            street_name = request.form['street_name']
            city = request.form['city']
            parish = request.form['parish']
            ifauditor = int(request.form['auditor'])
            auditor = request.form['auditor']
            phone = request.form['phone']
            ifphone = int(request.form['phone'])
            date_hiring = request.form['hiring_date']
            salary = request.form['yearly_salary']
            employee_trn = Employee.query.filter_by(trn=trn).first()

            if employee_trn:
                return render_template('manager/new-employee-reg.html',
                                       msg='Employee is Already Added',
                                       success=False,
                                       form=employeeform, segment='employee')

            if iftrn > 999999999:
                return render_template('manager/new-employee-reg.html',
                                       msg='Please Enter A Valid TRN',
                                       success=false,
                                       form=employeeform, segment='employee')
            if ifauditor > 999999999:
                return render_template('manager/new-employee-reg.html',
                                       msg='Please Enter A Valid Auditor TRN',
                                       success=false,
                                       form=employeeform, segment='employee')

            if ifphone > 9999999999:
                return render_template('manager/new-employee-temp.html',
                                       msg='Please Enter A Valid Phone Number',
                                       success=false,
                                       form=employeeform, segment='employee')

            if street_num == '':
                employee = Employee(trn=trn, first_name=first_name, last_name=last_name,
                                    street_name=street_name, city=city, parish=parish, auditor=auditor)

            else:
                employee = Employee(trn=trn, first_name=first_name, last_name=last_name, street_num=street_num,
                                    street_name=street_name, city=city, parish=parish, auditor=auditor)

            phone_num = Phone(fk_trn=trn, phone_number=phone)
            reg_employee = RegEmployee(
                fk_trn=trn, hiring_date=date_hiring, yearly_salary=salary)
            db.session.add(employee)
            db.session.add(reg_employee)
            db.session.add(phone_num)
            db.session.commit()

            return render_template('manager/new-employee-reg.html',
                                   msg='Employee Created',
                                   success=True, form=employeeform, segment='employee')

        else:
            return render_template('manager/new-employee-reg.html', form=employeeform, segment='employee')
    else:
        return redirect(url_for('emploayee_blueprint.employee_index'))


@blueprint.route('/manager/add-jobs', methods=['GET', 'POST'])
@login_required
def addjobs():
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        jobform = CreateJob(request.form)
        if 'add' in request.form:
            job_start = request.form['job_start']
            street_num = request.form['street_number']
            street_name = request.form['street_name']
            city = request.form['city']
            parish = request.form['parish']
            description = request.form['description']
            sup_trn = request.form['supervisor']
            original_job = request.form['original_job']

            supervisor = RegEmployee.query.filter_by(fk_trn=sup_trn).first()
            if not supervisor:
                return render_template('manager/new-job.html', msg='Please Enter a Valid Supervisor TRN', success=True, form=jobform, segment='employee')

            if street_num == '':
                if original_job == '':
                    jobs = Job(job_start_date=job_start, street_name=street_name, city=city,
                               parish=parish, description=description, fk_supervisor=sup_trn)
                else:
                    jobs = Job(job_start_date=job_start, street_name=street_name, city=city,
                               parish=parish, description=description, fk_supervisor=sup_trn, fk_job=original_job)
                db.session.add(jobs)
                db.session.commit()
            else:
                if original_job == '':
                    jobs = Job(job_start_date=job_start, street_num=street_num, street_name=street_name, city=city,
                               parish=parish, description=description, fk_supervisor=sup_trn)
                else:
                    Job(job_start_date=job_start, street_num=street_num, street_name=street_name, city=city,
                        parish=parish, description=description, fk_supervisor=sup_trn, fk_job=original_job)
                db.session.add(jobs)
                db.session.commit()

            return render_template('manager/new-job.html', msg='Job Created', success=True, form=jobform, segment='employee')

        else:
            return render_template('manager/new-job.html', msg='Please Create a Job', success=True, form=jobform, segment='employee')
    else:
        return redirect(url_for('employee_blueprint.employee_index'))


@ blueprint.route('/manager/delete-job/<string:id>')
@ login_required
def delete_job(id):
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        job_to_delete = Job.query.filter_by(ref_number=id).first()
        db.session.delete(job_to_delete)
        db.session.commit()
        return redirect(url_for('employee_blueprint.manage_jobs'))
    else:
        return redirect(url_for('employee_blueprint.employee_index'))


@ blueprint.route('/manager/end-job/<string:id>', methods=['GET', 'POST'])
@ login_required
def end_job(id):
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        form = EndJob(request.form)
        if 'add' in request.form:
            end_date = request.form['end_date']
            end_job = Job.query.filter_by(ref_number=id).update(
                dict(job_end_date=end_date))
            db.session.commit()
            return redirect(url_for('manager_blueprint.manage_jobs'))
        return render_template('manager/end-job.html', success=false, form=form)
    else:
        return redirect(url_for('employee_blueprint.employee_index'))


@blueprint.route('/manager/assign-employees/<string:id>', methods=['Get', 'POST'])
@login_required
def assign_employee(id):
    user = Users.query.filter_by(id=current_user.id).first()
    if user.manager == True:
        employee_list = Employee.query.filter(Employee.trn != None).all()

        class AssignForm(FlaskForm):
            employee = RadioField('employee', choices=(
                (employee) for employee in employee_list), validators=[DataRequired()])
            date_assigned = DateField(
                'date_assigned', validators=[DataRequired()])
            start_date = DateField('start_date', validators=[DataRequired()])

        form = AssignForm(request.form)
        if 'add' in request.form:
            employee = request.form['employee']
            employee = employee[0:9]
            date_assigned = request.form['date_assigned']
            start_date = request.form['start_date']
            assign = Assigned(fk_job=id, fk_employee=employee,
                              date_assigned=date_assigned, start_date=start_date)
            db.session.add(assign)
            db.session.commit()
            return redirect(url_for('manager_blueprint.manage_jobs'))
        return render_template('manager/assign-job.html', success=false, form=form, employees=employee_list)
    else:
        return redirect(url_for('employee_blueprint.employee_index'))

# @blueprint.route('/manager/manage-complaints')
# @login_required
# def manage_complaints():
#     user = Users.query.filter_by(id=current_user.id).first()
#     if user.manager == True:
#         complaints = Complaint.query.filter(Complaint.fk_resident != None).all()
#         return render_template('manager/complaints.html',jobs_complaints=complaints)        
#     else:
#         return redirect(url_for('employee_blueprint.employee_index'))

# @blueprint.route('/manager/view-complaints/<string:trn>/<string:resident>/<string:date>')
# @login_required
# def view_complaints(trn,resident,date):
#     user = Users.query.filter_by(TRN=current_user.TRN).first()
#     if user.manager == True:
#         complaints = Complaint.query.filter_by(fk_job=trn, fk_resident=resident,date=date).first()
#         job = complaints.fk_job
#         date = complaints.date
#         resident = complaints.fk_resident
#         complaint = complaints.content
#         return render_template('manager/view-complaints.html', job=job,date=date,resident=resident,complaint=complaint)
#     else:
#         return redirect(url_for('employee_blueprint.employee_index'))

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('error/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('error/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('error/page-500.html'), 500
