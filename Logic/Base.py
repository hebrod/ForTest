from flask import jsonify
from Config import db
from Models.Base import RegionDim, DataSourceDim, LocationDim, TimeDim, Facts
from datetime import datetime
from sqlalchemy.sql import func

def getFactId(idValues):
    factData = Facts.query.filter_by(region=idValues["region"],datasource=idValues["datasource"],origin=idValues["origin_coord"],destination=idValues["destination_coord"],time=idValues["datetime"])
    if factData.count() == 0:
        fact_entity = Facts()
        fact_entity.region = idValues["region"]
        fact_entity.datasource = idValues["datasource"]
        fact_entity.origin = idValues["origin_coord"]
        fact_entity.destination = idValues["destination_coord"]
        fact_entity.time = idValues["datetime"]
        fact_entity.events = 1
        db.session.add(fact_entity)
        db.session.commit()
    else:
        factData[0].events += 1
        db.session.commit()
    factData = Facts.query.filter_by(region=idValues["region"], datasource=idValues["datasource"],
                                     origin=idValues["origin_coord"], destination=idValues["destination_coord"],
                                     time=idValues["datetime"]).first()
    return factData.id

def getLocationId(value):
    locationIData = LocationDim.query.filter_by(location=func.ST_GeomFromText(value, 4326)).with_entities(LocationDim.id)
    if locationIData.count() == 0:
        location_entity = LocationDim()
        location_entity.location = func.ST_GeomFromText(value, 4326)
        db.session.add(location_entity)
        db.session.commit()
    locationIData = LocationDim.query.filter_by(location=func.ST_GeomFromText(value, 4326)).with_entities(LocationDim.id)[0]
    return locationIData.id

def getDateTimeId(value):
    dateTimeValue = datetime.fromisoformat(value)
    year = dateTimeValue.year
    month = dateTimeValue.month
    day = dateTimeValue.day
    hour = dateTimeValue.hour
    dateTimeData = TimeDim.query.filter_by(year=year,month=month, day=day, hour=hour)
    if dateTimeData.count() == 0:
        time_entity = TimeDim()
        time_entity.year = year
        time_entity.month = month
        time_entity.day = day
        time_entity.hour = hour
        db.session.add(time_entity)
        db.session.commit()
    dateTimeData = TimeDim.query.filter_by(year=year,month=month, day=day, hour=hour)[0]
    return dateTimeData.id

def getDataSourceId(value):
    datasourceData = DataSourceDim.query.filter_by(datasource=value)
    if datasourceData.count() == 0:
        datasource_entity = DataSourceDim()
        datasource_entity.datasource = value
        db.session.add(datasource_entity)
        db.session.commit()
    datasourceData = DataSourceDim.query.filter_by(datasource=value)[0]
    return datasourceData.id

def getRegionId(value):
    regionData = RegionDim.query.filter_by(region=value)
    if regionData.count() == 0:
        region_entity = RegionDim()
        region_entity.region = value
        db.session.add(region_entity)
        db.session.commit()
    regionData = RegionDim.query.filter_by(region=value)[0]
    return regionData.id

def handleData(record):
    columns = ["region","datasource","datetime","origin_coord","destination_coord"]
    idValues = {"region": None, "datasource": None,"datetime": None,"origin_coord": None, "destination_coord":None}
    finalId = None
    for column in columns:
        if column in record:
            value = record[column]
            if value is not None:
                if column == "region":
                    idValues[column] = getRegionId(value)
                if column == "datasource":
                    idValues[column] = getDataSourceId(value)
                if column == "datetime":
                    idValues[column] = getDateTimeId(value)
                if column == "origin_coord":
                    idValues[column] = getLocationId(value)
                if column == "destination_coord":
                    idValues[column] = getLocationId(value)
    if None not in idValues.values():
        finalId = getFactId(idValues)
    return finalId

def loadEvent(data):
    result = ""
    for record in data:
        result = handleData(record)
    return jsonify({'finished': result})