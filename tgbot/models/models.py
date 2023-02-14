import uuid
from datetime import datetime, timedelta

from sqlalchemy import Column, VARCHAR, BigInteger, DateTime, Uuid, Integer, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapped_column, joinedload

Base = declarative_base()


class BaseManager:
    def __init__(self, session):
        self.session = session

    def to_dict(self):
        return {
            'session': self.session
        }


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    name = Column(VARCHAR(32), unique=False, nullable=True)
    reg_date = Column(DateTime, default=datetime.now)
    update_date = Column(DateTime, onupdate=datetime.now)

    def __str__(self):
        return str(self.id)


class UserManager(BaseManager):
    async def get_or_create_user(self, id: int, name: str):
        async with self.session() as session:
            async with session.begin():
                user = await session.get(User, id)
                if not user:
                    user = User(id=id, name=name)
                    session.add(user)
                return user


class Periodicity(Base):
    __tablename__ = 'periodicity'

    id = Column(Uuid, unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR(300), unique=False, nullable=True)
    interval = Column(Integer)
    notifications = relationship('Notification', back_populates="periodicity")

    def __str__(self):
        return self.name


class PeriodicityManager(BaseManager):
    async def create(self, name, interval):
        async with self.session() as session:
            async with session.begin():
                periodicity = Periodicity(name=name, interval=interval)
                session.add(periodicity)
                return periodicity

    async def get_all(self):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Periodicity))
                result = result.scalars().all()
                return result

    async def get(self, id):
        async with self.session() as session:
            async with session.begin():
                return await session.get(Periodicity, id)


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Uuid, unique=True, nullable=False, primary_key=True, default=uuid.uuid4)
    name = Column(VARCHAR(250), unique=False, nullable=True)
    description = Column(VARCHAR(1000))
    first_date = Column(DateTime, default=datetime.now)
    next_data = Column(DateTime, nullable=True)
    periodicity_id = mapped_column(ForeignKey(Periodicity.id))
    periodicity= relationship('Periodicity', back_populates="notifications")
    user = Column(ForeignKey(User.id))

    def __str__(self):
        return self.name


class NotificationManager(BaseManager):
    async def create(self, name, description, date, periodicity_id, user):
        async with self.session() as session:
            async with session.begin():
                date = datetime.strptime(date, '%Y-%m-%d %H:%M')
                next_date = date
                notification = Notification(name=name,
                                            description=description,
                                            first_date=date,
                                            next_data=next_date,
                                            periodicity_id=periodicity_id,
                                            user=user)
                session.add(notification)
                return notification

    async def get_all(self):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Notification).options(
                    joinedload(Notification.periodicity)).join(Periodicity, Notification.periodicity_id == Periodicity.id))
                result = result.scalars().all()
                return result

    async def update_next_data(self, id, next_data):
        async with self.session() as session:
            async with session.begin():
                notification = await session.get(Notification, id)
                if not notification:
                    return None
                notification.next_data = next_data
                session.add(notification)
                return notification

    async def get_users_all(self, user_id):
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Notification).where(Notification.user==user_id).options(joinedload(Notification.periodicity))
                .join(Periodicity, Notification.periodicity_id == Periodicity.id))

                result = result.scalars().all()
                return result

    async def delete(self, id, user_id) -> bool:
        async with self.session() as session:
            async with session.begin():
                notification = await session.execute(select(Notification).where(Notification.user == user_id, Notification.id == id))
                notification = notification.scalar_one_or_none()
                if notification:
                    await session.delete(notification)
                    return True
                return False



