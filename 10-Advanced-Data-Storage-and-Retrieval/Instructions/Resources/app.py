import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

##Database setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#FLASK SETUP
app = Flask(__name__)

#Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query all dates/precipition
  precipitation = []
  results = session.query(Measurement.date, Measurement.prcp).\
  filter(Measurement.date >= "2016-08-23").all()

  for row in results:
      precipitation.append({row[0]:row[1]})
  return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all measurement.station names"""
    # Query all station
    results = session.query(Measurement.station).group_by(Measurement.station).all()

    # Convert list of tuples into normal list
    #station_names = list(np.ravel(results))

    return jsonify(results)

@app.route("/api/v1.0/tobs")   
def tobs():
    # Query all dates/tobs
  tobs = []
  results = session.query(Measurement.date, Measurement.tobs).\
  filter(Measurement.date >= "2016-08-23").all()

  for row in results:
      tobs.append({row[0]:row[1]})
  return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start(start):

    blankdate = start.replace(" ")

    sel = [Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    MeasurementDate_query = session.query(*sel).\
    filter(Measurement.date >= "2010-01-01").all()

    for date in MeasurementDate_query:
        search_date =  date["start"].replace(" ")

        if search_date == blankdate:
            return jsonify(date)
    return jsonify({"error"})
    
@app.route("/api/v1.0/<start>/<end><br/>")

if __name__ == '__main__':
    app.run(debug=True)