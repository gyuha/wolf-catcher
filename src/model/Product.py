import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
    select,
)
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from util.Config import Config

from model.Base import Base


class Product(Base):

    __tablename__ = "product"

    id = Column(String, primary_key=True)
    site = Column(String)
    title = Column(String)
    author = Column(String)
    path = Column(String)
    tags = Column(String)
    visible = Column(Boolean, default=False)
    download_count = Column(Integer, default=0)
    at = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return "<Product(id='{}', title='{}', path='{}', tags='{}', download_count='{})>".format(
            self.id, self.title, self.path, self.tags, self.download_count
        )
