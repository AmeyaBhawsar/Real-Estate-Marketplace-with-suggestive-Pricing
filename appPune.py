from flask import Flask, request, url_for, render_template
import pickle
import numpy as np
import json

app = Flask(__name__,template_folder='template')

app.config.update(
    dict(SECRET_KEY="powerful secretkey", WTF_CSRF_SECRET_KEY="a csrf secret key")
)

__locations = None
__data_columns = None
model = pickle.load(open("pune_home_prices_model.pickle","rb"))

def get_estimated_price(input_json):
    try:
        loc_index = __data_columns.index(input_json['location'].lower())
    except:
        loc_index = -1
    x = np.zeros(98)
    x[0] = input_json['sqft']
    x[1] = input_json['bath']
    x[2] = input_json['bhk']
    if loc_index >= 0:
        x[loc_index] = 1
    result = round(model.predict([x])[0],2)
    return result

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("Loading the saved artifacts...start !")
    global __data_columns
    global __locations
    global model

    with open("columns.json") as f:
        __data_columns = json.loads(f.read())["data_columns"]
        __locations = __data_columns[3:]

@app.route("/")
def indpune():
    return render_template('indpune.html')


@app.route("/predictpune", methods=["POST"])
def predictpune():
    
    if request.method == 'POST':
        input_json = {
            "location": request.form['sLocation'],
            "sqft": request.form['Squareft'],
            "bhk": request.form['uiBHK'],
            "bath": request.form['uiBathrooms']
        }
        result = get_estimated_price(input_json)

        if result > 100:
            result = round(result/100, 2)
            result = str(result) + ' Crore'
        else:
            result = str(result) + ' Lakhs'

    return render_template('predictpune.html', result=result)

if __name__ == "__main__":
    print("Starting Python Flask Server")
    load_saved_artifacts()
    app.run(debug=True)