from flask import Flask, render_template, request
import joblib
import pandas as pd
import os

# Set template_folder to current directory
app = Flask(__name__, template_folder='.')

# Load model and scaler
model = joblib.load("xgboost_concrete_model.pkl")
scaler = joblib.load("scaler.pkl")

# Feature order
features = ['Cement', 'Blast Furnace Slag', 'Fly Ash', 'Water',
            'Superplasticizer', 'Coarse Aggregate', 'Fine Aggregate', 'Age']

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', features=features, prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = [float(request.form[f]) for f in features]
        df = pd.DataFrame([dict(zip(features, input_data))])
        scaled = scaler.transform(df)
        prediction = model.predict(scaled)[0]
        return render_template('index.html', features=features,
                               prediction=f"{prediction:.2f}")
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
