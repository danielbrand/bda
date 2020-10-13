from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect

from src.models.analytics.analytics import Dataset
from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators

__author__ = 'jslvtr'


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for(".user_datasets"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.html")  # Send the user an error if their login was invalid


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for(".user_datasets"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.html")  # Send the user an error if their login was invalid


@user_blueprint.route('/datasets')
@user_decorators.requires_login
def user_datasets():
    overview_list = Dataset.retrieve_data()
    overview_list_user = [d for d in overview_list if d.get('user_email') == session['email']]
    return render_template("users/datasets.html", overview_list_user=overview_list_user)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route('/check_alerts/<string:user_id>')
@user_decorators.requires_login
def check_user_alerts(user_id):
    pass
