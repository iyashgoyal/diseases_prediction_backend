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
def home():
    return render_template('home.html', symptoms=symptoms)

@app.route('/disease_predict', methods=['POST'])
def disease_predict():
    selected_symptoms = []
    for key in ['Symptom1', 'Symptom2', 'Symptom3', 'Symptom4', 'Symptom5']:
        if request.form.get(key) and request.form.get(key).strip():
            selected_symptoms.append(request.form.get(key))
    
    # Make sure we have at least one symptom
    if not selected_symptoms:
        return render_template('home.html', symptoms=symptoms, error="Please enter at least one symptom")
    
    try:
        disease = diseaseprediction.dosomething(selected_symptoms)
        return render_template('disease_predict.html', disease=disease, symptoms=symptoms)
    except Exception as e:
        print(f"Error predicting disease: {e}")
        return render_template('home.html', symptoms=symptoms, error=f"Error processing symptoms: {e}")

@app.route('/find_doctor', methods=['POST', 'GET'])
def get_location():
    if request.method == 'POST':
        location = request.form.get('doctor', '')
        if not location:
            return render_template('home.html', symptoms=symptoms, error="Please enter a location")
    else:
        # Default location if coming from a GET request (e.g., link on disease prediction page)
        location = "Your City"
    
    return render_template('find_doctor.html', location=location, symptoms=symptoms)

@app.route('/drug', methods=['POST'])
def drugs():
    medicine = request.form['medicine']
    return render_template('home.html', medicine=medicine, symptoms=symptoms)

if __name__ == '__main__':
    # Enable debug mode for development
    app.run(debug=True, host='0.0.0.0', port=10000)  # Use a Render-compatible port
