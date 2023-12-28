from flask import Flask
from flask.testing import FlaskCliRunner


def test_create_superuser(app: Flask, cli_runner: FlaskCliRunner) -> None:
    command_args = ['create-superuser', 'test_super_user', 'test_super_user@example.com', 'Password123']
    with app.app_context():
        res = cli_runner.invoke(args=command_args)
    assert res.output
    assert command_args[1] in res.output
    assert command_args[2] in res.output
    assert command_args[3] not in res.output
