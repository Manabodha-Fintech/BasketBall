import os
from dotenv import load_dotenv  
load_dotenv()
from get_game_ids import get_closed_games_for_date
from get_game_details import process_game_ids
from player_stats import process_player_stats
from team_stats import process_team_stats
from append_data_to_rds import load_csvs_to_postgres

def main():
    print("fetching gameIds")
    nba_game_ids = get_closed_games_for_date()
    if len(nba_game_ids):
        print(f"Game IDs fetched {nba_game_ids}")

        print("started fetching game summary")
        game_summary = process_game_ids(nba_game_ids)
        # print(game_summary)

        print("Exporting player stats to CSV...")
        process_player_stats(game_summary)
        print("Player stats exported to CSV.")
        
        print("Exporting team stats to CSV...")
        process_team_stats(game_summary)
        print("Team stats exported to CSV.")
        
        print("Loading CSVs to PostgreSQL...")
        load_csvs_to_postgres()

    else :
        print("nothing to process")

def handler(event, context):
    main()

handler(1,2)