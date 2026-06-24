from flask import Flask, request, jsonify, render_template
import mysql.connector
import os
from openai import OpenAI  # Offizielle OpenAI-Bibliothek laden

app = Flask(__name__)

# Initialisiere den OpenAI Client (liest den Schlüssel automatisch aus der Umgebungsvariable OPENAI_API_KEY)
# Für Azure OpenAI würde die Initialisierung leicht abweichen, das hier ist für die Standard OpenAI-API.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def save_to_db(weight, height, activity, goal, plan):
    """Speichert den generierten KI-Plan in deiner MySQL-Datenbank"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Shahzad-1998", 
            database="fitness_db"
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_plans (
                id INT AUTO_INCREMENT PRIMARY KEY,
                weight INT,
                height INT,
                activity VARCHAR(255),
                goal VARCHAR(255),
                generated_plan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        query = "INSERT INTO user_plans (weight, height, activity, goal, generated_plan) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (weight, height, activity, goal, plan))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Datenbankfehler: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    data = request.json
    weight = data.get('weight')
    height = data.get('height')
    activity = data.get('activity')
    goal = data.get('goal')

    try:
        # Prompt für die KI dynamisch aus den Formular-Werten zusammenbauen
        system_instructions = (
            "Du bist ein zertifizierter KI-Fitness-Coach und Ernährungsberater. "
            "Erstelle präzise, motivierende und strukturierte Pläne. "
            "Nutze Emojis für eine ansprechende Formatierung."
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

        # Echte API-Abfrage an OpenAI (Nutzt gpt-4o für schnelle, starke Ergebnisse)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        # Den generierten Text extrahieren
        real_ki_plan = response.choices.message.content

        # Speichert den echten KI-Plan in der MySQL-Datenbank
        save_to_db(weight, height, activity, goal, real_ki_plan)

        return jsonify({"status": "success", "plan": real_ki_plan})

    except Exception as e:
        # Fehlermeldung zurückgeben, falls z.B. der API-Key fehlt
        return jsonify({"status": "error", "message": f"KI-Fehler: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
