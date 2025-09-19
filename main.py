import ujson

from  messaging.rabbitmq_messaging import rabbitmq_conn
from  basketball_prediction import prediction_handler
# Import all league-specific functions

def handler(event, context):
    try:
        print(f'Event received in handler:{event}')
        if "python_payload" not in event:
            raise ValueError("Missing 'python_payload' in event")

        payload = ujson.loads(ujson.dumps(event["python_payload"]))
        print('payload is ->')
        print(payload)
        required_fields = ['game_id', 'player_id', 'data_point', 'threshold', 'league']
        for field in required_fields:
            if field not in payload:
                raise ValueError(f"Missing required field '{field}' in payload")

        try:
            threshold = float(payload['threshold'])
        except (ValueError, TypeError):
            raise ValueError("Threshold must be a valid number (e.g., 3.5 or 1.5)")

        data_point = payload['data_point']
        league = payload['league'].lower()

        # attribute_list = ['qb_passing_yards', 'qb_rushing_yards', 'rb_rushing_yards', 'wr_receiving_yards'
        #                   , 'wr_receiving_touchdowns', 'wr_receptions', 'rb_rushing_plus_receiving_yards',
        #                   'rb_rushing_touchdowns', 'qb_passing_touchdowns']
        league_list = ['nba','ncaamb']
        if data_point not in attribute_list:
            raise ValueError(f"Unsupported attribute '{data_point}'. Supported attributes are: {attribute_list}")

        if league not in league_list:
            raise ValueError(f"Unsupported league '{league}' supported leagues are '{league_list}'.")

        event = prediction_handler(event, context)
        print(event)
        rabbitmq_conn(event)

    except Exception as e:
        event["result"] = "ERROR"
        event["result_data"] = []
        event["error_message"] = str(e)
        print(f"Error occurred in handler: {str(e)}")
        print(event)
        rabbitmq_conn(event)


# # # # # # Empty context (can mock AWS Lambda context if needed)
# event_for_qb = {
#     "python_payload": {
#         "game_id": "56779053-89da-4939-bc22-9669ae1fe05a", # 2025-09-05T00:20:00+00:00 - game_date_time
#         "player_id": "93147c90-09c8-471d-a6b2-0b9d19739ba1",
#         # "data_point": "qb_passing_yards",  # must match an item in `attribute_list`
#         # "data_point": "qb_rushing_yards",  # must match an item in `attribute_list`
#         "data_point": "qb_passing_touchdowns",  # must match an item in `attribute_list`
#         "threshold": 100,
#         "league": "nfl"       # must match an item in `league_list`
#     }
# }
# event_for_rb= {
#     "python_payload": {
#         "game_id": "56779053-89da-4939-bc22-9669ae1fe05a", # 2025-09-05T00:20:00+00:00 - game_date_time
#         "player_id": "9811b753-347c-467a-b3cb-85937e71e2b9",
#         # "data_point": "rb_rushing_yards",  # must match an item in `attribute_list`
#         # "data_point": "rb_rushing_touchdowns",  # must match an item in `attribute_list`
#         "data_point": "rb_rushing_plus_receiving_yards",  # must match an item in `attribute_list`
#         "threshold": 100,
#         "league": "nfl"       # must match an item in `league_list`
#     }
# }
# event_for_wr = {
#     "python_payload": {
#         "game_id": "56779053-89da-4939-bc22-9669ae1fe05a", # 2025-09-05T00:20:00+00:00 - game_date_time
#         "player_id": "d4a7917d-f327-431b-9b87-83af341c3e21",
#         "data_point": "wr_receiving_yards",  # must match an item in `attribute_list`
#         # "data_point": "wr_receiving_touchdowns",  # must match an item in `attribute_list`
#         # "data_point": "wr_receptions",  # must match an item in `attribute_list`
#         "threshold": 100,
#         "league": "nfl"       # must match an item in `league_list`
#     }
# }

# 56779053-89da-4939-bc22-9669ae1fe05a 9811b753-347c-467a-b3cb-85937e71e2b9 rb_rushing_plus_receiving_yards 113.5
# event_for_wr_ncaafb = {
#     "python_payload": {
#         "game_id": "56779053-89da-4939-bc22-9669ae1fe05a", 
#         "player_id": "d4a7917d-f327-431b-9b87-83af341c3e21", #wr
#         # "player_id": "9811b753-347c-467a-b3cb-85937e71e2b9", #demo rushing+receiving yards for testing why this playes rushing > rushing+receiving
#         # "player_id": "63748d48-4839-4814-94d0-af965d55e387", #qb
#         # "player_id": "4e410c90-b8a3-11ee-afed-87ba9f4d73a0", #rb
#         # "data_point": "rb_rushing_yards",  # must match an item in `attribute_list`
#         # "data_point": "rb_rushing_touchdowns",  # must match an item in `attribute_list`
#         # "data_point": "rb_rushing_plus_receiving_yards",  # must match an item in `attribute_list`
#         # "data_point": "qb_passing_yards",  # must match an item in `attribute_list`
#         # "data_point": "qb_passing_touchdowns",  # must match an item in `attribute_list`
#         # "data_point": "qb_rushing_yards",  # must match an item in `attribute_list`
#         "data_point": "wr_receiving_yards",  # must match an item in `attribute_list`
#         # "data_point": "wr_receiving_touchdowns",  # must match an item in `attribute_list`
#         # "data_point": "wr_receptions",  # must match an item in `attribute_list`
#         "threshold": 113.5,
#         "league": "nfl"       # must match an item in `league_list`
#     }
# }
# context = {}
# event = event_for_wr_ncaafb
# handler(event, context)
