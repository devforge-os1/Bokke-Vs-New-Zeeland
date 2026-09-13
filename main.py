import os
import time
import threading
import logging
from datetime import datetime
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from predictor import RacePredictor
from ai_analyst import AIAnalyst
from auth import SubscriptionAuth, require_subscription
from data_streamer import RealtimeDataStreamer, EventCache
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='.')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SOCKETIO_ASYNC_MODE'] = 'threading'

# Initialize extensions
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize services
predictor = RacePredictor()
analyst = AIAnalyst()
auth = SubscriptionAuth()
streamer = RealtimeDataStreamer(socketio)
cache = EventCache(ttl_seconds=3600)

# Global cache for live race data
LIVE_RACE_CACHE = {
    "last_updated": None,
    "race_info": {},
    "predictions": [],
    "analysis": [],
    "forecast": []
}

# ============== AUTHENTICATION ENDPOINTS ==============

@app.route('/auth/register', methods=['POST'])
def register():
    """Register a new user with subscription."""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        subscription_tier = data.get('subscription_tier', 'basic')
        
        if not user_id or not password:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Hash password
        hashed_password = auth.hash_password(password)
        
        # Generate token
        token = auth.generate_token(user_id, subscription_tier)
        
        logger.info(f"User registered: {user_id} with {subscription_tier} tier")
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'subscription_tier': subscription_tier,
            'token': token,
            'expires_in': 86400
        }), 201
    
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/auth/login', methods=['POST'])
def login():
    """Authenticate user and return token."""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        
        if not user_id or not password:
            return jsonify({'error': 'Missing credentials'}), 400
        
        # In production, verify against database
        # For now, accept any non-empty credentials
        subscription_tier = data.get('subscription_tier', 'basic')
        token = auth.generate_token(user_id, subscription_tier)
        
        logger.info(f"User logged in: {user_id}")
        
        return jsonify({
            'status': 'success',
            'token': token,
            'expires_in': 86400,
            'user_id': user_id,
            'subscription_tier': subscription_tier
        }), 200
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/auth/refresh', methods=['POST'])
def refresh():
    """Refresh an expiring token."""
    try:
        token = request.headers.get('Authorization', '').split(' ')[-1]
        new_token = auth.refresh_token(token)
        
        if not new_token:
            return jsonify({'error': 'Invalid token'}), 401
        
        return jsonify({
            'status': 'success',
            'token': new_token,
            'expires_in': 86400
        }), 200
    
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============== DATA ENDPOINTS ==============

@app.route('/')
def index():
    """Serve the main HTML interface."""
    if os.path.exists('index.html'):
        return send_from_directory('.', 'index.html')
    return jsonify({'error': 'Frontend not found'}), 404


@app.route('/api/predictions', methods=['GET', 'POST'])
@require_subscription()
def get_predictions():
    """Get current race predictions with AI analysis."""
    try:
        # Check cache first
        cached = cache.get('predictions')
        if cached:
            return jsonify(cached), 200
        
        # Fetch live race data
        race_data = fetch_live_race_data()
        cache.set('predictions', race_data)
        
        return jsonify(race_data), 200
    
    except Exception as e:
        logger.error(f"Predictions error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis/<track_id>', methods=['GET'])
@require_subscription()
def get_analysis(track_id):
    """Get detailed AI analysis for a specific track."""
    try:
        analysis = LIVE_RACE_CACHE.get('analysis', [])
        
        return jsonify({
            'track_id': track_id,
            'analysis': analysis,
            'timestamp': datetime.utcnow().isoformat(),
            'analyst': analyst.name
        }), 200
    
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/forecast/<runner_id>', methods=['GET'])
@require_subscription()
def get_forecast(runner_id):
    """Get performance forecast for a runner."""
    try:
        # Sample historical data (in production, fetch from database)
        historical_data = [65, 68, 70, 72, 75, 78]
        
        forecast = predictor.predict_future_performance(
            runner_id,
            historical_data,
            lookahead_days=7
        )
        
        return jsonify(forecast), 200
    
    except Exception as e:
        logger.error(f"Forecast error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'model_version': predictor.model_version,
        'analyst_version': analyst.name
    }), 200


