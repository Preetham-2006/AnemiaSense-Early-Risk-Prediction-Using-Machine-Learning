def chatbot_response(message):

    text = message.lower().strip()

    if "hemoglobin" in text or "hb" in text:
        return (
            "Hemoglobin is a protein in red blood cells that carries "
            "oxygen around the body. Your report can be interpreted "
            "together with other CBC parameters."
        )

    if "mcv" in text:
        return (
            "MCV represents the average size of red blood cells. "
            "It is one of the CBC indices used when evaluating "
            "different blood patterns."
        )

    if "mch" in text:
        return (
            "MCH represents the average amount of hemoglobin in "
            "a red blood cell."
        )

    if "anemia" in text:
        return (
            "Anemia is a condition involving a reduced ability of "
            "the blood to carry oxygen. AnemiaSense provides a "
            "screening prediction and should not be used as a "
            "definitive diagnosis."
        )

    if "doctor" in text or "hospital" in text:
        return (
            "If your report is concerning, or you have significant "
            "symptoms, please contact a qualified healthcare "
            "professional. For emergencies, seek urgent medical care."
        )

    if "platelet" in text:
        return (
            "Platelets help with blood clotting. Very high or very "
            "low platelet values should be interpreted by a healthcare "
            "professional in the context of the complete report."
        )

    if "wbc" in text or "white blood" in text:
        return (
            "WBC refers to white blood cells, which are involved in "
            "immune responses. Abnormal values can have many causes."
        )

    return (
        "I can explain CBC parameters such as Hemoglobin, RBC, "
        "Hematocrit, WBC, Platelets, MCV, MCH, MCHC and RDW. "
        "I can provide general educational information, but I "
        "cannot diagnose a medical condition."
    )