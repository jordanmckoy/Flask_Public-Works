from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from app import db, login_manager
from app.auth import blueprint
from app.auth.forms import LoginForm, CreateAccountForm
from app.models import Users,Employee
from app.auth.util import verify_pass
import sys

@blueprint.route('/login')
def route_default():
    return redirect(url_for('auth_blueprint.login'))

# Login & Registration

@blueprint.route('/auth/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        form_id = request.form['trn']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(trn=form_id).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            print("Logged In" , file=sys.stderr)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('auth/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('auth/login.html',
                               form=login_form)

    return redirect(url_for('employee_blueprint.employee_index'))

@blueprint.route('/auth/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        form_user = request.form['trn']
        form_email = request.form['email']
        form_password = request.form['password']

        # Check usename exists
        user = Users.query.filter_by(trn=form_user).first()
        employee = Employee.query.filter_by(trn=form_user).first()
        if user:
            return render_template('auth/register.html',
                                   msg='TRN already registered',
                                   success=False,
                                   form=create_account_form)
        if not employee:
            return render_template('auth/register.html',
                                   msg=f'{form_user}, Is not an employee',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=form_email).first()
        if user:
            return render_template('auth/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(trn=form_user,email=form_email,password=form_password)
        db.session.add(user)
        db.session.commit()

        return render_template('auth/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('auth/register.html', form=create_account_form)


@blueprint.route('/auth/logout')
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('error/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('error/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('error/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('error/page-500.html'), 500