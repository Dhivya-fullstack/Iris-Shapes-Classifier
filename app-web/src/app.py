from flask import Flask
from flask import render_template
from flask import request
import requests
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

UPLOAD_FOLDER = '../static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/irisClassifier', methods=['GET', 'POST'])
def irisClassifier():

    if request.method == 'GET':

        return render_template('irisClassifier.html')

    elif request.method == 'POST':

        # Get the input data from the form
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])

        # Call the API to get the prediction with a PUT request
        url = 'http://localhost:8002/api/models/irisClassifier'
        data = {
            'sepal_length': sepal_length,
            'sepal_width': sepal_width,
            'petal_length': petal_length,
            'petal_width': petal_width
        }
        response = requests.put(url, json=data)
        
        if response.status_code == 200:
            prediction = response.json()['prediction']
        else:
            prediction = 'Error: ' + response.content.decode('utf-8')

        return render_template('irisClassifier_prediction.html', 
                                sepal_length=sepal_length,
                                sepal_width=sepal_width,
                                petal_length=petal_length,
                                petal_width=petal_width,
                                prediction=prediction)



@app.route('/shapesClassifier', methods=['GET', 'POST'])
def shapesClassifier():

    if request.method == 'GET':

        return render_template('shapesClassifier.html')

    elif request.method == 'POST':

        # Get the input data from the form
        file = request.files['image']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        # Call the API to get the prediction with a PUT request
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        url = 'http://localhost:8002/api/models/shapesClassifier'
        files = {'image': open(image_path, 'rb')}
        response = requests.put(url, files=files)
        # Close the file after sending the request
        files['image'].close()
        
        if response.status_code == 200:
            prediction = response.json()['prediction']
        else:
            prediction = 'Error: ' + response.content.decode('utf-8')

        return render_template('shapesClassifier_prediction.html', 
                                file_name=file.filename,
                                prediction=prediction)
  







if __name__ == "__main__":
    print("Starting Flask...")   # add this for debug
    app.run(debug=True, port=5000)
