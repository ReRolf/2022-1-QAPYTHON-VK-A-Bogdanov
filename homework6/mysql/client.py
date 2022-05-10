import sqlalchemy
from models.models import Base
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker


class MySQLClient:

    def __init__(self, host, port, user, password, db_name):
        self.host = host
        self.port = port
        self.user = user
        self.db_name = db_name
        self.password = password

        self.engine = None
        self.session = None
        self.connection = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        self.session = sessionmaker(bind=self.connection.engine, autocommit=True)()

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def create_table(self, *table_name):
        for _ in table_name:
            if not inspect(self.engine).has_table(f'{_}'):
                Base.metadata.tables[f'{_}'].create(self.engine)

    def execute_query(self, query, fetch=False):
        response = self.connection.execute(query)
        if fetch:
            return response.fetchall()
