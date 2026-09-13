/**
 * Authentication Service
 * Handles user sign up, sign in, and session management
 */
export class AuthService {
  constructor(supabaseClient) {
    this.supabase = supabaseClient;
  }

  // Sign up new user
  async signUp(email, password) {
    const { user, error } = await this.supabase.auth.signUp({
      email,
      password
    });

    if (error) throw error;

    // Create user profile
    await this.createUserProfile(user.id, email);

    return { user, error };
  }

  // Sign in existing user
  async signIn(email, password) {
    const { user, session, error } = await this.supabase.auth.signInWithPassword({
      email,
      password
    });

    if (error) throw error;
    return { user, session, error };
  }

  // Sign out
  async signOut() {
    const { error } = await this.supabase.auth.signOut();
    if (error) throw error;
  }

  // Get current session
  async getSession() {
    const { data: { session }, error } = await this.supabase.auth.getSession();
    if (error) throw error;
    return session;
  }

  // Get current user
  async getUser() {
    const { data: { user }, error } = await this.supabase.auth.getUser();
    if (error) throw error;
    return user;
  }

  // Create user profile
  private async createUserProfile(userId, email) {
    const { error } = await this.supabase
      .from('users')
      .insert([{
        id: userId,
        email,
        subscription_tier: 'basic'
      }]);

    if (error && error.code !== 'PGRST116') {
      // Ignore unique constraint errors
      throw error;
    }
  }

  // Listen to auth changes
  onAuthStateChange(callback) {
    return this.supabase.auth.onAuthStateChange(callback);
  }
}
