from flask import render_template, redirect, url_for, abort, request, Blueprint, flash, Response
from flask_login import current_user, login_required
from injector import inject

from src.post.post_enums import PostGroup, PostCategory
from src.post.post_exceptions import InvalidPostDataError
from src.post.post_models import Post
from src.post.post_services import PostService, CommentService
from src.post.post_wtforms import PostCreateForm, PostUpdateForm, CommentCreateForm
from src.user.user_enums import UserStatus

post_router = Blueprint(name='posts',
                        import_name=__name__,
                        static_folder='static',
                        template_folder='templates',
                        url_prefix='/posts')


@post_router.get(rule='')
@inject
def show_posts(post_service: PostService) -> str:
    group = request.args.get(key='post_group', default=PostGroup.articles, type=PostGroup)
    current_category = request.args.get(key='category', type=PostCategory)
    page = request.args.get(key='page', default=1, type=int)

    match group:
        case PostGroup.articles:
            template = 'post/articles.html'
            per_page = 9
        case PostGroup.news:
            template = 'post/news.html'
            per_page = 12
        case _:
            abort(code=404)

    filters = {'group': group}
    if current_category:
        filters['category'] = current_category

    pgn = post_service.get_pgn(per_page=per_page,
                               page=page,
                               order_by=Post.created_at.desc(),
                               **filters)
    return render_template(template,
                           pagination=pgn,
                           current_category=current_category,
                           categories=PostCategory)


@post_router.route(rule='/<post_slug>', methods=['GET', 'POST'])
@inject
def show_post_detail(post_service: PostService,
                     comment_service: CommentService,
                     post_slug: str) -> str:
    post = post_service.get_one(slug=post_slug)

    if not post:
        abort(code=404)

    form = CommentCreateForm()
    if form.validate_on_submit():

        if not current_user.is_authenticated:
            abort(403)

        if post.group != PostGroup.articles:
            abort(404)

        comment_service.create_one(post_id=post.id,
                                   creator_id=current_user.id,
                                   com_data=form.data)

    return render_template('post/post_detail.html',
                           post=post,
                           form=form,
                           categories=PostCategory)


@post_router.route(rule='/create', methods=['GET', 'POST'])
@login_required
@inject
def create_post(post_service: PostService) -> Response | str:
    if current_user.status not in {UserStatus.author, UserStatus.admin}:
        abort(code=403)

    form = PostCreateForm()
    if form.validate_on_submit():
        try:
            new_post = post_service.create_one(post_data=form.data, creator_id=current_user.id)

        except InvalidPostDataError as exc:
            flash(f'{exc}', 'primary')

        else:
            return redirect(url_for('posts.show_posts', post_group=new_post.group))

    return render_template('post/create_post.html', form=form)


@post_router.route(rule='/<post_slug>/update', methods=['GET', 'POST'])
@login_required
@inject
def update_post(post_service: PostService, post_slug: str) -> Response | str:
    post = post_service.get_one(slug=post_slug)

    if not post:
        abort(code=404)

    if post.creator_id != current_user.id:
        abort(code=403)

    form = PostUpdateForm(group=post.group.name)
    if form.validate_on_submit():
        try:
            upd_post = post_service.update_one(post=post, upd_data=form.data)

        except InvalidPostDataError as exc:
            flash(f'{exc}', 'primary')

        else:
            return redirect(url_for('posts.show_posts', post_group=upd_post.group))

    return render_template('post/update_post.html', form=form, post=post)


@post_router.post(rule='/<post_slug>/delete')
@login_required
@inject
def delete_post(post_service: PostService, post_slug: str) -> Response:
    post = post_service.get_one(slug=post_slug)

    if not post:
        abort(code=404)

    if post.creator_id != current_user.id:
        abort(code=403)

    post_service.del_one(post=post)
    return redirect(url_for('posts.show_posts', post_group=post.group.value))


@post_router.get(rule='/search')
@inject
def search(post_service: PostService) -> str:
    query = request.args.get(key='q', default='', type=str)
    page = request.args.get(key='page', default=1, type=int)
    pgn = post_service.get_pgn(per_page=12,
                               page=page,
                               order_by=Post.created_at.desc(),
                               query=query)
    return render_template('post/search.html', query=query, pagination=pgn)
