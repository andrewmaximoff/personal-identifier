from flask import redirect, url_for, render_template, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app.utils.dropbox_helpers import upload_user_picture

from . import bp


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    if form.validate_on_submit():
        user = User.query.filter_by(name_lower=form.name.data.lower()).first()

        if not user or not user.check_password(form.password.data):
            return render_template('auth/login.html', form=form, error_log='Invalid login or password')

        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully.')
        return redirect(url_for('home.index'))

    return render_template('auth/login.html', form=form)


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
            admin=form.admin.data,
        )
        file = form.user_picture.data
        db.session.add(user)
        db.session.commit()
        if file:
            upload_user_picture(file, user)
        flash('Thanks for registering!')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', form=form, admin=True)


@bp.route('/')
def index():
    return redirect(url_for('auth.login'))
