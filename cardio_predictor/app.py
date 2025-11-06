from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load model and scaler
model = joblib.load('cardio_model.pkl')
scaler = joblib.load('scaler.pkl')

model_attack= joblib.load('heart_attack_model.pkl')
scalerr= joblib.load('scalerrr.pkl')
# Features used for prediction (excluding patientid and target)
FIELDS = [
    'age', 'gender', 'chest pain', 'resting BP', 'serum cholestrol',
    'fasting blood sugar', 'resting relectro', 'max heart rate',
    'exercise angia', 'old peak', 'slope', 'no of major vessels'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cardio', methods=['GET', 'POST'])
def cardio():
    result = None
    if request.method == 'POST':
        try:
            input_data = [float(request.form[f]) for f in FIELDS]
            input_scaled = scaler.transform([input_data])
            prediction = model.predict(input_scaled)[0]
            result = " The patient has cardiovascular disease." if prediction == 1 else " The patient does not have cardiovascular disease."
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template('cardio.html', result=result, fields=FIELDS)

@app.route('/attack', methods=['GET', 'POST'])
def attack():
    prediction = ""
    if request.method == "POST":
        try:
            # Collect and process input from the form
            input_data = [
                float(request.form["Age"]),
                float(request.form["Gender"]),
                float(request.form["HeartRate"]),
                float(request.form["SystolicBP"]),
                float(request.form["DiastolicBP"]),
                float(request.form["BloodSugar"]),
                float(request.form["CKMB"]),
                float(request.form["Troponin"])
            ]
            scaled_data = scalerr.transform([input_data])
            result = model_attack.predict(scaled_data)[0]
            prediction = " Heart Attack Risk: Positive" if result == 1 else " Heart Attack Risk: Negative"
        except:
            prediction = "⚠️ Please enter valid numeric values for all fields."
    return render_template("heart_attack.html", prediction=prediction)




if __name__ == '__main__':
    app.run(debug=True)
