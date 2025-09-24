import requests
import os
import json
from datetime import datetime, timedelta, timezone
# from dotenv import load_dotenv  
# load_dotenv()

def get_closed_games_for_date(league):
    date = datetime.now(timezone.utc).date()
    # print(date)
    # nba = 2024-10-22
    #ncaamb = 2025-03-03
    year = date.year
    month = date.month
    day = date.day
    # url = f"https://api.sportradar.com/nba/production/v8/en/games/{year}/{month:02d}/{day:02d}/schedule.json"
    url = f"https://api.sportradar.com/{league}/production/v8/en/games/{year}/{month}/{day}/schedule.json"

    # print(url)
    
    headers = {
        "accept": "application/json",
        "x-api-key": os.getenv('SPORTSRADAR_API_KEY')
    }

    # nba API call
    response = requests.get(url, headers=headers)
    data = response.json()
    # print(data)
    
    closed_games = []

    if len(data.get("games")):
        for game in data.get("games", []):
            status = game.get("status")
            game_id = game.get("id")

            if status == "closed":
                closed_games.append(game_id)
    else:
        print(f"no {league} game was scheduled on {date}")
    
    return closed_games

