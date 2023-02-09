import uuid
from datetime import datetime

from sqlalchemy import Column, VARCHAR, BigInteger, DateTime, Uuid, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseManager:
    def __init__(self, session):
        self.session = session


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    name = Column(VARCHAR(32), unique=False, nullable=True)
    reg_date = Column(DateTime, default=datetime.now)
    update_date = Column(DateTime, onupdate=datetime.now)

    def __str__(self):
        return f'user: {self.id}'


class UserManager(BaseManager):
    async def create(self, name):
        user = User(name=name)
        self.session.add(user)
        self.session.commit()
        return user

    async def delete(self, user_id):
        user = self.session.query(User).get(user_id)
        self.session.delete(user)
        self.session.commit()

    async def get_or_create_user(self, id: int, name: str):
        async with self.session() as session:
            async with session.begin():
                user = await session.get(User, id)
                if not user:
                    print('___CREATE USER___')
                    user = User(id=id, name=name)
                    session.add(user)
                return user


class Periodicity(Base):
    __tablename__ = 'periodicity'

    id = Column(Uuid, unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR(300), unique=False, nullable=True)
    interval = Column(Integer)

    def __str__(self):
        return self.name


class PeriodicityManager(BaseManager):
    async def create(self, name, interval):
        async with self.session() as session:
            async with session.begin():
                periodicity = Periodicity(name=name, interval=interval)
                session.add(periodicity)
                return periodicity


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Uuid, unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR(300), unique=False, nullable=True)
    first_date = Column(DateTime)
    next_data = Column(DateTime)
    periodicity = Column(ForeignKey(Periodicity.id))
    user = Column(ForeignKey(User.id))

    def __str__(self):
        return self.name
