# Flask Blog Website  
___
### Description
Blog web application based on Flask framework with systems of verification, password recovery, administration, user's profile, creating and updating posts.
Application can be launched as Docker container.
![](img/mainpage.png)
![](img/articles.png)
![](img/articledetail.png)
![](img/profile.png)
___
### Getting Started
#### Running on Local Machine
+ install dependencies using PIP
````
$ pip install -r requirements.txt 
````
+ configure environment variables in `.env` file
+ add app entrypoint
````
$ set FLASK_APP=wsgi.py
````
+ create tables in database
````
$ flask db upgrade
````
+ (optional) create superuser
````
$ flask create-superuser [OPTIONS] USERNAME EMAIL PASSWORD
````
+ start app in virtual environment
````
$ gunicorn -c gunicorn.conf.py wsgi:app
````
#### Launch in Docker
+ configure environment variables in `.env` file
+ building the docker image
````
$ docker compose build
````
+ start service
````
$ docker compose up -d
````
____
#### Environment variables
| variables                 | description                                          |
|:--------------------------|:-----------------------------------------------------|
| `PORT`                    | application port                                     |
| `SECRET_KEY`              | a secret key for securely signing the session cookie |
| `CSRF_SECRET_KEY`         | CSRF secret key                                      |
| `PG_USER`                 | PostgreSQL user                                      |
| `PG_HOST`                 | hostname or an IP address PostgreSQL database        |
| `PG_PORT`                 | PostgreSQL database port                             |
| `PG_DB`                   | PostgreSQL database name                             |
| `PG_PASSWORD`             | PostgreSQL database password                         |
| `EMAIL_SMTP_SERVER`       | email SMTP server                                    |
| `EMAIL_PORT`              | email port                                           |
| `EMAIL_USERNAME`          | email address                                        |
| `EMAIL_PASSWORD`          | email password                                       |
| `RESET_PSW_TOKEN_EXPIRES` | reset password token lifetime in minutes             |
| `RECAPTCHA_PUBLIC_KEY`    | reCAPTCHA V2 public key                              |
| `RECAPTCHA_PRIVATE_KEY`   | reCAPTCHA V2 private key                             |
____
#### Tech Stack
+ `Flask`
+ `Flask-SQLAlchemy` and `Flask-Migrate`
+ `Flask-Login`
+ `Flask-WTF`
+ `Flask-RedMail`
+ `Flask-JWTManager`
+ `Pillow`
+ `gunicorn`