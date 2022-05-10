from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RequestsAmount(Base):
    __tablename__ = 'requests_amount'
    __table_args__ = {'mysql_charset': 'utf8'}

    count = Column(Integer, nullable=False, primary_key=True)

    def __repr__(self):
        return f"<RequestsAmount(count='{self.count}')>"


class RequestsType(Base):
    __tablename__ = 'requests_type'
    __table_args__ = {'mysql_charset': 'utf8'}

    request_type = Column(String(1000), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<RequestsType(request_type='{self.request_type}', count='{self.count}')>"


class RequestsTop(Base):
    __tablename__ = 'requests_top'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    # максимальная длина URL - 2048 в зависимости от браузера
    # максимальная длина URI не ограничена, но серверы вернут 414 на строку более 2к символов
    url = Column(String(2048), nullable=False)
    count = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<RequestsTop(id='{self.id}', url='{self.url}', count='{self.count}')>"


class Requests400(Base):
    __tablename__ = 'requests_400'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(2048), nullable=False)
    size = Column(Integer, nullable=False)
    # максимальная длина Ipv6 больше чем Ipv4 и составляет 39 символов, но Ipv4 отображаемый в Ipv6 - 45 символов
    ip = Column(String(45), nullable=False)

    def __repr__(self):
        return f"<Requests400(id='{self.id}', url='{self.url}', size='{self.size}', ip='{self.ip}')>"


class Requests500(Base):
    __tablename__ = 'requests_500'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(45), nullable=False)
    requests_number = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Requests500(id='{self.id}', ip='{self.ip}', requests_number='{self.requests_number}')>"