# ============== WEBSOCKET EVENTS ==============

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info(f"Client connected: {request.sid}")
    emit('connection_response', {'status': 'connected', 'data': 'Connected to real-time stream'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info(f"Client disconnected: {request.sid}")
    streamer.stop_stream(request.sid)


@socketio.on('subscribe_to_track')
def handle_subscribe(data):
    """Subscribe to live updates for a track."""
    try:
        track_id = data.get('track_id')
        session_id = request.sid
        
        join_room(session_id)
        
        # Start streaming for this session
        streamer.stream_live_updates(session_id, track_id, interval=5)
        
        logger.info(f"Session {session_id} subscribed to track {track_id}")
        emit('subscription_confirmed', {
            'track_id': track_id,
            'status': 'active',
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Subscription error: {str(e)}")
        emit('error', {'message': str(e)})


@socketio.on('unsubscribe_from_track')
def handle_unsubscribe(data):
    """Unsubscribe from track updates."""
    session_id = request.sid
    streamer.stop_stream(session_id)
    leave_room(session_id)
    logger.info(f"Session {session_id} unsubscribed")
    emit('unsubscription_confirmed', {'status': 'success'})


# ============== DATA FETCHING ==============

def fetch_live_race_data():
    """
    Fetch and enrich live race data with predictions and analysis.
    """
    sample_runners = [
        {"name": "Gimmethegreenlight", "jockey": "S. Khumalo", "trainer": "M. de Kock", "rating": 92, "form": 88, "draw": 1, "weight": "60kg"},
        {"name": "Thunderstruck", "jockey": "R. Fourie", "trainer": "S. Tarry", "rating": 89, "form": 82, "draw": 2, "weight": "58kg"},
        {"name": "Main Defender", "jockey": "C. Zackey", "trainer": "T. Peter", "rating": 85, "form": 78, "draw": 3, "weight": "58kg"},
        {"name": "Royal Victory", "jockey": "G. Lerena", "trainer": "N. Kotzen", "rating": 81, "form": 70, "draw": 4, "weight": "56kg"}
    ]
    
    # Get predictions
    preds = predictor.calculate_probabilities(sample_runners)
    
    # Enrich with runner details
    enriched_preds = []
    for p in preds:
        original = next((r for r in sample_runners if r['name'] == p['runner']), {})
        p.update({
            'jockey': original.get('jockey', 'N/A'),
            'trainer': original.get('trainer', 'N/A'),
            'weight': original.get('weight', '58kg'),
            'draw': original.get('draw', 1)
        })
        enriched_preds.append(p)
    
    # Get analysis
    analysis_input = [{"name": r['name'], "score": r['rating']} for r in sample_runners]
    analysis = analyst.analyze_race(analysis_input)
    
    # Get forecasts
    forecasts = []
    for runner in sample_runners:
        forecast = predictor.predict_future_performance(
            runner['name'],
            [run \n for runner in sample_runners],
            lookahead_days=7
        )
        forecasts.append(forecast)
    
    LIVE_RACE_CACHE.update({
        "last_updated": datetime.utcnow().isoformat(),
        "race_info": {
            "race_name": "Live Event Analysis",
            "track_id": "turffontein",
            "time": datetime.utcnow().strftime('%H:%M'),
            "dist": "1400m",
            "cls": "Grade 1",
            "going": "Good",
            "prizeK": "R1,000,000"
        },
        "predictions": enriched_preds,
        "analysis": analysis,
        "forecast": forecasts
    })
    
    return LIVE_RACE_CACHE


# ============== APPLICATION STARTUP ==============

def auto_launch(url):
    """Auto-launch browser on startup."""
    import subprocess
    try:
        subprocess.Popen(['xdg-open', url])
    except Exception:
        pass


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    
    # Start background scheduler
    streamer.start_scheduler()
    
    # Fetch initial data
    threading.Thread(target=fetch_live_race_data, daemon=True).start()
    
    # Auto-open browser
    threading.Timer(1.5, auto_launch, args=[f"http://127.0.0.1:{port}/"]).start()
    
    # Start the application
    logger.info(f"Starting application on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
