from flask import jsonify, Flask, render_template

from connector import SensorConnector


app = Flask(__name__)
connector = SensorConnector()


@app.route('/')
def main():
    labels = ['PM 2.5 [ug/m^3]', 'PM 2.5 [%]', 'PM 10 [ug/m^3]', 'PM 10 [%]']
    result = connector.get_value()
    pm_25 = result['PM 2.5']
    pm_10 = result['PM 10']
    values = [pm_25, pm_25/.25, pm_10, pm_10/.50]
    return render_template('index.html', labels=labels, values=values)

@app.route('/')
def get_value():
    return jsonify(connector.get_value())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
