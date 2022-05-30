import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import Table

import mysql.models as models


class MysqlClient:

    def __init__(self, db_name, user, password):
        self.user = 'root'
        self.port = 3306
        self.password = 'pass'
        self.host = '127.0.0.1'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None
        self.table: Table = models.Base.metadata.tables["test_users"]

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}', encoding='utf8',
            max_overflow=5)
        self.connection = self.engine.connect()
        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def insert(self, user_data):
        self.connect()
        self.connection.execute(self.table.insert().values(user_data))
        self.connection.close()

    def delete(self, username: str):
        self.connect()
        self.connection.execute(self.table.delete().where(self.table.c.username == username))
        self.connection.close()

    def get_row(self, username) -> list:
        self.connect()
        self.session.commit()
        fields = self.session.execute(select(self.table).filter(self.table.c.username == username))
        self.connection.close()
        return [i._asdict() for i in fields]

    def update(self, user_data, username):
        self.connect()
        self.connection.execute(self.table.update().values(user_data).where(self.table.c.username == username))
        self.connection.close()
