from flask import Flask, jsonify, render_template, request
from geopy.distance import great_circle
import pandas

app = Flask(__name__)


APPLICANT  = 'Applicant'
ADDRESS    = 'Address'
STATUS     = 'Status'
FOOD_ITEMS = 'FoodItems'
LATITUDE   = 'Latitude'
LONGITUDE  = 'Longitude'

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/trucks/<latitude>/<longitude>', methods = ['GET'])
def food_trucks(latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)
    truck_data = retreive_dataset()
    truck_data = addDistanceFromLocation(truck_data, latitude, longitude)
    truck_data = filter_dataset(request, truck_data)

    return truck_data.to_json(orient="records")


def filter_dataset(request, dataFrame):
    radius = request.args.get('radius')
    status = request.args.get('status')

    dataFrame = dataFrame.sort_values('DistanceFromLocation')
    dataFrame = dataFrame[dataFrame[STATUS] == 'ISSUED']

    return dataFrame

def retreive_dataset():
    rawDataFrame = pandas.read_csv('https://data.sfgov.org/api/views/rqzj-sfat/rows.csv')
    cleanedDataFrame = rawDataFrame.reindex(
        [
            APPLICANT, ADDRESS, STATUS, FOOD_ITEMS, LATITUDE, LONGITUDE
        ],
        axis=1
    )
    # TODO: Caching
    return cleanedDataFrame

def addDistanceFromLocation(dataFrame, latitude, longitude):
    dataFrame['DistanceFromLocation'] = dataFrame.apply(
        calculateDistance, axis=1, args=(latitude, longitude)
    )

    return dataFrame

def calculateDistance(df_row, latitude, longitude):
    return great_circle(
        (latitude, longitude),
        (df_row[LATITUDE], df_row[LONGITUDE])
    ).miles



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')