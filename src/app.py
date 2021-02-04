from flask import Flask, jsonify, request
from truckdata import TruckData

app = Flask(__name__)


@app.route('/trucks/<latitude>/<longitude>', methods = ['GET'])
def food_trucks(latitude, longitude):
    truck_data = TruckData(float(latitude), float(longitude)).data
    filtered_data = filter_dataset(request, truck_data)

    return filtered_data.to_json(orient="records")


def filter_dataset(request, dataFrame):
    radius = float(request.args.get('radius', 2.0))
    status = request.args.get('status', 'all')
    limit  = int(request.args.get('limit', 20))

    dataFrame = dataFrame.sort_values(TruckData.DISTANCE)
    if status != 'all' and status in TruckData.STATUS_ENUM:
        dataFrame = dataFrame[dataFrame[TruckData.STATUS] == status]

    dataFrame = dataFrame[dataFrame[TruckData.DISTANCE] < radius]

    return dataFrame[:limit]


if __name__ == '__main__':
    app.run(host='0.0.0.0')