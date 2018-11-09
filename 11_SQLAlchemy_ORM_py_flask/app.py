import sqlalchemy
import numpy as np
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_end_date"
         )


@app.route("/api/v1.0/precipitation")

def precipitation():
    """Return a list of date and temperature for last 12 months"""
    # Query date and temperature
    last_observ = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Convert object to string and split it
    string = str(last_observ[0]).split('-')

    year_ago = dt.date(int(string[0]), int(string[1]), int(string[2])) - dt.timedelta(days=365)
    print(year_ago)

    # Perform a query to retrieve the data and precipitation scores
    tobs_data=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > year_ago).all()

    # Convert the query results to a Dictionary
    tobs_data_dict = dict(tobs_data)

    return jsonify(tobs_data_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature for previous year"""
    results=session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').all()
    tobs_list=[]
    for a in results:
        tobs_dict={}
        tobs_dict['date']=a.date
        tobs_dict['tobs']=a.tobs
        tobs_list.append(tobs_dict)
        
    return jsonify(tobs_list)

@app.route("/api/v1.0/start_date/<start_date>")
def start_date(start_date):
    """Returns the Tmin, Tavg and Tmax for all dates greater than and equal to the start date"""
    # Perform a query to retrieve the Tmin, Tavg and Tmax for all dates greater than and equal to the start date
    dates=session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ).filter(Measurement.date==start_date).all()
    
    if None in dates[0]:
        return jsonify({"error": f"Date: {start_date} not found."})
    return jsonify(dates)
    
@app.route("/api/v1.0/start_end_date/<start_date>/<end_date>")
def start_end_date(start_date,end_date):
    """Returns the Tmin, Tavg and Tmax for all dates between start and end dates"""
    # Perform a query to retrieve the Tmin, Tavg and Tmax for all dates between start and end dates
    dates=session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ).filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).all()
    
    if None in dates[0]:
        return jsonify({"error": f"Dates not found."})
    return jsonify(dates)


if __name__ == '__main__':
    app.run(debug=True)