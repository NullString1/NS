from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import table
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from .models import User
from .main import getTabs
from . import db
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html', tabs=getTabs())


@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()



    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')

        return redirect(url_for('auth.login'))


    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html', tabs=getTabs())


@auth.route('/signup', methods=['POST'])
def signup_post():

    username = request.form.get('username')
    password = request.form.get('password')


    user = User.query.filter_by(username=username).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))


    new_user = User(username=username, password=generate_password_hash(
        password, method='sha256'), auth_level=1)


    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
