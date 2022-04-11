from flask import jsonify
from Config import db
from Models.Base import RegionDim, DataSourceDim, LocationDim, TimeDim, Facts
from datetime import datetime
from sqlalchemy.sql import func, text
from pandas import DataFrame
import json

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
    day_of_week = dateTimeValue.strftime("%A")
    week_of_year = dateTimeValue.strftime("%V")
    dateTimeData = TimeDim.query.filter_by(year=year,month=month, day=day, hour=hour)
    if dateTimeData.count() == 0:
        time_entity = TimeDim()
        time_entity.year = year
        time_entity.month = month
        time_entity.day = day
        time_entity.hour = hour
        time_entity.day_of_week = day_of_week
        time_entity.week_of_year = int(week_of_year)
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

def loadEvents(data):
    result = ""
    for record in data:
        result = handleData(record)
    return jsonify({'finished': result})

def getDataEventsByRegion(data):
    if "region" in data:
        value = data["region"]
        statement = " select t.year, t.week_of_year, avg(f.events) avg_events from facts f "
        statement += " inner join time_dim t on t.id = f.time "
        statement += " inner join region_dim r on r.id = f.region "
        statement += " where r.region = :value "
        statement += " group by t.year, t.week_of_year "
        stmt = text(statement)
        result = db.session.execute(stmt, {"value": value})
        df = DataFrame(result.fetchall())
        if df.empty:
            return jsonify({'Result': 'No Data found.'})
        else:
            df.columns = result.keys()
            return json.dumps(json.loads(df.to_json(orient="records")))
    if "rectangle" in data:
        min_long = data["rectangle"]["min_longitude"]
        min_lat = data["rectangle"]["min_latitude"]
        max_long = data["rectangle"]["max_longitude"]
        max_lat = data["rectangle"]["max_latitude"]
        statement = " select t.year, t.week_of_year, avg(f.events) avg_events from facts f "
        statement += " inner join time_dim t on t.id = f.time "
        statement += " inner join location_dim lo on lo.id = f.origin "
        statement += " inner join location_dim ld on ld.id = f.destination "
        statement += " where ST_Intersects ( lo.location "
        statement += " , ST_MakeEnvelope ( :min_long, :min_lat, :max_long, :max_lat, 4326)::geography(:type) ) "
        statement += " or ST_Intersects ( ld.location "
        statement += " , ST_MakeEnvelope ( :min_long, :min_lat, :max_long, :max_lat, 4326)::geography(:type) ) "
        statement += " group by t.year, t.week_of_year "
        stmt = text(statement)
        result = db.session.execute(stmt, {"min_long": min_long, "min_lat": min_lat, "max_long": max_long, "max_lat":max_lat, "type":"POLYGON"})
        df = DataFrame(result.fetchall())
        if df.empty:
            return jsonify({'Result': 'No Data found.'})
        else:
            df.columns = result.keys()
            return json.dumps(json.loads(df.to_json(orient="records")))
    return jsonify({'Result': 'No valid option.'})