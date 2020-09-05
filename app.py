# import Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect

from flask import Flask, jsonify

# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)
base.classes.keys()

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

inspector = inspect(engine)
inspector.get_table_names()

# data_setup = datetime(measurement.date)
# Flask Setup
#################################################
app = Flask(__name__)


# Query for the dates and temperature observations from the last year.

@app.route("/")
def home():
    return("/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/2017-01-01<br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    results1 = session.query(measurement.date, measurement.prcp).filter(measurement.date>="2016-08-23").all()
    first_dict = list(np.ravel(results1))
#  Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
    # first_dict = []
    # for temps in results1:
    #     temps_dict = {}
    #     temps_dict["date"] = Measurement.date
    #     temps_dict["tobs"] = Measurement.tobs
    #     first_dict.append(temps_dict)

#  Return the JSON representation of your dictionary.
    return jsonify(first_dict)

# * `/api/v1.0/stations`
#   * Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    results2 = session.query(station.station, station.name).all()

    sec_dict = list(np.ravel(results2))
# # #  Convert the query results to a Dictionary.
# #     sec_dict = []
# #     for sta in results2:
# #         station_dict = {}
# #         station_dict["station"] = Station.station
# #         station_dict["name"] = Station.name
# #         sec_dict.append(station_dict)

# # #  Return the JSON representation of your dictionary.

    return jsonify(sec_dict)

# # * `/api/v1.0/tobs`
# #   * Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    results3 = session.query(measurement.date, measurement.tobs).\
            filter(measurement.date>="2016-08-23").\
            filter(measurement.date<="2017-08-23").all()

            
    temp_dict = list(np.ravel(results3))
# # #  Convert the query results to a Dic

# #  Convert the query results to a Dictionary.
#     third_dict = []
#     for temps in results3:
#         temp_dict = {}
#         temp_dict["date"] = Measurement.date
#         temp_dict["tobs"] = Measurement.tobs
#         third_dict.append(temp_dict)

# #  Return the JSON representation of your dictionary.

    return jsonify(temp_dict)


# # * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

# #   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# #   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

# #   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


@app.route("/api/v1.0/<date>")

def start1(date):

    results4 = session.query((measurement.date, func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).\
            filter(measurement.date)>=date).all()
   

    
    # temp_dates = list(np.ravel(results4))
    # #  Convert the query results to a Dictionary.
    five_dict = []
    for s in results4:
        
        # start_dict = {}
        # start_dict["Date"] = float(s[0])
        # start_dict["Avg"] = float(s[1])
        # start_dict["Min"] = float(s[2])
        # start_dict["Max"] = float(s[3])
        # five_dict.append(start_dict)

        start_dict = {}
        start_dict["Date"] = s.Date
        start_dict["Avg"] = s.func.avg(measurement.tobs)
        start_dict["Min"] = s.func.min(measurement.tobs)
        start_dict["Max"] = s.func.max(measurement.tobs)
        five_dict.append(start_dict)
# #  Return the JSON representation of your dictionary.

    return jsonify(five_dict)
    # return jsonify(temp_dates)

    
if __name__ == '__main__':
    app.run(debug=True)