def analyze_cbc(values, prediction):

    abnormal = []
    recommendations = []

    hb = values["hemoglobin"]
    rbc = values["rbc"]
    hct = values["hematocrit"]
    wbc = values["wbc"]
    platelets = values["platelets"]
    mcv = values["mcv"]
    mch = values["mch"]
    mchc = values["mchc"]
    rdw = values["rdw"]

    # These are example screening thresholds.
    # They should be adjusted to your dataset/lab reference ranges.

    if hb < 12:
        abnormal.append("Hemoglobin")

    if rbc < 4:
        abnormal.append("RBC")

    if hct < 36:
        abnormal.append("Hematocrit")

    if wbc < 4:
        abnormal.append("WBC")

    if wbc > 11:
        abnormal.append("WBC")

    if platelets < 150:
        abnormal.append("Platelets")

    if platelets > 450:
        abnormal.append("Platelets")

    if mcv < 80:
        abnormal.append("MCV")

    if mcv > 100:
        abnormal.append("MCV")

    if mch < 27:
        abnormal.append("MCH")

    if mchc < 32:
        abnormal.append("MCHC")

    if rdw > 15:
        abnormal.append("RDW")

    abnormal = list(dict.fromkeys(abnormal))

    if prediction == "Anemia Detected":

        if mcv < 80 and mch < 27:
            recommendations.append(
                "The screening result shows an anemia signal with "
                "low red-cell indices. Discuss the result with a "
                "qualified healthcare professional."
            )
        else:
            recommendations.append(
                "The screening model detected an anemia signal. "
                "Professional medical evaluation is recommended."
            )

    if abnormal:
        recommendations.append(
            "Some entered CBC parameters are outside the "
            "configured reference range."
        )

    if not abnormal and prediction == "No Anemia Detected":
        recommendations.append(
            "No concerning CBC pattern was detected by the "
            "configured screening checks."
        )

    # Risk classification for UI purposes.
    # This is NOT a clinical diagnosis/severity score.
    if prediction == "Anemia Detected" and len(abnormal) >= 3:
        risk = "High"
    elif prediction == "Anemia Detected" or len(abnormal) >= 2:
        risk = "Moderate"
    else:
        risk = "Low"

    if risk == "High":
        doctor_message = (
            "Prompt medical review is recommended based on the "
            "screening result and abnormal parameters."
        )
    elif risk == "Moderate":
        doctor_message = (
            "Consider discussing the report with a healthcare "
            "professional, particularly if abnormalities persist "
            "or symptoms are present."
        )
    else:
        doctor_message = (
            "No immediate medical-review alert was triggered by "
            "this screening result."
        )

    return {
        "abnormal_parameters": abnormal,
        "recommendations": recommendations,
        "risk_level": risk,
        "doctor_message": doctor_message
    }