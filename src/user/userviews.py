from typing import Any

from flask import render_template, abort, redirect, url_for, flash, request
from flask_login import login_required, current_user

from src import app
from src.database.enums import UserStatus
from src.user.userservice import get_user_by_username_db, update_user_db, get_users_pgn
from src.user.userutils import serialize_profile_form
from src.user.userwtforms import ProfileUpdateForm


@app.get('/profile/<username>')
def get_user_profile(username: str) -> Any:
    user = get_user_by_username_db(username=username)

    if not user:
        abort(404)

    return render_template('user/profile.html', user=user)


@app.route('/profile/<username>/update', methods=['GET', 'POST'])
@login_required
def update_user_profile(username: str) -> Any:
    user = get_user_by_username_db(username=username)

    if not user:
        abort(404)

    if current_user.id != user.id:
        abort(403)

    form = ProfileUpdateForm()
    if form.validate_on_submit():

        upd_user_data = serialize_profile_form(form_data=form.data)
        upd_user = update_user_db(user=user, upd_data=upd_user_data)

        flash('Profile successfully updated', 'primary')
        return redirect(url_for(endpoint='get_user_profile', username=upd_user.username))

    return render_template('user/updateprofile.html', user=user, form=form)


@app.get('/authors')
def show_authors() -> Any:
    page = request.args.get('page', default=1, type=int)
    pgn = get_users_pgn(user_status=UserStatus.Author, page=page)
    return render_template('user/authors.html', pagination=pgn)
