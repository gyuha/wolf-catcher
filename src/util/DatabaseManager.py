import PySide6.QtGui
from lib.Singleton import Singleton
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
import os
from model.Base import Base
from model.Product import Product
from util.Config import Config


class DatabaseManager(metaclass=Singleton):
    def __init__(self):
        super(DatabaseManager, self).__init__()
        config = Config()
        self.engine = create_engine(config.setting["db"], echo=True, future=True)
        self.session = Session(bind=self.engine)
        print("📢[DatabaseManager.py:13]: ", config.setting["db"])

        Base.metadata.create_all(self.engine)

        self.insert_product("123", "제목", "asdf", "path", "test,asdf")
        self.get_product("123")

    def insert_product(
        self, id, title, author, path, tags, visible=True, download_count=0
    ):
        product = Product(
            id=id,
            title=title,
            author=author,
            path=path,
            tags=tags,
            visible=visible,
            download_count=download_count,
        )
        self.session.add(product)
        self.session.commit()

    def get_product(self, id):
        try:
            p = self.session.query(Product).filter(Product.id == id).first()
            return p
        except MultipleResultsFound as e:
            print(e)
        except NoResultFound as e:
            print(e)
        return None
