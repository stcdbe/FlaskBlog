from typing import Any

from flask import Blueprint, render_template, abort, redirect, url_for, flash, request
from flask_login import login_required, current_user

from src.database.enums import UserStatus
from src.user.userservice import get_user_by_username_db, update_user_db, get_users_pgn
from src.user.userutils import prepare_profile_data
from src.user.userwtforms import ProfileUpdateForm
from src.utils import delete_picture


user_router = Blueprint('users',
                        __name__,
                        static_folder='static',
                        template_folder='templates',
                        url_prefix='/users')


@user_router.get('/<username>')
def get_user_profile(username: str) -> Any:
    user = get_user_by_username_db(username=username)

    if not user:
        abort(404)

    return render_template('user/profile.html', user=user)


@user_router.route('/<username>/update', methods=['GET', 'POST'])
@login_required
def update_user_profile(username: str) -> Any:
    user = get_user_by_username_db(username=username)

    if not user:
        abort(404)

    if current_user.id != user.id:
        abort(403)

    form = ProfileUpdateForm()
    if form.validate_on_submit():

        old_pic_name = user.picture
        upd_user_data = prepare_profile_data(form_data=form.data)
        upd_user = update_user_db(user=user, upd_data=upd_user_data)
        if upd_user_data.get('picture'):
            delete_picture(pic_name=old_pic_name, img_catalog='profileimages')
        flash('Profile successfully updated', 'primary')
        return redirect(url_for('users.get_user_profile', username=upd_user.username))

    return render_template('user/updateprofile.html', user=user, form=form)


@user_router.get('/authors')
def show_authors() -> Any:
    page = request.args.get('page', default=1, type=int)
    pgn = get_users_pgn(user_status=UserStatus.Author,
                        page=page,
                        per_page=10)
    return render_template('user/authors.html', pagination=pgn)
