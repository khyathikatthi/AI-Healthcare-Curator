  from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import gdown
import joblib

app = Flask(_name_)

MODEL_URL = "https://drive.google.com/uc?id=1--3ORXu68J6Vb9BL1bskE8KZygxv6hwO"
MODEL_PATH = "disease_model.pkl"

if not os.path.exists(MODEL_PATH): 
    print("Downloading model...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model Loaded Successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

SYMPTOMS_LIST = [
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering",
    "chills", "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue",
    "blackheads", "scurring", "skin_peeling", "silver_like_dusting",
    "small_dents_in_nails", "inflammatory_nails", "blister", "red_sore_around_nose",
    "yellow_crust_ooze", "muscle_wasting", "burning_micturition", "vomiting", "spotting_ urination", 
    "fatigue", "anxiety", "cold_hands_and_feets", "mood_swings","weight_loss", "restlessness", "lethargy", 
    "patches_in_throat", "irregular_sugar_level", "cough","high_fever","sunken_eyes","breathlessness",
    "sweating","dehydration","indigestion","headache",	"yellowish_skin",	"dark_urine",	
    "nausea",	"loss_of_appetite",	"pain_behind_the_eyes",	"back_pain",	"constipation",	"abdominal_pain",
    "diarrhoea",	"mild_fever",	"yellow_urine",	"yellowing_of_eyes",	"acute_liver_failure",	"fluid_overload",
    "swelling_of_stomach","swelled_lymph_nodes",	"malaise",	"blurred_and_distorted_vision",	"phlegm",	"throat_irritation",
    "redness_of_eyes",	"sinus_pressure",	"runny_nose",	"congestion",	"chest_pain",	"weakness_in_limbs",	"fast_heart_rate",
    "pain_during_bowel_movements",	"pain_in_anal_region",	"bloody_stool",	"irritation_in_anus",	"neck_pain",	"dizziness",	"cramps",	"bruising",	"obesity",
    "swollen_legs",	"swollen_blood_vessels",	"puffy_face_and_eyes",	"enlarged_thyroid",	"brittle_nails",	"swollen_extremeties",	"excessive_hunger",	
    "extra_marital_contacts",	"drying_and_tingling_lips",	"slurred_speech",	"knee_pain",	"hip_joint_pain",	"muscle_weakness",	"stiff_neck",	"swelling_joints",
    "movement_stiffness",	"spinning_movements",	"loss_of_balance",	"unsteadiness",	"weakness_of_one_body_side",	"loss_of_smell",	"bladder_discomfort",
    "foul_smell_of urine", "continuous_feel_of_urine",	"passage_of_gases",	"internal_itching",	"toxic_look_(typhos)",	"depression",	"irritability",
    "muscle_pain",	"altered_sensorium",	"red_spots_over_body",	"belly_pain",	"abnormal_menstruation",	"dischromic _patches",	"watering_from_eyes",
    "increased_appetite",	"polyuria",	"family_history","mucoid_sputum",	"rusty_sputum",	"lack_of_concentration",	"visual_disturbances",	"receiving_blood_transfusion",
    "receiving_unsterile_injections",	"coma",	"stomach_bleeding", "distention_of_abdomen",	"history_of_alcohol_consumption",	"fluid_overload",
    "blood_in_sputum"	,"prominent_veins_on_calf",	"palpitations",	"painful_walking",	"pus_filled_pimples",	"scurring"    
]

DISEASES = {
    0: "Fungal infection",
    1: "Allergy",
    2: "GERD",
    3: "Chronic cholestasis",
    4: "Drug Reaction",
    5: "Peptic ulcer disease",
    6: "AIDS",
    7: "Diabetes",
    8: "Gastroenteritis",
    9: "Bronchial Asthma",
    10: "Hypertension",
    11: "Migraine",
    12: "Cervical spondylosis",
    13: "Paralysis (brain hemorrhage)",
    14: "Jaundice",  # Your model predicted this
    15: "Malaria",
    16: "Chicken pox",
    17: "Dengue",
    18: "Typhoid",
    19: "Hepatitis A",
    20: "Hepatitis B",
    21: "Hepatitis C",
    22: "Hepatitis D",
    23: "Hepatitis E",
    24: "Alcoholic hepatitis",
    25: "Tuberculosis",
    26: "Common Cold",
    27: "Pneumonia",
    28: "Dimorphic Hemorrhoids (Piles)",
    29: "Heart attack",
    30: "Varicose veins",
    31: "Hypothyroidism",
    32: "Hyperthyroidism",
    33: "Hypoglycemia",
    34: "Osteoarthritis",
    35: "Arthritis",
    36: "Vertigo",
    37: "Acne",
    38: "Urinary tract infection",
    39: "Psoriasis",
    40: "Impetigo"
}

@app.route('/')
def home():
    return "Welcome to the Disease Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Check the file path.'}), 500

    try:
        data = request.get_json()
        symptoms = data.get('symptoms', {})

        # Debugging print statement
        print("🔍 Received symptoms:", symptoms)

        # Convert input to feature array
        input_features = np.array([symptoms.get(symptom, 0) for symptom in SYMPTOMS_LIST])

        # Ensure correct shape
        input_features = input_features.reshape(1, -1)

        # Make prediction
        predicted_index = model.predict(input_features)[0]
        predicted_disease = DISEASES.get(predicted_index, "Unknown Disease")  # Convert index to name

        return jsonify({'predicted_disease': predicted_disease})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000, debug=True)
