import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = process.env.REACT_APP_SUPABASE_URL || 'https://your-project.supabase.co';
const SUPABASE_KEY = process.env.REACT_APP_SUPABASE_KEY || 'your-anon-key';

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

/**
 * Authentication Service
 */
export const auth = {
  // Sign up new user
  async signUp(email, password) {
    const { user, error } = await supabase.auth.signUp({
      email,
      password
    });
    return { user, error };
  },

  // Sign in existing user
  async signIn(email, password) {
    const { user, session, error } = await supabase.auth.signInWithPassword({
      email,
      password
    });
    return { user, session, error };
  },

  // Sign out
  async signOut() {
    const { error } = await supabase.auth.signOut();
    return { error };
  },

  // Get current session
  async getSession() {
    const { data: { session } } = await supabase.auth.getSession();
    return session;
  },

  // Reset password
  async resetPassword(email) {
    const { data, error } = await supabase.auth.resetPasswordForEmail(email);
    return { data, error };
  },

  // Update password
  async updatePassword(newPassword) {
    const { data, error } = await supabase.auth.updateUser({
      password: newPassword
    });
    return { data, error };
  }
};

/**
 * Database Service - Predictions
 */
export const predictions = {
  // Get all predictions for user
  async getAll(userId) {
    const { data, error } = await supabase
      .from('predictions')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });
    return { data, error };
  },

  // Get single prediction
  async getOne(id) {
    const { data, error } = await supabase
      .from('predictions')
      .select('*')
      .eq('id', id)
      .single();
    return { data, error };
  },

  // Create prediction
  async create(prediction) {
    const { data, error } = await supabase
      .from('predictions')
      .insert([prediction])
      .select()
      .single();
    return { data, error };
  },

  // Update prediction
  async update(id, updates) {
    const { data, error } = await supabase
      .from('predictions')
      .update(updates)
      .eq('id', id)
      .select()
      .single();
    return { data, error };
  },

  // Delete prediction
  async delete(id) {
    const { error } = await supabase
      .from('predictions')
      .delete()
      .eq('id', id);
    return { error };
  },

  // Subscribe to real-time updates
  subscribe(userId, callback) {
    const subscription = supabase
      .from(`predictions:user_id=eq.${userId}`)
      .on('*', payload => {
        callback(payload);
      })
      .subscribe();
    return subscription;
  }
};

/**
 * Database Service - Events
 */
export const events = {
  // Get all events for user
  async getAll(userId, limit = 50) {
    const { data, error } = await supabase
      .from('events')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(limit);
    return { data, error };
  },

  // Create event
  async create(event) {
    const { data, error } = await supabase
      .from('events')
      .insert([event])
      .select()
      .single();
    return { data, error };
  },

  // Subscribe to events
  subscribe(userId, callback) {
    const subscription = supabase
      .from(`events:user_id=eq.${userId}`)
      .on('*', payload => {
        callback(payload);
      })
      .subscribe();
    return subscription;
  }
};

/**
 * Database Service - User Profile
 */
export const profile = {
  // Get user profile
  async getProfile(userId) {
    const { data, error } = await supabase
      .from('users')
      .select('*')
      .eq('id', userId)
      .single();
    return { data, error };
  },

  // Create profile
  async createProfile(userId, userData) {
    const { data, error } = await supabase
      .from('users')
      .insert([{
        id: userId,
        ...userData
      }])
      .select()
      .single();
    return { data, error };
  },

  // Update profile
  async updateProfile(userId, updates) {
    const { data, error } = await supabase
      .from('users')
      .update(updates)
      .eq('id', userId)
      .select()
      .single();
    return { data, error };
  }
};

// Auth state listener
export const onAuthStateChange = (callback) => {
  return supabase.auth.onAuthStateChange((event, session) => {
    callback(event, session);
  });
};
