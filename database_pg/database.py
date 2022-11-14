from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Profile_info(Base):
    __tablename__ = 'profile_info'
    id = Column(Integer, primery_key = True)
    id_who_fav = relationship("Favorite_profile")
    id_that_fav = relationship("Favorite_profile")
    id_who_black = relationship("Black_list")
    id_that_black = relationship("Black_list")

class Favorite_profile(Base):
    __tablename__ = 'favorite_list'
    id = Column(Integer, primery_key = True)
    id_who = Column(Integer, ForeignKey('profile_info.id'))
    id_that = Column(Integer, ForeignKey('profile_info.id'))

class Black_list(Base):
    __tablename__ = 'black_list'
    id = Column(Integer, primery_key = True)
    id_who = Column(Integer, ForeignKey('profile_info.id'))
    id_that = Column(Integer, ForeignKey('profile_info.id'))