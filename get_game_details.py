import requests
import time
import os
from typing import List, Dict, Any, Optional

# Constants
API_BASE_URL = "https://api.sportradar.com/nba/production/v8/en/games"
MAX_RETRIES = 5
BACKOFF_FACTOR = 1.5
REQUEST_TIMEOUT = 30

def fetch_with_retry(url: str, params: Dict[str, str], retries: int = MAX_RETRIES, 
    backoff_factor: float = BACKOFF_FACTOR) -> Optional[Dict[str, Any]]:
    """Fetch data from API with retry logic. Returns JSON dict on success or None on failure."""
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return response.json()  # Return JSON directly
            print(f"Non-200 status ({response.status_code}) from {url}. Retrying...")
        except (requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout, 
                requests.exceptions.RequestException) as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
        
        sleep_time = backoff_factor ** (attempt + 1)
        print(f"Retrying in {sleep_time:.1f} seconds...")
        time.sleep(sleep_time)
    
    print(f"Failed to fetch {url} after {retries} attempts.")
    return None

def fetch_game_details(game_id: str) -> Optional[Dict[str, Any]]:
    """Fetch game details for a single game ID. Returns JSON dict or None."""
    url = f"{API_BASE_URL}/{game_id}/summary.json"
    params = {"api_key": os.getenv('SPORTSRADAR_API_KEY')}
    data = fetch_with_retry(url, params)
    
    if data:
        return data
    else:
        print(f"Skipping game {game_id} due to repeated failures.")
        return None

def process_game_ids(game_ids: List[str]) -> List[Dict[str, Any]]:
    """Fetch game details for all game IDs and return a list of JSON data."""
    all_games_data = []
    total = len(game_ids)
    
    for count, game_id in enumerate(game_ids, start=1):
        game_data = fetch_game_details(game_id)
        if game_data:
            all_games_data.append(game_data)
            print(f"{count}/{total} Fetched data for game {game_id}")
        time.sleep(1)  # Optional rate limiting
    
    return all_games_data

# Example usage:
# game_ids = ["a06b10fa-fd80-4058-9e0a-d3d1d69cb6f1", "4c189e09-fabf-4608-a2bf-f0f77d8e2bbf"]
# games_data = process_game_ids(game_ids)
# print(games_data)
