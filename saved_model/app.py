from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load model, encoders, and features
model = joblib.load("saved_model/logistic_model.joblib")
label_encoders = joblib.load("saved_model/label_encoders.joblib")
FEATURES = joblib.load("saved_model/features.joblib")

@app.route("/")
def index():
    feature_options = {}
    for feature in FEATURES:
        if feature in label_encoders:
            options = [opt for opt in label_encoders[feature].classes_ if str(opt).lower() != 'nan']
            feature_options[feature] = options
        else:
            feature_options[feature] = None  # Numeric field
    return render_template("index.html", features=FEATURES, feature_options=feature_options)

@app.route("/predict", methods=["POST"])
def predict():
    input_data = []
    try:
        for feature in FEATURES:
            value = request.form.get(feature)

            if feature in label_encoders:
                options = list(label_encoders[feature].classes_)
                if value not in options:
                    return f"❌ Invalid value for {feature}: {value}"
                value = label_encoders[feature].transform([value])[0]
            else:
                value = float(value)
            input_data.append(value)

        input_array = np.array([input_data])
        prediction = model.predict(input_array)[0]
        prediction_label = label_encoders['LFP'].inverse_transform([prediction])[0]

        return render_template(
            "result.html",
            prediction=prediction_label,
            confidence=round(float(np.max(model.predict_proba(input_array)) * 100), 2),
            input_summary=dict(zip(FEATURES, request.form.values()))
        )

    except Exception as e:
        return f"❌ Error during prediction: {e}"

if __name__ == "__main__":
    app.run(debug=True)
