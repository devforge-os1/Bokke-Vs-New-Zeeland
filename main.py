@app.route('/')                                                 def index():                                                        if os.path.exists('index.html'):                                    return send_from_directory('.', 'index.html')               elif os.path.exists('the-card.html'):                               return send_from_directory('.', 'the-card.html')            return 'Index file not found', 404
                                                                
def auto_launch(url):                                               import subprocess                                               try:                                                                subprocess.run(['termux-open-url', url], check=False)
    except Exception:                                                   pass
                                                                import os
import time                                                     import threading
import subprocess                                               import webbrowser
from flask import Flask, jsonify, send_from_directory           from flask_cors import CORS                                     from predictor import RacePredictor
from ai_analyst import AIAnalyst                                                                                                app = Flask(__name__, static_folder='.')
CORS(app)                                                       
predictor = RacePredictor()
analyst = AIAnalyst()

# Global memory state for live race updates
LIVE_RACE_CACHE = {
    "last_updated": None,
    "race_info": {},
    "predictions": [],
    "analysis": []
}


def fetch_live_race_data():
    sample_runners = [
        {"name": "Gimmethegreenlight", "jockey": "S. Khumalo", "trainer": "M. de Kock", "rating": 92, "form": 88, "draw": 1, "weight": "60kg"},
        {"name": "Thunderstruck", "jockey": "R. Fourie", "trainer": "S. Tarry", "rating": 89, "form": 82, "draw": 2, "weight": "58kg"},
        {"name": "Main Defender", "jockey": "C. Zackey", "trainer": "T. Peter", "rating": 85, "form": 78, "draw": 3, "weight": "58kg"},
        {"name": "Royal Victory", "jockey": "G. Lerena", "trainer": "N. Kotzen", "rating": 81, "form": 70, "draw": 4, "weight": "56kg"}
    ]

    preds = predictor.calculate_probabilities(sample_runners)

    # Merge additional runner details back into predictions
    enriched_preds = []
    for p in preds:
        original = next((r for r in sample_runners if r['name'] == p['runner']), {})
        p['jockey'] = original.get('jockey', 'N/A')
        p['trainer'] = original.get('trainer', 'N/A')
        p['weight'] = original.get('weight', '58kg')
        p['draw'] = original.get('draw', 1)
        enriched_preds.append(p)

    analysis_input = [{"name": r['name'], "score": r['rating']} for r in sample_runners]
    analysis = analyst.analyze_race(analysis_input)

    return {
        "race_name": "Gauteng Summer Cup Preview",
        "track_id": "turffontein",
        "time": "15:15",
        "dist": "1400m",
        "cls": "Grade 1",
        "going": "Good",
        "prizeK": "R1,000,000",
        "predictions": enriched_preds,
        "analysis": analysis
    }

def serve_index():
    return send_from_directory('.', 'index.html')

# Live Endpoint hit by index.html automatically
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        if 'predictor' in globals():
            data = predictor.get_live_predictions()
        elif 'RacePredictor' in globals():
            engine = RacePredictor()
            data = engine.get_live_predictions()
        else:
            from predictor import RacePredictor
            engine = RacePredictor()
            data = engine.get_live_predictions()
        return jsonify({'status': 'Active', 'live_data': data})
    except Exception as e:
        return jsonify({'status': 'Error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))

    # Start live prediction engine worker thread
    threading.Thread(target=fetch_live_race_data, daemon=True).start()

    # Auto-open browser
    threading.Timer(1.5, auto_launch, args=[f"http://127.0.0.1:{port}/"]).start()

    app.run(host='0.0.0.0', port=port)
