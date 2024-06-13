from http import HTTPMethod, HTTPStatus

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from injector import inject
from werkzeug.wrappers.response import Response

from src.modules.user.models.enums import UserStatus
from src.modules.user.services.services import UserService
from src.modules.user.views.wtforms import ProfileUpdateForm

user_router = Blueprint(
    name="users",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/users",
)


@user_router.get(rule="/<username>")
@inject
def get_user_profile(user_service: UserService, username: str) -> str:
    user = user_service.get_one(username=username)

    if not user:
        abort(code=HTTPStatus.NOT_FOUND)

    return render_template("user/profile.html", user=user)


@user_router.route(rule="/<username>/update", methods=(HTTPMethod.GET, HTTPMethod.POST))
@login_required
@inject
def update_user_profile(user_service: UserService, username: str) -> Response | str:
    user = user_service.get_one(username=username)

    if not user:
        abort(code=HTTPStatus.NOT_FOUND)

    if current_user.id != user.id:
        abort(code=HTTPStatus.FORBIDDEN)

    form = ProfileUpdateForm()
    if form.validate_on_submit():
        user = user_service.update_one(user=user, data=form.data)
        flash("Profile successfully updated", "primary")
        return redirect(url_for("users.get_user_profile", username=user.username))

    return render_template("user/update_profile.html", user=user, form=form)


@user_router.get(rule="/authors")
@inject
def show_authors(user_service: UserService) -> str:
    page = request.args.get(key="page", default=1, type=int)
    pgn = user_service.get_pgn(
        page=page,
        per_page=10,
        order_by="username",
        status=UserStatus.author,
    )
    return render_template("user/authors.html", pagination=pgn)
