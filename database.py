import uuid
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from flask import Flask, request, render_template, jsonify
import string, random

# Placeholder config για σύνδεση με τη βάση δεδομένων
config = {
    "host": "localhost",   #βαλτε το δικό σας host name
    "user": "root",     # βάλτε το δικό σας ονομα user
    "password": "MYdatabase23!",  # βάλτε τον κωδικο βασης σας
    "database": "WEBSITE"   # βαλτε τοο ονομα βασης σας
}

app = Flask(__name__)

# Δημιουργία σύνδεσης με τη βάση δεδομένων
def create_connection():
    return mysql.connector.connect(
        host="localhost",            #βαλτε το δικό σας host name
        user="root",                    # βάλτε το δικό σας ονομα user
        password="MYdatabase23!",                # κωδικος βασης
        database="WEBSITE"          # ονομα βασης
    )

#Συναρτηση που παιρνει τα βάρη για κάθε δείκτη απο την βάση
def get_indicator_weights():
    connection = create_connection()        #δημιουργια συνδεσς
    if not connection:
        return {}

    cursor = connection.cursor()
    weights = {}

    try:
        cursor.execute("SELECT INDICATOR, WEIGHT FROM INDICATORS")  
        rows = cursor.fetchall()
        for row in rows:
            indicator = f"I{row[0]}"
            weight = row[1]
            weights[indicator] = weight

    except Error as e:
        print(f"Error fetching weights: {e}")
    finally:
        cursor.close()
        connection.close()

    return weights


# Συνάρτηση για την διαχείριση αλληλεπιδράσεων με τη βάση δεδομένων
def handle_database_interactions(sdg_scores, sdg_eval_years):
    connection = create_connection()
    if not connection:
        return {'status': 'error', 'message': 'No DB connection'}

    cursor = connection.cursor()
    session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))    #session id
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    final_scores = {}  # θα αποθηκεύσει τη συνολική και σταθμισμένη βαθμολογία για κάθε δείκτη

    try:
        for indicator, score in sdg_scores.items():
            eval_year = sdg_eval_years.get(indicator, "2023") # προεπιλογη 2023
            indicator_fk = int(indicator[1:])     #μετατροπή string σε αριθμο πχ Ι1-> 1

            # Εισαγωγή βασικών εγγραφών
            cursor.execute("INSERT IGNORE INTO INDICATORS (INDICATOR) VALUES (%s)", (indicator_fk,))
            cursor.execute("""
                INSERT INTO USER_DATA (USER_ID, INDICATOR_ID, USER_RATING, CREATED_AT)
                VALUES (%s, %s, %s, %s)
            """, (session_id, indicator_fk, score, current_date))
            cursor.execute("""
                INSERT INTO RESULTS (USER_ID, INDICATOR_ID, RATING, EVALUATION_YEAR)
                VALUES (%s, %s, %s, %s)
            """, (session_id, indicator_fk, score, eval_year))

            # Υπολογισμός συνολικής βαθμολογίας για δείκτες με πράξη διαίρεσης
            if indicator in ["I3", "I8", "I9", "I13", "I17", "I18", "I24", "I30"]: 
                if indicator in ["I8", "I9", "I18", "I30"]: # στηλη G ελεγχος if για κάθε ποσοστό
                   if score < 1:              # if percentage<1
                      total_score = 0        # Η = 0
                   else:
                       total_score = score   # H = G = percentage change
                else:
                    if score < 1:
                        total_score = 1 / score   # 1/percentage = H (Στήλη H = VALUES στο EXCEL)
                    elif score > 1:
                        total_score = 0       # H = 0

                # Debug: Εκτύπωση για έλεγχο των δεδομένων διαίρεσης
                print(f"Debug {indicator}: score = {score}, total_score = {total_score}")
                   
            else:                           # Υπολογισμός συνολικής βαθμολογίας για δείκτες ΧΩΡΙΣ ΔΙΑΙΡΕΣΗ
                 cursor.execute("""
                      SELECT COALESCE(SUM(RATING), 0)
                      FROM RESULTS
                      WHERE INDICATOR_ID = %s AND EVALUATION_YEAR = %s
                     """, (indicator_fk, eval_year))
                 row = cursor.fetchone()
                 total_score = row[0] if row else 0

            # Ανάκτηση βάρους από τον πίνακα INDICATORS
            cursor.execute("SELECT WEIGHT FROM INDICATORS WHERE INDICATOR = %s", (indicator_fk,))
            row = cursor.fetchone()
            weight = row[0] if row and row[0] is not None else 1.0

            #υπολογισμός σταθμισμενης βαθμολογίας  ( D * H )
            weighted_score = total_score * weight

            # Μονο 3 δεκαδικα ψηφία στο αποτελεσμα
            weighted_score = round(weighted_score, 3)
            total_score = round(total_score, 3)

            # Αποθήκευση αυτών σε ένα λεξικό για επιστροφή
            final_scores[indicator] = {
                'total_score': total_score,
                'weighted_score': weighted_score
            }

        connection.commit()
        return {
            'status': 'success',
            'message': 'Data submitted successfully',
            'final_scores': final_scores
        }

    except Exception as e:
        connection.rollback()
        return {'status': 'error', 'message': str(e)}
    finally:
        cursor.close()
        connection.close()          # κλεισιμο συδεσης