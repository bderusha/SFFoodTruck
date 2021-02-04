from flask import Flask, jsonify, render_template, request
import pandas

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/trucks/<lat>/<long>', methods = ['GET'])
def food_trucks(lat, long):
    return jsonify([{'my':'test2'}])


def filter_dataset(request, dataset):
    radius = request.args.get('radius')
    status = request.args.get('status')

def retreive_dataset():
    dataFrame = pandas.read_csv('https://data.sfgov.org/api/views/rqzj-sfat/rows.csv')
    return dataFrame

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')