from uuid import UUID
from datetime import datetime

from flask import render_template, redirect, url_for, abort, request, Response
from flask_login import current_user, login_required

from app import app
from app.database.dbmodels import Article, News, ArticleComment
from app.database.dbfuncs import getpostspgn, getpostbyid, updatepost, addpost, getcomments
from app.posts.postswtforms import ArticleForm, NewsForm, EditNewsForm, EditArticleForm, ArticleCommentForm
from app.utils import savepicture, deletepicture


@app.route('/posts')
def showposts() -> str:
    posts = request.args.get('posts', default='articles', type=str)
    category = request.args.get('category', type=str)
    page = request.args.get('page', default=1, type=int)
    match posts:

        case 'articles':
            pgn = getpostspgn(tablemodel=Article,
                              perpage=9,
                              page=page,
                              category=category)
            return render_template('posts/articles.html',
                                   pagination=pgn,
                                   ctg=category)

        case 'news':
            pgn = getpostspgn(tablemodel=News,
                              perpage=15,
                              page=page,
                              category=category)
            return render_template('posts/news.html',
                                   pagination=pgn,
                                   ctg=category)

        case _:
            abort(404)


@app.route('/articles/<uuid:id>/detail', methods=['GET', 'POST'])
def showarticledetail(id: UUID) -> str | Response:
    article = getpostbyid(tablemodel=Article, postid=id)
    comments = getcomments(articleid=article.id)

    if article:
        form = ArticleCommentForm()
        if form.validate_on_submit():
            data = dict(articleid=article.id,
                        text=form.text.data.strip(),
                        username=current_user.username,
                        date=datetime.utcnow().replace(microsecond=0),)
            addpost(data=data, tablemodel=ArticleComment)
        return render_template('posts/articledetail.html',
                               article=article,
                               comments=comments,
                               form=form)

    abort(404)


@app.route('/create/<post>', methods=['GET', 'POST'])
@login_required
def createpost(post: str) -> str | Response:
    if current_user.status == 'Author' or current_user.status == 'Admin':
        match post:

            case 'article':
                form = ArticleForm()
                if form.validate_on_submit():
                    picname = savepicture(picture=form.picture.data,
                                          imgcatalog='postimages',
                                          size=(900, 400))
                    articledata = dict(picture=picname,
                                       title=form.title.data.strip(),
                                       intro=form.intro.data.strip(),
                                       category=form.category.data,
                                       text=form.text.data.strip(),
                                       username=current_user.username,
                                       date=datetime.utcnow().replace(microsecond=0),)
                    addpost(data=articledata, tablemodel=Article)
                    return redirect(url_for(endpoint='showposts', posts='articles'))
                return render_template('posts/createarticle.html', form=form)

            case 'newspost':
                form = NewsForm()
                if form.validate_on_submit():
                    picname = savepicture(picture=form.picture.data,
                                          imgcatalog='postimages',
                                          size=(900, 400))
                    newsdata = dict(picture=picname,
                                    title=form.title.data.strip(),
                                    category=form.category.data,
                                    text=form.text.data.strip(),
                                    username=current_user.username,
                                    date=datetime.utcnow().replace(microsecond=0),)
                    addpost(data=newsdata, tablemodel=News)
                    return redirect(url_for(endpoint='showposts', posts='news'))
                return render_template('posts/createnewspost.html', form=form)

            case _:
                abort(404)

    abort(404)


@app.route('/edit/<post>/<uuid:id>', methods=['GET', 'POST'])
@login_required
def editpost(post: str, id: UUID) -> str | Response:
    match post:

        case 'article':
            article = getpostbyid(tablemodel=Article, postid=id)
            if article.username == current_user.username:
                form = EditArticleForm()
                if form.validate_on_submit():
                    articledata = dict(title=form.title.data.strip(),
                                       intro=form.intro.data.strip(),
                                       category=form.category.data,
                                       text=form.text.data.strip(),)
                    if form.picture.data:
                        picname = savepicture(picture=form.picture.data,
                                              imgcatalog='postimages',
                                              size=(900, 400))
                        articledata['picture'] = picname
                        deletepicture(imgcatalog='postimages', picname=article.picture)
                    updatedarticle = updatepost(post=article, data=articledata)
                    return redirect(url_for(endpoint='showarticledetail', id=updatedarticle.id))
                return render_template('posts/editarticle.html',
                                       form=form,
                                       post=article)
            abort(404)

        case 'newspost':
            newspost = getpostbyid(tablemodel=News, postid=id)
            if newspost.username == current_user.username:
                form = EditNewsForm()
                if form.validate_on_submit():
                    newsdata = dict(title=form.title.data.strip(),
                                    category=form.category.data,
                                    text=form.text.data.strip(),)
                    if form.picture.data:
                        picname = savepicture(picture=form.picture.data,
                                              imgcatalog='postimages',
                                              size=(900, 400))
                        newsdata['picture'] = picname
                        deletepicture(imgcatalog='postimages', picname=newspost.picture)
                    updatepost(post=newspost, data=newsdata)
                    return redirect(url_for(endpoint='showposts', posts='news'))
                return render_template('posts/editnewspost.html',
                                       form=form,
                                       post=newspost)
            abort(404)

        case _:
            abort(404)
