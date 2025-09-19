import pandas as pd
import requests
import os

def create_game_dataframe(json_data):
    """
    Create a DataFrame from the JSON response containing venue, home team, and away team details.
    
    Args:
        json_data (dict): JSON response from the API
    
    Returns:
        pandas.DataFrame: DataFrame with game, venue, home team, and away team details
    """
    # Extract the main game information
    game_data = {
        'game_id': json_data.get('id'),
        'status': json_data.get('status'),
        'scheduled': json_data.get('scheduled'),
        'entry_mode': json_data.get('entry_mode'),
        'sr_id': json_data.get('sr_id'),
        'game_type': json_data.get('game_type'),
        'conference_game': json_data.get('conference_game'),
        'season_year': json_data.get('season', {}).get('year'),
        'season_type': json_data.get('season', {}).get('type'),
        # 'week_sequence': json_data.get('summary', {}).get('week', {}).get('sequence'),   #not exits
        # 'week_title': json_data.get('summary', {}).get('week', {}).get('title'),  #not exists
        # 'broadcast_network': json_data.get('broadcast', {}).get('network')   #is an array
    }
    
    # Extract venue information
    venue = json_data.get('venue', {})
    venue_data = {
        'venue_id': venue.get('id'),
        'venue_name': venue.get('name'),
        'venue_city': venue.get('city'),
        'venue_state': venue.get('state'),
        'venue_country': venue.get('country'),
        'venue_zip': venue.get('zip'),
        'venue_address': venue.get('address'),
        'venue_capacity': venue.get('capacity'),
        'venue_surface': venue.get('surface'),
        'venue_roof_type': venue.get('roof_type'),
        'venue_sr_id': venue.get('sr_id'),
        'venue_lat': venue.get('location', {}).get('lat'),
        'venue_lng': venue.get('location', {}).get('lng')
    }
    
    # Extract home team information
    home = json_data.get('home', {})
    home_data = {
        'home_team_id': home.get('id'),
        'home_team_name': home.get('name'),
        'home_team_market': home.get('market'),
        'home_team_alias': home.get('alias'),
        'home_team_sr_id': home.get('sr_id','not_present')
    }
    
    # Extract away team information
    away = json_data.get('away', {})
    away_data = {
        'away_team_id': away.get('id'),
        'away_team_name': away.get('name'),
        'away_team_market': away.get('market'),
        'away_team_alias': away.get('alias'),
        'away_team_sr_id': away.get('sr_id','not present')
    }
    
    # Extract time zone information
    time_zones = json_data.get('time_zones', {})
    time_zone_data = {
        'venue_time_zone': time_zones.get('venue'),
        'home_time_zone': time_zones.get('home'),
        'away_time_zone': time_zones.get('away')
    }
    
    # Combine all data
    all_data = {**game_data, **venue_data, **home_data, **away_data, **time_zone_data}
    
    # Create DataFrame
    df = pd.DataFrame([all_data])
    
    return df

def get_event_dataframe(game_id, league):
    try:
        # print(os.getenv("SPORTSRADAR_API_KEY"))
        # Example usage with your API call:
        url = f"https://api.sportradar.com/{league}/production/v8/en/games/{game_id}/summary.json"
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