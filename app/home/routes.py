from flask import render_template, redirect, url_for
from flask_login import current_user

from . import bp


@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile.visit_list'))
    return render_template('home/index.html')

