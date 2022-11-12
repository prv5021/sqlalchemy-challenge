
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


### Flask Setup
app = Flask(__name__)

### Database Setup

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)



# home route
@app.route("/")
def home():
    return(
        f"<center><h2>Hawaii Climate Analysis (Flask API)</h2></center>"
        f"<center><h3>Available routes:</h3></center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>/api/v1.0/stations</center>"
        f"<center>/api/v1.0/tobs</center>"
        f"<center>/api/v1.0/start/end</center>"
        )


# /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the result as a json
    # Calculate the date one year from the last date in data set.
    yearDate = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    scores = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= yearDate).all()

    

    # Convert List of Tuples Into a Dictionary
    prcp_data = dict(scores)
    # Return JSON Representation of Dictionary
    return jsonify(prcp_data)


# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON names of stations from the Dataset
    station = session.query(Station.station).all()

    

    station_list = list(np.ravel(station))

    
    return jsonify(station_list)


# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    # Dates and Temperature Observations from a Year from the Last Data Point

    yearDate = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp_year = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= yearDate).\
                filter(Measurement.station=='USC00519281').all()

    session.close()

    temp_list = list(np.ravel(temp_year))

    return jsonify(temp_list)


# /api/v1.0/<start>/<end> and /api/v1.0/<start>
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def startEnd(start=None, end=None):

    # select statement
    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    if not end:

        startDate = dt.datetime.strptime(start, "%m%d%Y")

        results = session.query(*selection).filter(Measurement.date >= startDate).all()

        session.close()

        temperatureList = list(np.ravel(results))

        # return the list of temperatures
        return jsonify(temperatureList)


    startDate = startDate = dt.datetime.strptime(start, "%m%d%Y")
    endDate = startDate = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*selection)\
                .filter(Measurement.date >= startDate)\
                .filter(Measurement.date <= endDate).all()

    session.close()

    temperatureList = list(np.ravel(results))

    # return the list of temperatures
    return jsonify(temperatureList)




# app launcher
if __name__=='__main__':
    app.run(debug=True)
