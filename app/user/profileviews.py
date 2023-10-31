from flask import render_template, abort, Response, redirect, url_for, flash
from flask_login import login_required, current_user

from app import app
from app.database.dbfuncs import getuser, upduserdata
from app.utils import savepicture, deletepicture
from app.user.profilewtforms import EditProfileForm


@app.route('/profile/<username>')
def getprofile(username: str) -> str:
    user = getuser(usernameoremail=username)
    if user:
        return render_template('user/profile.html', user=user)
    abort(404)


@app.route('/profile/<username>/edit', methods=['GET', 'POST'])
@login_required
def editprofile(username: str) -> str | Response:
    user = getuser(usernameoremail=username)
    if current_user.username == user.username:
        form = EditProfileForm()

        if form.validate_on_submit():
            userdata = {'website': form.website.data.strip(),
                        'github': form.github.data.strip(),
                        'twitter': form.twitter.data.strip(),
                        'name': form.name.data.strip(),
                        'position': form.position.data.strip(),
                        'company': form.company.data.strip(),
                        'location': form.location.data.strip()}
            if form.picture.data:
                userdata['picture'] = savepicture(picture=form.picture.data,
                                                  imgcatalog='profileimages',
                                                  size=(250, 250))
                deletepicture(picname=user.picture, imgcatalog='profileimages')
            updateduser = upduserdata(user=user, data=userdata)
            flash('Profile successfully updated', 'primary')
            return redirect(url_for(endpoint='getprofile', username=updateduser.username))

        return render_template('user/editprofile.html', user=user, form=form)

    abort(404)
