import click
from werkzeug.security import generate_password_hash

from src.user.userenums import UserStatus
from src.user.userservice import create_user_db


@click.command('create-superuser', help='Create a superuser before start.')
@click.argument('username')
@click.argument('email')
@click.argument('password')
def create_superuser(username: str, email: str, password: str) -> None:
    for val in [username, email, password]:
        if len(val) not in range(6, 101):
            click.echo(f'Length of {val} not in range 6-100 characters')
            return
    hashed_psw = generate_password_hash(password=password)
    superuser_data = {'username': username,
                      'email': email,
                      'password': hashed_psw,
                      'status': UserStatus.Admin}
    if superuser := create_user_db(user_data=superuser_data):
        click.echo(f'Superuser {superuser.username} {superuser.email} has been created.')
        return
    click.echo('Failed to create superuser.')
