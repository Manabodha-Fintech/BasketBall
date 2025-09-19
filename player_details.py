import requests
import json
import os
import pandas as pd
from typing import Dict, Any, Optional

def get_player_data(player_id: str,league: str) -> Optional[Dict[str, Any]]:
    url = f"https://api.sportradar.com/{league}/production/v8/en/players/{player_id}/profile.json"

    headers = {
        "accept": "application/json",
        "x-api-key": os.getenv("SPORTSRADAR_API_KEY")
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def extract_player_info(player_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract player team details and player level information
    """
    if not player_data:
        return {}
    
    # Basic player information
    player_info = {
        'id': player_data.get('id'),
        'abbr_name': player_data.get('abbr_name'),
        'full_name': f"{player_data.get('first_name', '')} {player_data.get('last_name', '')}".strip(),
        'jersey_number': player_data.get('jersey'),
        'position': player_data.get('position'),
        'status': player_data.get('status'),
        'experience': player_data.get('experience'),
        'rookie_year': player_data.get('rookie_year'),
        'salary': player_data.get('salary'),
        'height': player_data.get('height'),
        'weight': player_data.get('weight'),
        'birth_date': player_data.get('birth_date'),
        'college': player_data.get('college')
    }
    
    # Current team information
    current_team = player_data.get('team', {})
    team_info = {
        'current_team_id': current_team.get('id'),
        'current_team_name': current_team.get('name'),
        'current_team_market': current_team.get('market'),
        'current_team_alias': current_team.get('alias')
    }
    
    # Draft information
    draft_info = player_data.get('draft', {})
    draft_data = {
        'draft_year': draft_info.get('year'),
        'draft_round': draft_info.get('round'),
        # 'draft_number': draft_info.get('number'),
        'draft_team': draft_info.get('team', {}).get('name') if draft_info.get('team') else None
    }
    
    # Combine all information into a flat dictionary for DataFrame
    combined_info = {**player_info, **team_info, **draft_data}
    
    return combined_info

def get_seasons_dataframe(player_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Create a DataFrame with season-by-season information
    """
    if not player_data:
        return pd.DataFrame()
    
    seasons_list = []
    for season in player_data.get('seasons', []):
        team_data = season.get('teams', [{}])[0] if season.get('teams') else {}
        statistics = team_data.get('total', {})
        
        season_info = {
            'player_id': player_data.get('id'),
            'season_year': season.get('year'),
            'season_type': season.get('type'),
            'team_id': team_data.get('id'),
            'team_name': team_data.get('name'),
            'team_market': team_data.get('market'),
            'team_alias': team_data.get('alias'),
            'games_played': statistics.get('games_played', 0),
            'games_started': statistics.get('games_started', 0)
        }
        
        # Add all available statistics
        for stat_key, stat_value in statistics.items():
            if stat_key not in ['games_played', 'games_started']:
                season_info[f'stat_{stat_key}'] = stat_value
        
        seasons_list.append(season_info)
    
    return pd.DataFrame(seasons_list)


def player_info_handler(player_id: str, league: str, return_type: str = 'basic') -> pd.DataFrame:
    """
    Main handler function to get player information as DataFrame(s)
    
    Parameters:
    -----------
    player_id : str
        The player ID to fetch data for
    return_type : str
        'basic' - returns basic player info DataFrame
        'seasons' - returns seasons DataFrame
        'both' - returns both DataFrames as a tuple
    
    Returns:
    --------
    DataFrame or tuple of DataFrames
    """
    player_data = get_player_data(player_id, league)    
    if not player_data:
        raise ValueError(f"Could not retrieve data for player ID: {player_id}")
    
    # Extract basic player info
    player_info = extract_player_info(player_data)
    basic_df = pd.DataFrame([player_info])

     # Extract seasons data
    # seasons_df = get_seasons_dataframe(player_data)
    seasons_df = pd.DataFrame([])

    if return_type == 'basic':
        return basic_df
    elif return_type == 'seasons':
        return seasons_df
    elif return_type == 'both':
        return basic_df, seasons_df
    else:
        raise ValueError("return_type must be 'basic', 'seasons', or 'both'")
    
