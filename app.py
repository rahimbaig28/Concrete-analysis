from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load model and scaler
model = joblib.load("xgboost_concrete_model.pkl")
scaler = joblib.load("scaler.pkl")

features = ['Cement', 'Blast Furnace Slag', 'Fly Ash', 'Water',
            'Superplasticizer', 'Coarse Aggregate', 'Fine Aggregate', 'Age']

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        try:
            # Collect inputs
            data = [float(request.form[feature]) for feature in features]
            df = pd.DataFrame([dict(zip(features, data))])

            # Preprocess & predict
            scaled = scaler.transform(df)
            result = model.predict(scaled)[0]
            prediction = f"{result:.2f} MPa"
        except Exception as e:
            prediction = f"Error: {e}"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
