import os
import time
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
RACE_API_KEY = os.getenv("RACE_API_KEY")
MARKET_API_KEY = os.getenv("MARKET_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

AI_MODEL_VERSION = os.getenv("AI_MODEL_VERSION", "2.0")
DATA_FETCH_INTERVAL = int(os.getenv("DATA_FETCH_INTERVAL", 300))
MAX_PREDICTIONS_PER_CYCLE = int(os.getenv("MAX_PREDICTIONS_PER_CYCLE", 1000))

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_race_data():
    headers = {"Authorization": f"Bearer {RACE_API_KEY}"}
    # Replace with your actual race API endpoint
    response = requests.get("https://api.racingapi.example/v1/data", headers=headers)
    return response.json() if response.status_code == 200 else None

def fetch_market_data():
    headers = {"Authorization": f"Bearer {MARKET_API_KEY}"}
    # Replace with your actual market API endpoint
    response = requests.get("https://api.marketapi.example/v1/data", headers=headers)
    return response.json() if response.status_code == 200 else None

def fetch_weather_data():
    headers = {"Authorization": f"Bearer {WEATHER_API_KEY}"}
    # Replace with your actual weather API endpoint
    response = requests.get("https://api.weatherapi.example/v1/data", headers=headers)
    return response.json() if response.status_code == 200 else None

def push_to_supabase(table_name, payload):
    data, count = supabase.table(table_name).insert(payload).execute()
    return data

def run_orchestrator():
    print(f"Starting AI Model Orchestrator v{AI_MODEL_VERSION}")
    
    while True:
        print("Fetching fresh data from Race, Market, and Weather APIs...")
        
        race_data = fetch_race_data()
        market_data = fetch_market_data()
        weather_data = fetch_weather_data()
        
        # Process and structure prediction payload here up to MAX_PREDICTIONS_PER_CYCLE
        payload = {
            "race": race_data,
            "market": market_data,
            "weather": weather_data,
            "timestamp": time.time()
        }
        
        # Push results to Supabase table so frontend displays them
        try:
            push_to_supabase("predictions", payload)
            print("Successfully updated Supabase with latest prediction cycle.")
        except Exception as e:
            print(f"Failed to push to Supabase: {e}")
            
        time.sleep(DATA_FETCH_INTERVAL)

if __name__ == "__main__":
    run_orchestrator()

