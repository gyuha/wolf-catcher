import PySide6.QtGui
from lib.Singleton import Singleton
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
import os
from util.Config import Config

Base = declarative_base()


class Product(Base):

    __tablename__ = "product"

    id = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)
    path = Column(String)
    tags = Column(String)
    visible = Column(Boolean, default=False)
    download_count = Column(Integer, default=0)

    def __repr__(self):
        return "<Product(id='{}', title='{}', path='{}', tags='{}', download_count='{})>".format(
            self.id, self.title, self.path, self.tags, self.download_count
        )