from flask import Blueprint, render_template, abort, redirect, url_for, flash, request, Response
from flask_login import login_required, current_user
from injector import inject

from src.user.user_enums import UserStatus
from src.user.user_models import User
from src.user.user_services import UserService
from src.user.user_wtforms import ProfileUpdateForm

user_router = Blueprint(name='users',
                        import_name=__name__,
                        static_folder='static',
                        template_folder='templates',
                        url_prefix='/users')


@user_router.get(rule='/<username>')
@inject
def get_user_profile(user_service: UserService, username: str) -> str:
    user = user_service.get_one(username=username)

    if not user:
        abort(404)

    return render_template('user/profile.html', user=user)


@user_router.route(rule='/<username>/update', methods=['GET', 'POST'])
@login_required
@inject
def update_user_profile(user_service: UserService, username: str) -> Response | str:
    user = user_service.get_one(username=username)

    if not user:
        abort(404)

    if current_user.id != user.id:
        abort(403)

    form = ProfileUpdateForm()
    if form.validate_on_submit():
        upd_user = user_service.update_one(user=user, upd_data=form.data)
        flash('Profile successfully updated', 'primary')
        return redirect(url_for('users.get_user_profile', username=upd_user.username))

    return render_template('user/update_profile.html', user=user, form=form)


@user_router.get(rule='/authors')
@inject
def show_authors(user_service: UserService) -> str:
    page = request.args.get(key='page', default=1, type=int)
    pgn = user_service.get_pgn(page=page,
                               per_page=10,
                               order_by=User.username,
                               status=UserStatus.author)
    return render_template('user/authors.html', pagination=pgn)
