# THE CARD — Subscription Analytics Platform

A modern real-time sports event analytics and prediction platform with AI-powered insights.

## Features

### 🔐 Subscription Authentication
- JWT-based token authentication
- Multiple subscription tiers (basic, premium, professional)
- Secure password hashing with bcrypt
- Token refresh mechanism

### 📊 Real-Time Data Streaming
- WebSocket-based live event updates
- Daily data refresh scheduler
- In-memory event cache with TTL
- Multi-session streaming support

### 🤖 AI Analytics
- **AI Analyst**: Sentiment analysis, trend forecasting, and comprehensive race analysis
- **Race Predictor**: Multi-factor probability calculation with confidence scoring
- Performance forecasting with historical data analysis
- Automated recommendation generation

### 📈 Data Processing
- Event data ingestion and transformation
- Performance metrics calculation
- Trend analysis and forecasting
- Batch data refresh (daily 6 AM UTC)

## Project Structure

```
├── main.py              # Flask application with WebSocket support
├── auth.py              # Subscription authentication layer
├── data_streamer.py     # Real-time data streaming and scheduling
├── ai_analyst.py        # Enhanced AI analysis module
├── predictor.py         # Multi-factor prediction engine
├── index.html           # Frontend interface
├── requirements.txt     # Python dependencies
├── .env.example         # Environment configuration template
└── README.md            # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/devforge-os1/Bokke-Vs-New-Zeeland.git
   cd Bokke-Vs-New-Zeeland
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run application**
   ```bash
   python main.py
   ```

   The application will automatically open in your browser at `http://localhost:5050`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get token
- `POST /auth/refresh` - Refresh authentication token

### Data Access (requires authentication)
- `GET /api/predictions` - Get current predictions with AI analysis
- `GET /api/analysis/<track_id>` - Get detailed analysis for track
- `GET /api/forecast/<runner_id>` - Get performance forecast
- `GET /health` - Health check

## WebSocket Events

### Client Events
- `subscribe_to_track` - Subscribe to live track updates
- `unsubscribe_from_track` - Stop receiving track updates

### Server Events
- `connection_response` - Connection confirmation
- `subscription_confirmed` - Track subscription confirmed
- `live_update` - Live event data update
- `data_updated` - Daily data refresh notification
- `data_error` - Error in data processing

## Authentication

All protected endpoints require a bearer token:

```bash
Authorization: Bearer <your_jwt_token>
```

### Token Response
```json
{
  "status": "success",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": 86400,
  "subscription_tier": "basic"
}
```

## Configuration

Edit `.env` file to configure:

- `JWT_SECRET_KEY` - Secret key for token signing
- `DATABASE_URL` - Database connection string
- `DATA_REFRESH_HOUR` - Hour for daily data refresh (UTC)
- `CACHE_TTL_SECONDS` - Cache expiration time

## AI Analysis Models

### AIAnalyst
Provides comprehensive race analysis with:
- Form analysis
- Going compatibility assessment
- Jockey-trainer synergy evaluation
- Trend forecasting
- Sentiment analysis of commentary
- Performance forecasting

### RacePredictor
Calculates probability-based predictions using:
- Rating (35% weight)
- Form (30% weight)
- Draw position (15% weight)
- Jockey-trainer synergy (10% weight)
- Going compatibility (10% weight)

## Real-Time Streaming

### Connection Example
```javascript
const socket = io('http://localhost:5050');

socket.on('connect', () => {
  console.log('Connected to streaming service');
  
  // Subscribe to track updates
  socket.emit('subscribe_to_track', {
    track_id: 'turffontein'
  });
});

socket.on('live_update', (data) => {
  console.log('Live update:', data);
});
```

## Daily Data Refresh

The application automatically refreshes event data daily at 6 AM UTC:
- Fetches latest event information
- Updates analytics cache
- Broadcasts updates to all connected clients
- Maintains historical data for forecasting

## Development

### Running with Debug Mode
```bash
FLASK_ENV=development python main.py
```

### Logging
Logs are written to console with INFO level by default. Modify `logging` configuration in `main.py` to adjust verbosity.

## Security Notes

- Change `SECRET_KEY` and `JWT_SECRET_KEY` in production
- Use environment variables for sensitive configuration
- Enable HTTPS in production
- Implement rate limiting for API endpoints
- Validate all user inputs
- Use strong passwords for database connections

## Performance Optimization

- Event cache reduces database queries
- Background scheduler prevents blocking requests
- WebSocket streaming minimizes polling overhead
- Multi-factor prediction model balances speed and accuracy

## Troubleshooting

### WebSocket Connection Issues
- Ensure WebSocket support is enabled in your proxy/load balancer
- Check CORS configuration if connecting from different domain

### Authentication Errors
- Verify token is being sent in Authorization header
- Check token expiration and refresh if needed
- Ensure subscription tier has access to endpoint

### Data Not Updating
- Check scheduler is running (see logs)
- Verify database connection if using persistent storage
- Check cache TTL configuration

## License

MIT License - See LICENSE file for details

## Support

For issues, feature requests, or questions, please open an issue on GitHub.
