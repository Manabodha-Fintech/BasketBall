import os
from dotenv import load_dotenv  
load_dotenv()
from get_game_ids import get_closed_games_for_date
from get_game_details import process_game_ids
from player_stats import process_player_stats
from team_stats import process_team_stats
from append_data_to_rds import load_csvs_to_postgres

def main(league):
    print("fetching gameIds")
    fetch_game_ids = get_closed_games_for_date(league)
    if len(fetch_game_ids):
        print(f"Game IDs fetched {fetch_game_ids}")

        print("started fetching game summary")
        game_summary = process_game_ids(fetch_game_ids, league)
        # print(game_summary)

        print("Exporting player stats to CSV...")
        process_player_stats(game_summary, league)
        print("Player stats exported to CSV.")
        
        print("Exporting team stats to CSV...")
        process_team_stats(game_summary, league)
        print("Team stats exported to CSV.")
        
        print("Loading CSVs to PostgreSQL...")
        load_csvs_to_postgres(league)

    else :
        print("nothing to process")

def handler(event, context):
    # event = {
    #     "payload" : {
    #         "league" : "nba"
    #     }
    # }
    league = event.get("payload", {}).get("league")
    
    if not league:
        print("League not found in event payload")
        return
    # print(event)
    main(league)

# handler(1,2)