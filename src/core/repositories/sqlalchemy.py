from flask_sqlalchemy import SQLAlchemy
from injector import inject


class SQLAlchemyRepository:
    db: SQLAlchemy

    @inject
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db
