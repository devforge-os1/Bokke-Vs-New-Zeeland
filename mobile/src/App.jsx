import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, ActivityIndicator, Alert } from 'react-native';
import { supabase } from './supabase';
import { AuthService } from './services/authService';
import { RealtimeService } from './services/realtimeService';
import styles from './App.styles';

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [predictions, setPredictions] = useState([]);
  const [liveUpdate, setLiveUpdate] = useState(null);

  const authService = new AuthService(supabase);
  const realtimeService = new RealtimeService(supabase);

  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    if (user) {
      subscribeToRealtime();
    }
  }, [user]);

  const checkAuth = async () => {
    try {
      const session = await authService.getSession();
      setUser(session?.user || null);
    } catch (error) {
      Alert.alert('Auth Error', error.message);
    } finally {
      setLoading(false);
    }
  };

  const subscribeToRealtime = async () => {
    // Subscribe to predictions
    realtimeService.subscribeToPredictions(user.id, (payload) => {
      console.log('Prediction update:', payload);
      fetchPredictions();
      setLiveUpdate(`Updated: ${new Date().toLocaleTimeString()}`);
    });

    // Subscribe to server broadcasts
    realtimeService.subscribeToServerBroadcast('updates', (message) => {
      console.log('Server broadcast:', message);
      setLiveUpdate(message.message);
      fetchPredictions();
    });
  };

  const fetchPredictions = async () => {
    const { data, error } = await realtimeService.getPredictions(user.id);
    if (!error) {
      setPredictions(data);
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  if (!user) {
    return <LoginScreen onAuth={checkAuth} />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>THE CARD</Text>
      {liveUpdate && <Text style={styles.liveUpdate}>🔴 {liveUpdate}</Text>}
      <ScrollView style={styles.predictionsContainer}>
        {predictions.map((pred) => (
          <View key={pred.id} style={styles.predictionCard}>
            <Text style={styles.runnerName}>{pred.runner_name}</Text>
            <Text style={styles.probability}>Win: {pred.win_probability}%</Text>
            <Text style={styles.confidence}>
              Confidence: {(pred.confidence_score * 100).toFixed(1)}%
            </Text>
          </View>
        ))}
      </ScrollView>
    </View>
  );
}

function LoginScreen({ onAuth }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const authService = new AuthService(supabase);

  const handleLogin = async () => {
    try {
      await authService.signIn(email, password);
      onAuth();
    } catch (error) {
      Alert.alert('Login Error', error.message);
    }
  };

  return (
    <View style={styles.loginContainer}>
      <Text style={styles.loginTitle}>THE CARD</Text>
      {/* Add input fields and login button */}
    </View>
  );
}
