from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Erlaubt dem Browser den Zugriff ohne Timeout!

app = Flask(__name__)
CORS(app)  # Schaltet den CORS-Schutz für deinen Test frei

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    data = request.json or {}
    weight = data.get('weight', 80)
    goal = data.get('goal', 'Muskelaufbau')

    real_ki_plan = f"""
    === REINER NETZWERK-TEST ===
    Gewicht: {weight} kg | Ziel: {goal}
    Das Netzwerk und der Browser-Zugriff funktionieren jetzt blitzschnell!
    """
    return jsonify({"status": "success", "plan": real_ki_plan})

if __name__ == '__main__':
    # Geändert von 5000 auf 8080, um Scannern zu entkommen
    app.run(host='0.0.0.0', port=8080, debug=True)