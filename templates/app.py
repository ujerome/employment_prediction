from flask import Flask, render_template, request, Response, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import numpy as np
import mysql.connector
from datetime import datetime
import csv
import io

app = Flask(__name__)
app.secret_key = '@Boateng@123'

# MySQL connection
db = mysql.connector.connect(
    host="sql202.infinityfree.com",         # replace with your actual SQL host
    user="if0_39101979",            # replace with your InfinityFree username
    password="uwanyagasani123",        # your InfinityFree MySQL password
    database="if0_39101979_employment_prediction"  # your InfinityFree DB name
cursor = db.cursor()

# Login manager setup
login_manager = LoginManager(app)

# In-memory user store (for demo)
users = {}

class User(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Google OAuth setup
google_bp = make_google_blueprint(
    client_id="ujerome250@gmail.com",
    client_secret="@Boateng@123",
    redirect_url="/login/google/authorized",
    scope=["profile", "email"]
)
app.register_blueprint(google_bp, url_prefix="/login")

# Load model and encoders
model = joblib.load("saved_model/logistic_model.joblib")
label_encoders = joblib.load("saved_model/label_encoders.joblib")
FEATURES = ["Sex", "Age", "Marital_status", "Unpaid_work", "Educational_level", "TVET", "Field_of_education"]

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if not session.get("loggedin"):
        return redirect(url_for("login"))

    feature_options = {
        feature: list(label_encoders[feature].classes_) if feature in label_encoders else None
        for feature in FEATURES
    }
    return render_template("index.html", features=FEATURES, feature_options=feature_options)

@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("loggedin"):
        return redirect(url_for("login"))

    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        if cursor.fetchone():
            msg = "⚠️ Username or email already exists."
        else:
            hashed_pw = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_pw))
            db.commit()
            return redirect(url_for("login", registered="true"))

    return render_template("register.html", msg=msg)

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("loggedin"):
        return redirect(url_for("home"))

    msg = ""
    if request.args.get("registered") == "true":
        msg = "✅ Registration successful. Please log in."

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            session["loggedin"] = True
            session["username"] = username
            return redirect(url_for("home"))
        else:
            msg = "❌ Invalid username or password."

    return render_template("login.html", msg=msg)

@app.route("/login/google/authorized")
def google_authorized():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "❌ Failed to get user info from Google", 400

    user_info = resp.json()
    user_id = user_info["id"]

    user = User(id_=user_id, name=user_info["name"], email=user_info["email"])
    users[user_id] = user
    login_user(user)

    session["loggedin"] = True
    session["username"] = user_info["email"]
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("login"))

@app.route("/predict", methods=["POST"])
def predict():
    if not session.get("loggedin"):
        return redirect(url_for("login"))

    raw_input = {}
    input_data = []

    try:
        for feature in FEATURES:
            value = request.form.get(feature)
            raw_input[feature] = value

            if feature in label_encoders:
                if value not in label_encoders[feature].classes_:
                    return f"❌ Invalid value for {feature}: {value}"
                value = label_encoders[feature].transform([value])[0]
            else:
                value = float(value)
                if feature == "Age" and not (16 <= value <= 35):
                    return "❌ Age must be between 16 and 35"

            input_data.append(value)

        input_array = np.array([input_data])
        prediction = model.predict(input_array)[0]
        prediction_label = label_encoders["LFP"].inverse_transform([prediction])[0]
        confidence = round(float(np.max(model.predict_proba(input_array)) * 100), 2)

        cursor.execute("""
            INSERT INTO employment_output (
                Sex, Age, Marital_status, Unpaid_work, Educational_level, TVET, Field_of_education,
                prediction, confidence, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            raw_input["Sex"], float(raw_input["Age"]), raw_input["Marital_status"],
            raw_input["Unpaid_work"], raw_input["Educational_level"], raw_input["TVET"],
            raw_input["Field_of_education"], prediction_label, confidence, datetime.now()
        ))
        db.commit()

        return render_template("result.html", prediction=prediction_label, confidence=confidence, input_summary=raw_input)

    except Exception as e:
        return f"❌ Error during prediction: {str(e)}"

@app.route("/recent")
def recent_predictions():
    if not session.get("loggedin"):
        return redirect(url_for("login"))

    try:
        cursor.execute("""
            SELECT id, Sex, Age, Marital_status, Unpaid_work, Educational_level, TVET,
                   Field_of_education, prediction, confidence, timestamp
            FROM employment_output
            ORDER BY timestamp DESC
        """)
        rows = cursor.fetchall()
        columns = ["id", "Sex", "Age", "Marital_status", "Unpaid_work", "Educational_level",
                   "TVET", "Field_of_education", "prediction", "confidence", "timestamp"]
        recent_data = [dict(zip(columns, row)) for row in rows]
        return render_template("recent.html", records=recent_data)

    except Exception as e:
        return f"❌ Error fetching recent predictions: {str(e)}"

@app.route("/export")
def export_csv():
    if not session.get("loggedin"):
        return redirect(url_for("login"))

    try:
        cursor.execute("""
            SELECT Sex, Age, Marital_status, Unpaid_work, Educational_level, TVET,
                   Field_of_education, prediction, confidence, timestamp
            FROM employment_output
            ORDER BY timestamp DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()
        columns = ["Sex", "Age", "Marital_status", "Unpaid_work", "Educational_level",
                   "TVET", "Field_of_education", "prediction", "confidence", "timestamp"]

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(columns)
        writer.writerows(rows)

        response = Response(output.getvalue(), mimetype='text/csv')
        response.headers["Content-Disposition"] = "attachment; filename=recent_predictions.csv"
        return response

    except Exception as e:
        return f"❌ Error exporting CSV: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
