import allure
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from mysql.models import TestUser


class MySQLClient:

    def __init__(self, user='root', password='admin',
                 db_name='DB_MYAPP', host='0.0.0.0', port='3306'):

        self.user = user
        self.password = password
        self.db_name = db_name
        self.host = host
        self.port = port

        self.connection = self.connect()
        self.session = sessionmaker(bind=self.connection)()

    def connect(self):
        engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}',
            encoding='utf8'
        )

        return engine.connect()

    @allure.step("Запрос из БД пользователя {username}")
    def select_by_username(self, username):
        return self.session.query(TestUser).filter(TestUser.username == username).first()

    @allure.step("Блокировка доступа для пользователя {username}")
    def drop_access_by_username(self, username):
        user = self.session.query(TestUser).filter(TestUser.username == username).first()
        user.access = 0
        self.session.commit()
