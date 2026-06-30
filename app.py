from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
# CORS komplett für alle Browser-Anfragen freischalten
CORS(app, resources={r"/*": {"origins": "*"}})

# Groq Client mit dem kostenlosen Key initialisieren
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

# Geändert von /api/generate-plan zu /generate, damit es exakt zum JavaScript passt
@app.route('/generate', methods=['POST'])
def generate_plan():
    data = request.json or {}
    weight = data.get('weight', 80)
    height = data.get('height', 180)
    activity = data.get('activity', 'moderate')
    goal = data.get('goal', 'muscle')

    try:
        system_instructions = (
            "Du bist ein zertifizierter KI-Fitness-Coach und Ernährungsberater. "
            "Erstelle präzise, motivierende und strukturierte Pläne. "
            "Nutze Emojis für eine ansprechende Formatierung. Antworte immer auf Deutsch."
        )
        
        user_prompt = f"""
        Erstelle einen kombinierten Trainings- und Ernährungsplan basierend auf folgenden Daten:
        - Gewicht: {weight} kg
        - Größe: {height} cm
        - Aktivitätslevel: {activity}
        - Ziel: {goal}
        
        Bitte teile die Antwort übersichtlich in zwei Hauptbereiche auf:
        1. 🍏 ERNÄHRUNGSPLAN (Makronährstoffe & Beispieltag)
        2. 🏋️ TRAININGSPLAN (Fokus & Beispiel-Workout)
        """

        # Das aktive, kostenlose Nachfolgemodell von Groq abfragen
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_prompt}
            ], 
            temperature=0.7
        )

        real_ki_plan = response.choices[0].message.content
        return jsonify({"status": "success", "plan": real_ki_plan})
    except Exception as e:
        print("\n!!! KI-ABSTURZ-FEHLER:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Geändert von Port 5000 auf Port 5005, damit Nginx die App erreichen kann
    app.run(host='0.0.0.0', port=5005, debug=True)
