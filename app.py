from flask import Flask, request, render_template
import csv
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/flights', methods=['GET', 'POST'])
def flightTable():
    if request.method == 'POST':
        f = request.form['csvFile']

        #try to open the csv file for reading
        try:
            file = open(f)
            csvflight = csv.reader(file)
        except IOError:
            return "File not accessible or not csv"

        #remove the header and get all the row to data
        header = next(csvflight)
        data = []
        for r in csvflight:
            data.append(r)

        #get the arrival by order
        arrivalsTime = []
        for row in data:
            arrivalsTime.append(row[1])
        sorted(arrivalsTime)

        TheFirsts = 20
        TheFirstsSuc = 0

        for row in data:
            flightNum = row[0]
            correctRow = False
            if flightNum != '':
                try:
                    arrivalTime = datetime.strptime(row[1].strip(), "%H:%M")
                    DeparturesTime = datetime.strptime(row[2].strip(), "%H:%M")
                    correctRow = True
                except:
                    row[3] = 'failed'
            else:
                row[3] = 'failed'

            if correctRow:
                MinDif = (DeparturesTime - arrivalTime).total_seconds() / 60
                if MinDif > 180 and row[1] in arrivalsTime[:TheFirsts] and TheFirstsSuc < 20:
                    row[3] = 'success'
                    TheFirstsSuc += 1
                else:
                    row[3] = 'failed'
            else:
                if row[1] in arrivalsTime[:TheFirsts]:
                    TheFirsts += 1
        file.close()

        with open(f, 'w') as file:
            writer = csv.writer(file)
            for r in data:
                writer.writerow(r)

        return render_template('flights.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
