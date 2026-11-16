def analyze_blood_conditions(data):

    hb = float(data.get("HB", 0))
    ery = float(data.get("ERY", 0))
    hk = float(data.get("HK", 0))
    leuko = float(data.get("LEUKO", 0))
    plt = float(data.get("PLT", 0))
    mcv = float(data.get("MCV", 0))
    mchc = float(data.get("MCHC", 0))
    mch = float(data.get("MCH", 0))
    rdw = float(data.get("RDW", 0))

    conditions = []

    # --------------------------------
    # ANEMIA
    # --------------------------------

    anemia = hb < 12

    if anemia:
        conditions.append({
            "name": "Anemia",
            "status": "Detected",
            "type": "screening"
        })

    # --------------------------------
    # POLYCYTHEMIA / ERYTHROCYTOSIS
    # --------------------------------

    polycythemia = (
        ery > 5.9 or
        hk > 50
    )

    if polycythemia:
        conditions.append({
            "name": "Polycythemia / Erythrocytosis",
            "status": "Abnormal pattern detected",
            "type": "screening"
        })

    # --------------------------------
    # LEUKOCYTOSIS
    # --------------------------------

    leukocytosis = leuko > 11

    if leukocytosis:
        conditions.append({
            "name": "Leukocytosis",
            "status": "Detected",
            "type": "CBC abnormality"
        })

    # --------------------------------
    # LEUKOPENIA
    # --------------------------------

    leukopenia = leuko < 4.5

    if leukopenia:
        conditions.append({
            "name": "Leukopenia",
            "status": "Detected",
            "type": "CBC abnormality"
        })

    # --------------------------------
    # THROMBOCYTOSIS
    # --------------------------------

    thrombocytosis = plt > 450

    if thrombocytosis:
        conditions.append({
            "name": "Thrombocytosis",
            "status": "Detected",
            "type": "CBC abnormality"
        })

    # --------------------------------
    # THROMBOCYTOPENIA
    # --------------------------------

    thrombocytopenia = plt < 150

    if thrombocytopenia:
        conditions.append({
            "name": "Thrombocytopenia",
            "status": "Detected",
            "type": "CBC abnormality"
        })

    # --------------------------------
    # PANCYTOPENIA
    # --------------------------------

    pancytopenia = (
        anemia and
        leuko < 4.5 and
        plt < 150
    )

    if pancytopenia:
        conditions.append({
            "name": "Pancytopenia",
            "status": "Detected",
            "type": "screening"
        })

    # --------------------------------
    # ANEMIA PATTERN
    # --------------------------------

    anemia_pattern = None

    if anemia:

        if mcv < 80:
            anemia_pattern = "Microcytic pattern"

        elif mcv > 100:
            anemia_pattern = "Macrocytic pattern"

        else:
            anemia_pattern = "Normocytic pattern"

    # --------------------------------
    # HYPOCHROMIC PATTERN
    # --------------------------------

    hypochromic = (
        anemia and
        (mch < 27 or mchc < 32)
    )

    if hypochromic:
        conditions.append({
            "name": "Hypochromic pattern",
            "status": "Detected",
            "type": "CBC pattern"
        })

    # --------------------------------
    # ABNORMAL PARAMETERS
    # --------------------------------

    abnormal_parameters = []

    if hb < 12:
        abnormal_parameters.append("Hemoglobin")

    if ery < 4.2 or ery > 5.9:
        abnormal_parameters.append("RBC count")

    if hk < 38 or hk > 50:
        abnormal_parameters.append("Hematocrit")

    if leuko < 4.5 or leuko > 11:
        abnormal_parameters.append("WBC count")

    if plt < 150 or plt > 450:
        abnormal_parameters.append("Platelets")

    if mcv < 80 or mcv > 100:
        abnormal_parameters.append("MCV")

    if mchc < 32 or mchc > 36:
        abnormal_parameters.append("MCHC")

    if mch < 27 or mch > 33:
        abnormal_parameters.append("MCH")

    if rdw > 14.5 or rdw < 11.5:
        abnormal_parameters.append("RDW")

    # --------------------------------
    # SEVERITY
    # --------------------------------

    if hb >= 12:
        severity = "Normal"

    elif hb >= 10:
        severity = "Mild"

    elif hb >= 8:
        severity = "Moderate"

    else:
        severity = "Severe"

    # --------------------------------
    # DOCTOR ALERT
    # --------------------------------

    doctor_alert = (
        severity == "Severe" or
        pancytopenia
    )

    # --------------------------------
    # RECOMMENDATIONS
    # --------------------------------

    recommendations = []

    if anemia:
        recommendations.append(
            "Discuss the abnormal result with a qualified healthcare professional."
        )

    if hypochromic:
        recommendations.append(
            "A healthcare professional may consider further tests to determine the cause of the abnormal red-cell pattern."
        )

    if thrombocytopenia:
        recommendations.append(
            "Discuss the low platelet result with a healthcare professional."
        )

    if thrombocytosis:
        recommendations.append(
            "Discuss the elevated platelet result with a healthcare professional."
        )

    if leukopenia or leukocytosis:
        recommendations.append(
            "Discuss the abnormal white blood cell count with a healthcare professional."
        )

    if polycythemia:
        recommendations.append(
            "Discuss the elevated red-cell/hematocrit pattern with a healthcare professional."
        )

    if doctor_alert:
        recommendations.append(
            "Medical evaluation is recommended because the screening result is concerning."
        )

    if not recommendations:
        recommendations.append(
            "Continue routine health monitoring and follow your healthcare professional's advice."
        )

    return {
        "conditions": conditions,
        "severity": severity,
        "abnormal_parameters": abnormal_parameters,
        "recommendations": recommendations,
        "doctor_alert": doctor_alert,
        "anemia_pattern": anemia_pattern
    }