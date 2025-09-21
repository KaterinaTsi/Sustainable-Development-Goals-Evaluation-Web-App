from flask import Blueprint, render_template, request, jsonify
from database import handle_database_interactions, get_indicator_weights

views = Blueprint('views', __name__)

# Δείκτες για κάθε ΣΒΑ
sdg_indicators = {
    "SDG01": ["I1", "I2"],
    "SDG02": ["I3", "I4"],
    "SDG03": ["I5", "I6"],
    "SDG04": ["I7", "I8"],
    "SDG05": ["I9", "I10", "I11", "I12"],
    "SDG06": ["I13", "I14"],
    "SDG07": ["I15", "I16", "I17"],
    "SDG08": [],
    "SDG09": ["I18"],
    "SDG10": ["I19"],
    "SDG11": ["I20", "I21"],
    "SDG12": ["I22", "I23", "I24"],
    "SDG13": ["I25", "I26"],
    "SDG14": ["I27"],
    "SDG15": ["I28"],
    "SDG16": ["I29"],
    "SDG17": ["I30", "I31", "I32", "I33", "I34"]
}


@views.route("/", methods=["GET", "POST"])       #Συναρτηση που συνδεεται με το html και το προγραμμα βασης
def add_sdg():
    if request.method == "POST":
        sdg_scores = {}
        sdg_eval_years = {}

        for sdg, indicators in sdg_indicators.items():
            for indicator in indicators:
                
                # Έτος αξιολόγησης για αυτόν τον δείκτη
                evalyear_key = f"evalyear_{indicator}"
                evalyear_value = request.form.get(evalyear_key)

                # Βαθμολογία για δεικτες που απαιτουν διαίρεση
                if indicator in ["I3", "I8", "I9", "I13", "I17", "I18", "I24", "I30"]:
                    numerator_key = f"score_{indicator}_numerator"
                    denominator_key = f"score_{indicator}_denominator"

                    numerator = request.form.get(numerator_key, None)         #αριθμητης
                    denominator = request.form.get(denominator_key, None)       #παρανομαστης

                    if numerator is None or denominator is None:  # ελεγχος υπαρξης πεδιου
                        print(f"Λείπει το πεδίο: {numerator_key} ή {denominator_key}")
                        return jsonify({'status': 'error', 'message': f'Missing field: {numerator_key} or {denominator_key}'}), 400

                    try:
                        numerator = float(numerator)
                        denominator = float(denominator) if float(denominator) != 0 else 1  # Αποφυγή διαίρεσης με μηδέν
                        sdg_scores[indicator] = numerator / denominator                    # πραξη διαιρεσης
                    except ValueError:
                        sdg_scores[indicator] = 0.0  # Αν υπάρχει μη έγκυρη τιμή

                    print(f"Debug {indicator}: {numerator} / {denominator} = {sdg_scores[indicator]}")

                # Αν ο δείκτης δεν απαιτεί διαίρεση
                else:
                    score_key = f"score_{indicator}"
                    score_value = request.form.get(score_key)
                    # Αποθήκευση της βαθμολογίας (αν έχει δοθεί)
                    if score_value not in (None, ""):
                        try:
                            sdg_scores[indicator] = float(score_value)
                        except ValueError:
                            sdg_scores[indicator] = 0.0   

                # Debug εκτύπωση για έλεγχο των δεδομένων
                print(f"Debug score: {score_key} = {score_value}")
                print(f"Debug evalYear: {evalyear_key} = {evalyear_value}")

                # Αποθήκευση του έτους αξιολόγησης για αυτόν τον δείκτη
                if evalyear_value not in (None, ""):
                    sdg_eval_years[indicator] = evalyear_value
                else:
                    # Εναλλακτική λύση αν ο χρήστης το αφήσει κενό (απίθανο αν είναι required) 
                    sdg_eval_years[indicator] = "2023"

        # Επιστροφή των αποτελεσμάτων στον function handle_database_interactions
        response = handle_database_interactions(sdg_scores, sdg_eval_years)
        return jsonify(response)
    else:
        # Επιστροφή της φόρμας για την προσθήκη δεδομένων
        indicator_weights = get_indicator_weights() # Ανάκτηση του βάρους των δεικτών
        return render_template("add_sdg.html", sdg_indicators=sdg_indicators, indicator_weights=indicator_weights)
