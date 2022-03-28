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
    if 'POST' in request.method:
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
        if Resident.query.filter_by(email=form_email).first():
            resident_complaint = Complaint(
                fk_resident=form_email, fk_job=form_job, date=form_date, content=form_complaint)
            db.session.add(resident_complaint)
            db.session.commit()
        else:
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
            return redirect(url_for('home_blueprint.index'))
    else:
        return render_template('user/complaints.html', segment='Complaints', form=form)
