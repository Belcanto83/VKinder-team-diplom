"""Модели таблиц базы данных проекта VKinder"""
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

""" Таблица с пользователями бота """

class User(Base):
    __tablename__ = "public.user"
    user_id = sa.Column(sa.Integer, primary_key=True)
    # user = relationship("User", foreign_keys=[user_id])
    def __str__(self):
        return f"Пользователь бота с VK_ID: {self.user_id}"

""" Таблица с флагами, которые проставляет пользователь при выводе профиля
    0 - favorite list
    1 - black list """

class Mark(Base):
    __tablename__ = "public.mark"
    mark_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=50), nullable=False)
    def __str__(self):
        return f"Отметка '{self.mark_id}' - {self.name}"

""" Таблица с записями кого пользователь добавил в favorite list или black list """

class UserMark(Base):
    __tablename__ = "public.user_mark"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("public.user.user_id"), nullable=False)
    marked_user_id = sa.Column(sa.Integer, nullable=False)
    mark_id = sa.Column(sa.Integer, sa.ForeignKey("public.mark.mark_id"), nullable=False)
    # __table_args__ = (sa.PrimaryKeyConstraint("user_id", "marked_user_id"),)

    user = relationship("User", backref='public.user_mark')
    mark = relationship("Mark", backref='public.user_mark')

    # user = relationship("User", foreign_keys=[user_id])
    # mark = relationship("Mark", foreign_keys=[mark_id])

    def __str__(self):
        return f"Отметка '{self.mark_id}', поставленная пользователем {self.user_id} пользователю {self.marked_user_id}"



# class ViewHistory(Base):
#     __tablename__ = "view_history"
#     view_id = sa.Column(sa.Integer, primary_key=True)
#     viewer_id = sa.Column(sa.Integer, sa.ForeignKey("user.user_id"), nullable=False)
#     viewed_id = sa.Column(sa.Integer, nullable=False)
#     view_date = sa.Column(sa.DateTime, nullable=False)

#     viewer = relationship("User", foreign_keys=[viewer_id])

#     def __str__(self):
#         return f"Просмотр ID {self.viewed_id}: Пользователь {self.viewer_id} посмотрел пользователя {self.viewed_id} " \
#                f"{self.view_date}"