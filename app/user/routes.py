import sys
from app.user import blueprint
from flask import redirect, render_template, request, url_for
from app.models import Complaint, Resident
from app import db
from app.user.forms import ComplaintForm


@blueprint.route('/index')
@blueprint.route('/')
def index():
    return render_template('user/index.html', segment='index')


@blueprint.route('/complaints', methods=['Get', 'POST'])
def complaint_page():
    form = ComplaintForm(request.form)
    if 'add' in request.form:

        form_email = request.form['email_address']
        form_job = request.form['job_id']
        form_complaint = request.form['complaint']
        form_first_name = request.form['first_name']
        form_last_name = request.form['last_name']
        form_street_num = request.form['street_number']
        form_street_name = request.form['street_name']
        form_city = request.form['city']
        form_parish = request.form['parish']
        form_date = request.form['date']

        resident_chk = Resident.query.filter_by(email=form_email).first()
        print(f'Read resident ?', file=sys.stderr)
        if resident_chk:
            print('Check Passed', file=sys.stderr)
            resident_complaint = Complaint(
                fk_resident=form_email, fk_job=form_job, date=form_date, content=form_complaint)
            db.session.add(resident_complaint)
            db.session.commit()
        else:
            print('New Resident', file=sys.stderr)
            if form_street_num == '':
                resident = Resident(email=form_email, first_name=form_first_name,
                                    last_name=form_last_name, street_name=form_street_name, city=form_city, parish=form_parish)
            else:
                resident = Resident(email=form_email, first_name=form_first_name, last_name=form_last_name,
                                    street_num=form_street_num, street_name=form_street_name, city=form_city, parish=form_parish)

            resident_complaint = Complaint(
                fk_resident=form_email, fk_job=form_job, date=form_date, content=form_complaint)
            db.session.add(resident)
            db.session.add(resident_complaint)
            db.session.commit()

            return redirect(url_for('user_blueprint.index'))
    else:
        return render_template('user/complaints.html', segment='Complaints', form=form)

# Errors


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('error/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('error/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('error/page-500.html'), 500
