from sqlalchemy.orm import declarative_base, backref, relationship, sessionmaker
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, TEXT
import os


Base = declarative_base()
Session = sessionmaker()

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = 'sqlite:///'+os.path.join(BASE_DIR, 'cars_scrape.db')
engine = create_engine(connection_string, echo=True)


def drop_database():
    Base.metadata.drop_all(engine)


def create_database():
    Base.metadata.create_all(engine)


class Link(Base):

    __tablename__ = 'link'
    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False)
    #car = relationship('Car', back_populates='link', uselist=False)            # one to one

    def __repr__(self):
        return self.id


class Car(Base):

    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    brand = Column(String(50))
    model = Column(String(50))
    fuel = Column(String(50))
    price = Column(Integer)
    mileage = Column(Integer)
    emission = Column(Integer)
    #carbon_id = Column(Integer, ForeignKey('carbon.id'))
    #carbon = relationship('CarbonData', back_populates='car', uselist=False)

    #link_id = Column(Integer(), ForeignKey('link.id'))
    #link = relationship('Link', back_populates='car', uselist=False)                # check! many to one

    def __repr__(self):
        return f'{self.brand}-{self.model}-{self.fuel}-{self.id}'


class CarbonData(Base):

    __tablename__ = 'carbon'
    id = Column(Integer(), primary_key=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50))
    emission = Column(Integer())
    #car = relationship('Car', back_populates='carbon', uselist=False)                # one to many

    def __repr__(self):
        return f'{self.brand}'

