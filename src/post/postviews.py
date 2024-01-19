from typing import Any

from flask import render_template, redirect, url_for, abort, request, Blueprint, flash
from flask_login import current_user, login_required

from src.database.enums import PostGroup, UserStatus, PostCategory
from src.post.postservice import (get_posts_pgn,
                                  create_post_db,
                                  upd_post_db,
                                  create_com_db,
                                  del_post_db,
                                  get_post_by_slug_db)
from src.post.postutils import prepare_post_data, prepare_com_data
from src.post.postwtforms import PostCreateForm, PostUpdateForm, CommentCreateForm
from src.utils import delete_picture


post_router = Blueprint('posts',
                        __name__,
                        static_folder='static',
                        template_folder='templates',
                        url_prefix='/posts')


@post_router.get('')
def show_posts() -> Any:
    post_group = request.args.get('post_group', type=str)
    ctg = request.args.get('category', type=str)
    page = request.args.get('page', default=1, type=int)

    if ctg:
        if ctg not in set(PostCategory):
            abort(404)

    match post_group:
        case PostGroup.articles:
            template = 'post/articles.html'
            per_page = 9
        case PostGroup.news:
            template = 'post/news.html'
            per_page = 12
        case _:
            abort(404)

    pgn = get_posts_pgn(post_group=PostGroup(post_group),
                        per_page=per_page,
                        page=page,
                        category=ctg)
    return render_template(template, pagination=pgn, ctg=ctg)


@post_router.route('/create', methods=['GET', 'POST'])
@login_required
def create_post() -> Any:
    if current_user.status not in {UserStatus.Author, UserStatus.Admin}:
        abort(403)

    form = PostCreateForm()
    if form.validate_on_submit():
        post_data = prepare_post_data(form_data=form.data, creator_id=current_user.id)
        if new_post := create_post_db(post_data=post_data):
            return redirect(url_for('posts.show_posts', post_group=new_post.group.value))

        flash('Post title must be unique.', 'primary')
    return render_template('post/createpost.html', form=form)


@post_router.route('/<post_slug>', methods=['GET', 'POST'])
def show_post_detail(post_slug: str) -> Any:
    post = get_post_by_slug_db(post_slug=post_slug)

    if not post:
        abort(404)

    if post.group == PostGroup.articles:
        form = CommentCreateForm()
        if form.validate_on_submit():
            if not current_user.is_authenticated:
                abort(403)
            com_data = prepare_com_data(form_data=form.data,
                                        post_id=post.id,
                                        creator_id=current_user.id)
            create_com_db(post=post, com_data=com_data)
    else:
        form = None

    return render_template('post/articledetail.html', post=post, form=form)


@post_router.route('/<post_slug>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_slug: str) -> Any:
    post = get_post_by_slug_db(post_slug=post_slug)

    if not post:
        abort(404)

    if post.user_id != current_user.id:
        abort(403)

    form = PostUpdateForm(group=post.group.name)
    if form.validate_on_submit():

        old_pic_name = post.picture
        upd_post_data = prepare_post_data(form_data=form.data,
                                          creator_id=current_user.id)
        if upd_post := upd_post_db(post=post, upd_data=upd_post_data):
            if upd_post_data.get('picture'):
                delete_picture(pic_name=old_pic_name, img_catalog='postimages')
            return redirect(url_for('posts.show_posts', post_group=upd_post.group.value))

        flash('Post title must be unique.', 'primary')
    return render_template('post/updatepost.html', form=form, post=post)


@post_router.post('/<post_slug>/delete')
@login_required
def delete_post(post_slug: str) -> Any:
    post = get_post_by_slug_db(post_slug=post_slug)

    if not post:
        abort(404)

    if post.user_id != current_user.id:
        abort(403)

    del_post_db(post=post)
    delete_picture(pic_name=post.picture, img_catalog='postimages')
    return redirect(url_for('posts.show_posts', post_group=post.group.value))


@post_router.get('/search')
def search() -> Any:
    query = request.args.get('q', default='', type=str)
    page = request.args.get('page', default=1, type=int)
    pgn = get_posts_pgn(post_group=PostGroup.articles,
                        per_page=10,
                        page=page,
                        search_query=query)
    return render_template('post/search.html', query=query, pagination=pgn)
