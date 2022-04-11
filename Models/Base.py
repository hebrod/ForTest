from sqlalchemy_serializer import SerializerMixin
from geoalchemy2 import Geometry
from Config import db

class RegionDim(db.Model, SerializerMixin):
  __tablename__ = 'region_dim'
  id = db.Column(db.Integer(), primary_key=True)
  region = db.Column(db.String(50))

class DataSourceDim(db.Model, SerializerMixin):
  __tablename__ = 'datasource_dim'
  id = db.Column(db.Integer(), primary_key=True)
  datasource = db.Column(db.String(50))

class LocationDim(db.Model, SerializerMixin):
  __tablename__ = 'location_dim'
  id = db.Column(db.Integer(), primary_key=True)
  location = db.Column(Geometry(srid=4326, management=True))

class TimeDim(db.Model, SerializerMixin):
  __tablename__ = 'time_dim'
  id = db.Column(db.Integer(), primary_key=True)
  year = db.Column(db.Integer())
  month = db.Column(db.Integer())
  day = db.Column(db.Integer())
  hour = db.Column(db.Integer())

class Facts(db.Model, SerializerMixin):
  __tablename__ = 'facts'
  id = db.Column(db.Integer(), primary_key=True)
  region = db.Column(db.Integer())
  datasource = db.Column(db.Integer())
  origin = db.Column(db.Integer())
  destination = db.Column(db.Integer())
  time = db.Column(db.Integer())
  events = db.Column(db.Integer())