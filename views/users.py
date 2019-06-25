from flask import Blueprint, session, url_for, request, render_template, redirect
from models.user import User, UserErrors


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/users/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email, password)
            session['email'] = email
            return email
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/register.html')


@user_blueprint.route('/users/login', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                text = 'welcome, {} you are now logged in'.format(email)
                return render_template('users/user_login.html', text1=text)
        except UserErrors.UserError as e:
            return e.message

    return render_template('users/user_login.html')


@user_blueprint.route('/users/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('users.login_user'))
