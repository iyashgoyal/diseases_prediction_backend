import csv
import os
from flask import Flask, render_template, request
import diseaseprediction

app = Flask(__name__)

# Ensure the correct path for the CSV file
csv_path = os.path.join(os.path.dirname(__file__), 'templates', 'Testing.csv')

# Read CSV file for symptoms
with open(csv_path, newline='') as f:
    reader = csv.reader(f)
    symptoms = next(reader)[:-1]  # Remove last empty element

@app.route('/', methods=['GET'])
def dropdown():
    return render_template('includes/default.html', symptoms=symptoms)

@app.route('/disease_predict', methods=['POST'])
def disease_predict():
    selected_symptoms = [request.form[key] for key in ['Symptom1', 'Symptom2', 'Symptom3', 'Symptom4', 'Symptom5'] if request.form.get(key)]
    
    disease = diseaseprediction.dosomething(selected_symptoms)
    return render_template('disease_predict.html', disease=disease, symptoms=symptoms)

@app.route('/find_doctor', methods=['POST'])
def get_location():
    location = request.form['doctor']
    return render_template('find_doctor.html', location=location, symptoms=symptoms)

@app.route('/drug', methods=['POST'])
def drugs():
    medicine = request.form['medicine']
    return render_template('homepage.html', medicine=medicine, symptoms=symptoms)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Use a Render-compatible port
