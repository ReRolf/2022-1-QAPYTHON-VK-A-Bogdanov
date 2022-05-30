from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TestUser(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(16), default=None, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    access = Column(Integer, default=None)
    active = Column(Integer, default=None)
    start_active_time = Column(DateTime, default=None)

    def __repr__(self):
        return f"<TestUser(id={self.id}, username='{self.username}', password='{self.password}', " \
               f"email='{self.email}', access={self.access}, active={self.active}, " \
               f"start_active_time='{self.start_active_time}')>"
