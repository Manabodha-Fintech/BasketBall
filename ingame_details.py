import pandas as pd
import requests
import os

def get_event_dataframe(game_id, league):
    try:
        # print(os.getenv("SPORTSRADAR_API_KEY"))
        # Example usage with your API call:
        url = f"https://api.sportradar.com/{league}/trial/v7/en/games/{game_id}/statistics.json" if league =='ncaafb' else f"https://api.sportradar.com/{league}/official/trial/v7/en/games/{game_id}/statistics.json"
        # url = "https://api.sportradar.com/nc?aafb/trial/v7/en/games/fefcd061-2c97-4356-bf87-d11b398148fc/statistics.json"
        
        headers = {
            "accept": "application/json",
            "x-api-key": os.getenv("SPORTSRADAR_API_KEY"),
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an HTTPError for bad status codes

        json_data = response.json()
        print(json_data)
        game_df = create_game_dataframe(json_data)
        print(game_df)
        return game_df
        
    except requests.exceptions.RequestException as e:
        # Handle any request-related errors (connection, timeout, HTTP errors, etc.)
        print(f"Request error occurred: {e}")
        # raise Exception(f"Failed to fetch ingame data for game_id {game_id}.Also ensure you are passing correct game_id for correct league, Error: {e}")
        raise Exception(
    f"Failed to fetch in-game data for game_id {game_id}. "
    f"Ensure that you are passing the correct game_id for the correct league. "
    f"For example, use an NFL game_id with the NFL league and an NCAAFB game_id with the NCAAFB league — mixing them will not work. "
    f"Error: {e}"
)
    except ValueError as e:
        # Handle JSON parsing errors
        print(f"JSON parsing error: {e}")
        raise Exception(f"Failed to parse response for game_id {game_id}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")
        raise Exception(f"An unexpected error occurred while processing game_id {game_id}")