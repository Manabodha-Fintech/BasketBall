import json
import csv
import sys
import os
from pathlib import Path
import pandas as pd
from column_details import *

team_stats = []

def create_team_stats_csv(game_data):
    try:
        # print(data)
        rows = []
        if game_data["status"] != "closed":
            return []
        
        for side in ["home", "away"]:
            team = game_data.get(side, {})
            if not team:
                continue

            row = {
                # game details
                "game_id": game_data.get("id"),
                "game_sr_id": game_data.get("sr_id"),
                "scheduled": game_data.get("scheduled"),
                "duration": game_data.get("duration"),
                "game_date":game_data.get("scheduled").split('T')[0],
                "status": game_data.get("status"),
                "attendance":game_data.get("attendance"),
                "track_on_court":game_data.get("track_on_court"),
                # team details
                "team_id": team.get("id"),
                "team_sr_id": team.get("sr_id"),
                "team_name": team.get("name"),
                "team_alias": team.get("alias"),
                "team_market": team.get("market"),
                "points": team.get("points"),
                "bonus": team.get("bonus"),
                "timeouts_remaining": team.get("remaining_timeouts"),
                # team records
                # "record_wins":team.get("record").get("wins"),
                # "record_losses":team.get("record").get("losses"),
                
            }

            record = team.get("record", {})
            row.update({
                     "record_wins":record.get("wins"),
                     "record_losses":record.get("losses")
                })
            # venue details
            venue = game_data.get("venue", {})
            row.update({
                "venue_id": venue.get("id"),
                "venue_name": venue.get("name"),
                "venue_capacity": venue.get("capacity"),
                "venue_address": venue.get("address"),
                "venue_city": venue.get("city"),
                "venue_state": venue.get("state"),
                "venue_zip": venue.get("zip"),
                "venue_country": venue.get("country"),
                "venue_sr_id": venue.get("sr_id"),
            })

            # location details (if present inside venue)
            location = venue.get("location", {})
            row.update({
                "venue_lat": location.get("lat"),
                "venue_lon": location.get("lng"),
            })
            
            # team scoring
            scoring = team.get("scoring", [])
            for i, s in enumerate(scoring):
                row[f"scoring_{i}_points"] = s.get("points")
                row[f"scoring_{i}_type"] = s.get("type")
                row[f"scoring_{i}_number"] = s.get("number")
                row[f"scoring_{i}_sequence"] = s.get("sequence")

            # team statistics
            stats_data = team.get("statistics", [])
            stats_dict = {}
            if stats_data:
                # usually list with one dict inside
                for k, v in stats_data.items():
                        row[k] = v

                # team most_unanswered
                most_unanswered = stats_data.get("most_unanswered", {})
                if most_unanswered:
                    for k, v in most_unanswered.items():
                        row[f"most_unanswered_{k}"] = v

                # team periodic statistics
                periods = stats_data.get("periods", [])
                for p in periods:
                        period_no = p.get("number")
                        suffix = f"{period_no}th_period"
                        for stat_name, value in p.items():
                            if stat_name != "number":
                                row[f"{suffix}_{stat_name}"] = value
            
            rows.append(row)
                
        return rows
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
        return []

def process_team_stats(game_summary):
    for game in game_summary:
        stats = create_team_stats_csv(game)
        team_stats.extend(stats)
    
    df = pd.DataFrame(team_stats)
    df = df[required_column_order_for_nba_team_stats]
    # Save DataFrame to CSV
    output_file = "/tmp/team_stats.csv"   # you can give any path here
    df.to_csv(output_file, index=False)
    

    print(f"✅ team stats saved to {output_file}")