import datetime

from lib.Singleton import Singleton
from model.Base import Base
from model.Product import Product
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        asc, create_engine, desc, select)
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

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
        site="wfwf",
        title="",
        author="",
        path="",
        tags="",
        visible=True,
        download_count=0,
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
            at=datetime.datetime.now()
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
                    "at": datetime.datetime.now()
                }
            )
            return self.session.commit()
        except Exception as e:
            print(e)
        return None

    def get_visible_products(self):
        try:
            return self.session.query(Product).filter(Product.visible == True).order_by(Product.at).all()
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
    