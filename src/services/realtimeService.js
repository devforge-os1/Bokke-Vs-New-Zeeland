/**
 * Real-time Service
 * Handles real-time subscriptions and server push notifications
 */
export class RealtimeService {
  constructor(supabaseClient) {
    this.supabase = supabaseClient;
    this.subscriptions = [];
  }

  /**
   * Subscribe to predictions updates for a user
   * Automatically receives updates when server pushes new data
   */
  subscribeToPredictions(userId, onUpdate) {
    const subscription = this.supabase
      .from(`predictions:user_id=eq.${userId}`)
      .on('*', (payload) => {
        console.log('Prediction update:', payload);
        onUpdate(payload);
      })
      .subscribe();

    this.subscriptions.push(subscription);
    return subscription;
  }

  /**
   * Subscribe to server broadcasts
   * Server pushes updates to ALL connected users
   */
  subscribeToServerBroadcast(channel, onMessage) {
    const subscription = this.supabase
      .channel(channel)
      .on('broadcast', { event: 'update' }, (payload) => {
        console.log('Server broadcast:', payload);
        onMessage(payload.data);
      })
      .subscribe();

    this.subscriptions.push(subscription);
    return subscription;
  }

  /**
   * Subscribe to events
   */
  subscribeToEvents(userId, onUpdate) {
    const subscription = this.supabase
      .from(`events:user_id=eq.${userId}`)
      .on('*', (payload) => {
        onUpdate(payload);
      })
      .subscribe();

    this.subscriptions.push(subscription);
    return subscription;
  }

  /**
   * Get predictions for user
   */
  async getPredictions(userId) {
    const { data, error } = await this.supabase
      .from('predictions')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });

    return { data, error };
  }

  /**
   * Unsubscribe from all subscriptions
   */
  unsubscribeAll() {
    this.subscriptions.forEach((sub) => {
      this.supabase.removeSubscription(sub);
    });
    this.subscriptions = [];
  }
}
