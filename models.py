import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from flask_cors import CORS

db = SQLAlchemy()


def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    CORS(app)
    Migrate(app, db)
    return db


class Customer(db.Model):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    email = Column(String)
    customer_orders = db.relationship('Order', backref='customer', lazy=True)

    def __init__(self, name, city, email):
        self.name = name
        self.city = city
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'email': self.email
        }


class Merchant(db.Model):
    __tablename__ = 'merchant'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    email = Column(String)
    merchant_orders = db.relationship('Order', backref='merchant', lazy=True)

    def __init__(self, name, city, email):
        self.name = name
        self.city = city
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'email': self.email
        }


class Order(db.Model):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    customer_id = db.Column(Integer, db.ForeignKey('customer.id'), nullable=False)
    merchant_id = db.Column(Integer, db.ForeignKey('merchant.id'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'merchant_id': self.merchant_id
        }
