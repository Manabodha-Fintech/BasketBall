import pandas as pd
import ujson
import pickle
import boto3
import os
import numpy as np
from scipy.stats import norm


from player_details import player_info_handler

def prediction_handler(event, context):
    try:
        if "python_payload" not in event:
            raise ValueError("Missing python_payload in event")
        
        payload = ujson.loads(ujson.dumps(event["python_payload"]))
        attribute = payload['data_point']
        league = payload['league'].lower()
        threshold = payload['threshold']
        player_id = payload['player_id']
        game_id = payload['game_id']

        player_info = player_info_handler(player_id,league)

        print('curr_game_df from data from sportsradar api')
        curr_game_df = get_event_dataframe(game_id, league)

    except Exception as e:
        event["result"] = "ERROR"
        event["result_data"] = []
        event["error_message"] = str(e)
        print(f"Error occurred in handler: {str(e)}")
        return event