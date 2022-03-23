from app.user import blueprint
from flask import redirect, render_template, request, url_for
from app.models import Complaint,Resident
from app import db
from app.user.forms import ComplaintForm


@blueprint.route('/complaints', methods=['Get', 'POST'])
def complaint_page():
    form = ComplaintForm(request.form)
    if 'add' in request.form:
        form_email = request.form['email_address']
        form_job = request.form['job_id']
        form_complaint = request.form['complaint']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        street_num = request.form['street_number']
        street_name = request.form['street_name']
        city = request.form['city']
        parish = request.form['parish']
        date= request.form['date']
        if Resident.query.filter_by(email=form_email).first():
            resident_complaint = Complaint(
                fk_resident=form_email, fk_job=form_job,date=date, content=form_complaint)
            db.session.add(resident_complaint)
            db.session.commit()
        else:
            if street_num == '':
                resident = Resident(email=form_email,first_name=first_name,last_name=last_name,street_name=street_name,city=city,parish=parish)
            else:
                resident = Resident(email=form_email,first_name=first_name,last_name=last_name,street_num=street_num,street_name=street_name,city=city,parish=parish)

            resident_complaint = Complaint(
                fk_resident=form_email, fk_job=form_job, date=date, content=form_complaint)
            db.session.add(resident)
            db.session.add(resident_complaint)
            db.session.commit()
            return redirect(url_for('home_blueprint.index'))
    else:
        return render_template('home/complaint.html', form=form)