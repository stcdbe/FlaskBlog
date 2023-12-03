from typing import Any
from uuid import UUID

from flask import render_template, redirect, url_for, abort, request
from flask_login import current_user, login_required

from src import app
from src.database.enums import PostType, UserStatus, PostCategory
from src.post.postutils import serialize_post_form, serialize_com_form
from src.post.postwtforms import (ArticleCreateForm,
                                  NewsPostCreateForm,
                                  NewsPostUpdateForm,
                                  ArticleUpdateForm,
                                  CommentCreateForm)
from src.post.postservice import (get_posts_pgn,
                                  get_post_db,
                                  add_post_db,
                                  upd_post_db,
                                  add_com_db,
                                  get_some_posts_db,
                                  search_article_db)


@app.get('/')
def show_main_page() -> Any:
    articles = get_some_posts_db(post_type=PostType.article_post, size=7)
    news = get_some_posts_db(post_type=PostType.news_post, size=10)
    return render_template('post/mainpage.html', articles=articles, news=news)


@app.get('/<posts>')
def show_posts(posts: str) -> Any:
    if ctg := request.args.get('category', type=str):
        if ctg not in set(PostCategory):
            abort(404)
    page = request.args.get('page', default=1, type=int)
    match posts:
        case 'articles':
            pgn = get_posts_pgn(post_type=PostType.article_post, per_page=9, page=page, category=ctg)
            return render_template('post/articles.html', pagination=pgn, ctg=ctg)

        case 'news':
            pgn = get_posts_pgn(post_type=PostType.news_post, per_page=12, page=page, category=ctg)
            return render_template('post/news.html', pagination=pgn, ctg=ctg)

        case _:
            abort(404)


@app.route('/articles/<uuid:article_id>', methods=['GET', 'POST'])
def show_article_detail(article_id: UUID) -> Any:
    article = get_post_db(post_type=PostType.article_post, post_id=article_id)

    if not article:
        abort(404)

    form = CommentCreateForm()
    if form.validate_on_submit():
        com_data = serialize_com_form(form_data=form.data)
        com_data['post_id'] = article.id
        com_data['user_id'] = current_user.id
        add_com_db(post=article, com_data=com_data)
    return render_template('post/articledetail.html', article=article, form=form)


@app.route('/<posts>/create', methods=['GET', 'POST'])
@login_required
def create_post(posts: str) -> Any:
    if current_user.status not in [UserStatus.Author, UserStatus.Admin]:
        abort(403)

    match posts:
        case 'articles':
            form = ArticleCreateForm()
            if form.validate_on_submit():
                article_data = serialize_post_form(form_data=form.data)
                article_data['user_id'] = current_user.id
                add_post_db(post_type=PostType.article_post, post_data=article_data)
                return redirect(url_for('show_posts', posts='articles'))
            return render_template('post/createarticle.html', form=form)

        case 'news':
            form = NewsPostCreateForm()
            if form.validate_on_submit():
                news_post_data = serialize_post_form(form_data=form.data)
                news_post_data['user_id'] = current_user.id
                add_post_db(post_type=PostType.news_post, post_data=news_post_data)
                return redirect(url_for('show_posts', posts='news'))
            return render_template('post/createnewspost.html', form=form)

        case _:
            abort(404)


@app.route('/<posts>/<uuid:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(posts: str, post_id: UUID) -> Any:
    match posts:
        case 'articles':
            post = get_post_db(post_type=PostType.article_post, post_id=post_id)
            if not post:
                abort(404)
            if post.user_id != current_user.id:
                abort(403)
            form = ArticleUpdateForm()
            if form.validate_on_submit():
                article_data = serialize_post_form(form_data=form.data)
                upd_post_db(post=post, upd_data=article_data)
                return redirect(url_for('show_article_detail', article_id=post.id))
            return render_template('post/updatearticle.html', form=form, post=post)

        case 'news':
            post = get_post_db(post_type=PostType.news_post, post_id=post_id)
            if not post:
                abort(404)
            if post.user_id != current_user.id:
                abort(403)
            form = NewsPostUpdateForm()
            if form.validate_on_submit():
                news_post_data = serialize_post_form(form_data=form.data)
                upd_post_db(post=post, upd_data=news_post_data)
                return redirect(url_for('show_posts', posts='news'))
            return render_template('post/updatenewspost.html', form=form, post=post)

        case _:
            abort(404)


@app.get('/search')
def search() -> Any:
    query = request.args.get('q', default='', type=str)
    page = request.args.get('page', default=1, type=int)
    pgn = search_article_db(query=query, page=page)
    return render_template('post/search.html', query=query, pagination=pgn)
