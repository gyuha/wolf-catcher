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
        self.engine = create_engine(config.setting["db"], echo=False, future=True)
        self.session = Session(bind=self.engine)

        Base.metadata.create_all(self.engine)

    def insert_product(
        self,
        id,
        title="",
        author="",
        path="",
        tags="",
        visible=True,
        download_count=0,
        site="wfwf"
    ):
        if self.get_product(id) is not None:
            self.set_visible_product(id, True)
            return

        product = Product(
            id=id,
            site=site,
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
        except Exception as e:
            print(e)
        return None

    def updated_product(
        self, id, title, author, path, tags
    ):
        try:
            self.session.query(Product).filter_by(id=id).update(
                {
                    "title": title,
                    "author": author,
                    "path": path,
                    "tags": tags,
                }
            )
            return self.session.commit()
        except Exception as e:
            print(e)
        return None

    def get_visible_products(self):
        try:
            return self.session.query(Product).filter(Product.visible == True).all()
        except Exception as e:
            print(e)
        return None

    def set_visible_product(self, id: str, visible: bool):
        try:
            self.session.query(Product).filter(Product.id == id).update({"visible": visible})
            return self.session.commit()
        except NoResultFound as e:
            print(e)
        return None
