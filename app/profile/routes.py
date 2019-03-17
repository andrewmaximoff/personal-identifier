from flask import (
    render_template,
    request,
    redirect,
    flash,
    current_app,
    url_for,
    abort
)
from flask_login import login_required, current_user

from app import db
from app.models import Family, User, Visit
from .forms import (
    UserProfileUpdateForm,
    FamilyProfileUpdateForm,
    NewUserForm,
    DeleteUserForm
)
from . import bp
from app.utils.dropbox_helpers import (
    upload_user_picture,
    upload_family_picture
)


@bp.route('/user', methods=['GET', 'POST'])
@login_required
def update_user_profile():
    form = UserProfileUpdateForm(obj=current_user)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        file = form.user_picture.data
        upload_user_picture(file, current_user)
        db.session.commit()
        flash('Your profile has been updated!')
    return render_template('profile/edit_user_profile.html', form=form, user_picture=current_user.get_picture_url)


@bp.route('/family', methods=['GET', 'POST'])
@login_required
def family():
    form = FamilyProfileUpdateForm()
    user_family = current_user.family

    if not user_family:
        user_family = Family()
        user_family.users.append(current_user)
        db.session.add(user_family)
        db.session.commit()

    page = request.args.get('page', 1, type=int)
    users = user_family.users.order_by(User.datetime.asc()).paginate(
        page, current_app.config['USER_PER_PAGE'], False)

    next_url = url_for('profile.family', page=users.next_num) \
        if users.has_next else None
    prev_url = url_for('profile.family', page=users.prev_num) \
        if users.has_prev else None

    if form.validate_on_submit():
        file = form.family_picture.data
        if file:
            upload_family_picture(file, user_family)
        db.session.commit()
        flash('Family profile has been updated!')
    return render_template('profile/edit_family_profile.html',
                           form=form,
                           family_picture=user_family.get_picture_url,
                           users=users.items,
                           next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    if not current_user.admin:
        abort(404)

    form = NewUserForm()

    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
            admin=form.admin.data,
        )
        new_user.family_id = current_user.family_id
        file = form.user_picture.data
        db.session.add(new_user)
        db.session.commit()
        if file:
            upload_user_picture(file, new_user)
        db.session.commit()
        flash('Member has been created!')
        return redirect(url_for('profile.family'))
    return render_template('profile/add_new_member.html', form=form)


@bp.route('/user/<uuid:user_id>', methods=['GET'])
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(str(user_id))

    page = request.args.get('page', 1, type=int)
    visits = user.visits.order_by(Visit.visit_date.asc()).paginate(
        page, current_app.config['USER_PER_PAGE'], False)

    next_url = url_for('profile.user_profile', user_id=user_id, page=visits.next_num) \
        if visits.has_next else None
    prev_url = url_for('profile.user_profile', user_id=user_id, page=visits.prev_num) \
        if visits.has_prev else None

    return render_template(
        'profile/user_profile.html',
        user=user,
        visits=visits.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route('/visit', methods=['GET'])
@login_required
def visit_list():
    user_family = current_user.family

    if not user_family:
        user_family = Family()
        user_family.users.append(current_user)
        db.session.add(user_family)
        db.session.commit()

    page = request.args.get('page', 1, type=int)

    visits = user_family.visits.order_by(Visit.visit_date.desc()).paginate(
        page, current_app.config['USER_PER_PAGE'], False)

    next_url = url_for('profile.visit_list', page=visits.next_num) \
        if visits.has_next else None
    prev_url = url_for('profile.visit_list', page=visits.prev_num) \
        if visits.has_prev else None

    return render_template('profile/visit_list.html',
                           visits=visits.items,
                           next_url=next_url,
                           prev_url=prev_url)


@bp.route('/visit/<uuid:visit_id>', methods=['GET'])
@login_required
def visit_profile(visit_id):
    visit = Visit.query.get_or_404(str(visit_id))
    return render_template('profile/visit_profile.html', visit=visit)


@bp.route('/user/<uuid:user_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if not current_user.admin:
        abort(404)

    form = DeleteUserForm()
    user = User.query.get_or_404(str(user_id))
    if form.validate_on_submit():
        if user.name == form.name.data:
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('profile.family'))
        return render_template('profile/delete_user.html', form=form, user=user, error=True)
    return render_template('profile/delete_user.html', form=form, user=user)
