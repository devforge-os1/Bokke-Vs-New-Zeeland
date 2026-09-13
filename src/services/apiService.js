/**
 * Backend API Service
 * Single API endpoint that updates server and pushes to all users
 */

export class APIService {
  constructor(apiUrl) {
    this.apiUrl = apiUrl;
  }

  /**
   * Update race predictions
   * ONE API CALL updates the database
   * Server automatically broadcasts to ALL connected users
   */
  async updatePredictions(predictions) {
    try {
      const response = await fetch(`${this.apiUrl}/api/predictions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getToken()}`
        },
        body: JSON.stringify({
          predictions,
          timestamp: new Date().toISOString()
        })
      });

      if (!response.ok) {
        throw new Error('Failed to update predictions');
      }

      const data = await response.json();
      console.log('Predictions updated, broadcasting to users...');
      return data;
    } catch (error) {
      console.error('API error:', error);
      throw error;
    }
  }

  /**
   * Update event data
   * Automatically broadcasts to all connected users
   */
  async updateEvent(eventData) {
    try {
      const response = await fetch(`${this.apiUrl}/api/events`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getToken()}`
        },
        body: JSON.stringify(eventData)
      });

      if (!response.ok) {
        throw new Error('Failed to update event');
      }

      return await response.json();
    } catch (error) {
      console.error('API error:', error);
      throw error;
    }
  }

  /**
   * Publish analysis results
   * Server pushes to all clients via WebSocket
   */
  async publishAnalysis(analysis) {
    try {
      const response = await fetch(`${this.apiUrl}/api/analysis/publish`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getToken()}`
        },
        body: JSON.stringify(analysis)
      });

      if (!response.ok) {
        throw new Error('Failed to publish analysis');
      }

      const data = await response.json();
      console.log('Analysis published to all users');
      return data;
    } catch (error) {
      console.error('API error:', error);
      throw error;
    }
  }

  /**
   * Get auth token from Supabase
   */
  async getToken() {
    const token = localStorage.getItem('sb_token');
    return token;
  }
}
