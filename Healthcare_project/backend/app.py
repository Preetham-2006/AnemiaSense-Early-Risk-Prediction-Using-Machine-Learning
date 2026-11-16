from datetime import timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from prediction import predict_anemia
from database import (
    init_db,
    save_report,
    get_reports,
    get_latest_report,
    get_user,
    update_user,
)
from auth import auth_bp
from recommendations import analyze_cbc
from chatbot import chatbot_response

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "anemiasense-development-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=False)
jwt = JWTManager(app)

@jwt.unauthorized_loader
def missing_token(reason):
    return jsonify({"success": False, "message": "Login required. Please sign in again."}), 401

@jwt.invalid_token_loader
def invalid_token(reason):
    return jsonify({"success": False, "message": "Your login session is invalid. Please sign in again."}), 401

@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return jsonify({"success": False, "message": "Your login session has expired. Please sign in again."}), 401
init_db()
app.register_blueprint(auth_bp, url_prefix="/api/auth")


@app.get("/")
def home():
    return jsonify({"success": True, "status": "running", "message": "AnemiaSense API is running", "model": "LightGBM"})


@app.get("/api/health")
def health():
    return jsonify({"success": True, "message": "Backend is healthy", "model": "LightGBM", "database": "SQLite"})


def _require_json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("Request body must be valid JSON.")
    return data


@app.post("/api/predict")
@app.post("/predict")
@jwt_required()
def predict():
    try:
        data = _require_json()
        required = [
            "ward_number", "hemoglobin", "rbc", "hematocrit", "wbc",
            "platelets", "mcv", "mchc", "mch", "rdw"
        ]
        missing = [k for k in required if data.get(k) in (None, "")]
        if missing:
            return jsonify({"success": False, "message": "Missing required fields.", "missing": missing}), 400

        values = {key: float(data[key]) for key in required}

        model_data = {
            "WardNum": values["ward_number"],
            "ERY": values["rbc"],
            "HK": values["hematocrit"],
            "LEUKO": values["wbc"],
            "HB": values["hemoglobin"],
            "PLT": values["platelets"],
            "MCV": values["mcv"],
            "MCHC": values["mchc"],
            "MCH": values["mch"],
            "RDW": values["rdw"],
        }

        print("\n======================================")
        print("NEW BLOOD REPORT")
        print("======================================")
        print("Input:", values)
        print("Model features:", model_data)

        ml_result = predict_anemia(model_data)
        prediction_value = int(ml_result["prediction"])
        probability = ml_result.get("probability")
        prediction_text = "Anemia Detected" if prediction_value == 1 else "No Anemia Detected"

        analysis = analyze_cbc(values, prediction_text)
        user_id = int(get_jwt_identity())

        report_id = save_report(user_id, {
            **values,
            "prediction": prediction_text,
            "probability": probability,
            "risk_level": analysis["risk_level"],
            "recommendations": analysis["recommendations"],
            "abnormal_parameters": analysis["abnormal_parameters"],
            "doctor_message": analysis["doctor_message"],
        })

        print("REPORT SAVED SUCCESSFULLY. ID:", report_id)

        return jsonify({
            "success": True,
            "report_id": report_id,
            "prediction": prediction_text,
            "prediction_value": prediction_value,
            "diagnosis": prediction_text,
            "probability": probability,
            "risk_level": analysis["risk_level"],
            "abnormal_parameters": analysis["abnormal_parameters"],
            "recommendations": analysis["recommendations"],
            "doctor_message": analysis["doctor_message"],
            "saved": True,
            "message": "Analysis completed and report saved successfully.",
        })

    except (TypeError, ValueError) as exc:
        return jsonify({"success": False, "message": f"Invalid input: {exc}"}), 400
    except Exception as exc:
        app.logger.exception("Prediction error")
        return jsonify({"success": False, "message": f"Prediction failed: {exc}"}), 500


@app.get("/api/reports")
@jwt_required()
def reports():
    try:
        user_id = int(get_jwt_identity())
        return jsonify(get_reports(user_id))
    except Exception as exc:
        app.logger.exception("Reports fetch error")
        return jsonify({"success": False, "message": f"Could not load reports: {exc}"}), 500


@app.get("/api/reports/latest")
@jwt_required()
def latest_report():
    try:
        user_id = int(get_jwt_identity())
        return jsonify(get_latest_report(user_id))
    except Exception as exc:
        app.logger.exception("Latest report error")
        return jsonify({"success": False, "message": f"Could not load latest report: {exc}"}), 500


@app.get("/api/dashboard")
@jwt_required()
def dashboard():
    try:
        user_id = int(get_jwt_identity())
        reports_data = get_reports(user_id)
        latest = reports_data[0] if reports_data else None
        return jsonify({
            "success": True,
            "latest_report": latest,
            "report_count": len(reports_data),
            "reports": reports_data[:8],
        })
    except Exception as exc:
        app.logger.exception("Dashboard error")
        return jsonify({"success": False, "message": f"Could not load dashboard: {exc}"}), 500


@app.get("/api/profile")
@jwt_required()
def profile():
    user = get_user(int(get_jwt_identity()))
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404
    return jsonify({"success": True, "user": user})


@app.put("/api/profile")
@jwt_required()
def edit_profile():
    try:
        data = _require_json()
        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip().lower()
        if not name or not email:
            return jsonify({"success": False, "message": "Name and email are required."}), 400
        user = update_user(int(get_jwt_identity()), name, email)
        if not user:
            return jsonify({"success": False, "message": "That email is already in use."}), 409
        return jsonify({"success": True, "user": user, "message": "Profile updated successfully."})
    except Exception as exc:
        app.logger.exception("Profile update error")
        return jsonify({"success": False, "message": str(exc)}), 500


@app.post("/api/chat")
@jwt_required()
def chat():
    try:
        data = _require_json()
        message = str(data.get("message", "")).strip()
        if not message:
            return jsonify({"response": "Please enter a question about your CBC report."}), 400
        return jsonify({"response": chatbot_response(message)})
    except Exception as exc:
        return jsonify({"response": "Sorry, I could not process your question right now.", "error": str(exc)}), 500


if __name__ == "__main__":
    print("\n======================================")
    print("        ANEMIASENSE BACKEND")
    print("======================================")
    print("API: http://127.0.0.1:5000")
    print("Model: LightGBM")
    print("Database: SQLite")
    app.run(host="127.0.0.1", port=5000, debug=True)
