import pandas as pd
import ujson
import pickle
import boto3
import os
import numpy as np
from scipy.stats import norm

# from dotenv import load_dotenv
# load_dotenv()

from preprocessing import preprocessing_and_feature_engineering
from ingame_details import get_event_dataframe
from player_details import player_info_handler
from columns_mapping import columns_required_for_model

s3 = boto3.client('s3')
MODEL_BUCKET = os.getenv('MODEL_BUCKET')

def load_model_from_s3(league: str, attribute: str):
    """Get the corresponding environment variable for a league-attribute combination."""
    league = league.lower()
    attribute = attribute.lower()
    
    # try:
    #     env_var_name = model_key_map[league][attribute]
    # except KeyError:
    #     raise ValueError(f"No environment variable mapping found for league '{league}' and attribute '{attribute}'")
    
    # key_value = os.getenv(env_var_name)
    key_value = os.getenv(f'{league}_{attribute}_model_key')
    if key_value is None:
        # raise ValueError(f"Environment variable {env_var_name} is not set")
        raise ValueError(f"No model file found for league '{league}' and attribute '{attribute}'")
    
    try:
        response = s3.get_object(Bucket=MODEL_BUCKET, Key=key_value)
        return pickle.loads(response['Body'].read())
    except s3.exceptions.NoSuchKey:
        raise FileNotFoundError(f"Model file not found at key: {key_value}")
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")
    

def predict(league,model,attribute, y_test ,threshold):
    model_features  = columns_required_for_model[league][attribute]
    print('Missing cols are ->')
    missing_cols = set(model_features) - set(y_test.columns)
    print(missing_cols)
    extra_cols = set(y_test.columns) -set(model_features)
    print(extra_cols)
    for col in missing_cols:
        y_test[col] = 0
    y_test = y_test[model_features]
    print('model input as y_test is ->')
    print(y_test)
    # y_test['receiving_air_yards_prev_7_games_career_sum']=0
    # y_test.to_csv('model_input_for_rushing_receiving.csv',index=False)
    # y_test.to_csv('model_input_for_rushing.csv',index=False)
    if isinstance(y_test, pd.DataFrame) or isinstance(y_test, pd.Series):
        y_test = y_test.values.reshape(1, -1)
    else:
        y_test = y_test.reshape(1, -1)
    prediction = model.predict(y_test)
    preds_list = [tree.predict(y_test)[0] for tree in model.estimators_]
    # preds_array = np.array([tree.predict(y_test)[0] for tree in model.estimators_])
    # print(f"pred_list {preds_list}")
    preds_list = [l.item() for l in preds_list]
    # print(f"pred_list {preds_list}")
    mean_pred = np.mean(preds_list)
    std_dev_pred = np.std(preds_list)
    mean_pred = mean_pred.item()
    std_dev_pred = std_dev_pred.item()
    print(mean_pred,type(mean_pred),std_dev_pred,type(std_dev_pred),prediction,type(prediction))
    # Create the fitted normal distribution
    # fitted_normal_dist = norm(loc=mean_pred, scale=std_dev_pred)
    if std_dev_pred == 0:
        prob_over_threshold = 1.0 if prediction > threshold else 0.0
        prob_under_threshold = 1.0 - prob_over_threshold
    else:
        # Create the fitted normal distribution
        fitted_normal_dist = norm(loc=mean_pred, scale=std_dev_pred)
        print('normal_distribution fitted !')

        # Calculate probability over the threshold (Survival Function)
        prob_over_threshold = fitted_normal_dist.sf(threshold)

        # Calculate probability under the threshold (Cumulative Distribution Function)
        prob_under_threshold = fitted_normal_dist.cdf(threshold)

    # print(f"Overall Prediction: {strikeout_prediction:.4f}")
    # print(f"Parametric P(X > {threshold}) (Over Probability): {prob_over_threshold:.4f}")
    # print(f"Parametric P(X <= {threshold}) (Under Probability): {prob_under_threshold:.4f}")

    return {
        'overall_prediction': prediction[0],
        'prob_over_threshold': prob_over_threshold,
        'prob_under_threshold': prob_under_threshold
    }

def prediction_handler(event, context):
    try:
        if "python_payload" not in event:
            raise ValueError("Missing 'python_payload' in event")

        payload = ujson.loads(ujson.dumps(event["python_payload"]))
        attribute = payload['data_point']
        league = payload['league'].lower()
        threshold = payload['threshold']
        player_id = payload['player_id']
        game_id = payload['game_id']

        #dataFrame for player info
        player_info = player_info_handler(player_id,league)
        # For checking if the player belong to same position as the attribute in the request for prediction
        # player_position = player_info['position'].iloc[0]
        # if player_position.capitalize() != attribute.split('_')[0].capitalize():
        #     raise ValueError(f"request for {attribute} but this player primary position is {player_position}")
        
        print('curr_game_df from data from sportsradar api')
        curr_game_df = get_event_dataframe(game_id, league)
        print(curr_game_df)

        player_belongs_to_team = [player_info['current_team_name'].iloc[0]]
        # Extract home and away teams from the DataFrame
        # Determine which of home/away is NOT one of the player's teams or just determine which is players opponent team.
        home_team = curr_game_df['home_team_name'].iloc[0]
        away_team = curr_game_df['away_team_name'].iloc[0]
        if home_team in player_belongs_to_team and away_team not in player_belongs_to_team:
            opponent_team = away_team
            player_team = home_team
        elif away_team in player_belongs_to_team and home_team not in player_belongs_to_team:
            opponent_team = home_team
            player_team = away_team
        else:
            # Handle cases where:
            # - Player is on both teams (shouldn't happen)
            # - Player is on neither team (data inconsistency)
            raise ValueError(f"Cannot determine opponent team. Player teams: {player_belongs_to_team}, Game teams: {home_team} vs {away_team}")

        print(f"Player team is {player_team}, opponent team is {opponent_team}")
        curr_game_df['opponent_name'] = opponent_team
        curr_game_df = curr_game_df[['venue_roof_type', 'venue_surface', 'venue_capacity','opponent_name']]
        processed_df = preprocessing_and_feature_engineering(league, player_id, opponent_team, curr_game_df,player_info, attribute)
        print('processed_df is prepared ->')
        print(processed_df)
        # processed_df.to_csv('processedd_df.csv')
        print('Loading model ...')
        model = load_model_from_s3(league,attribute)
        print('Model Loaded ! Below is the Model details')
        print(model)
        prediction = predict(league,model=model, attribute=attribute, y_test=processed_df ,threshold=threshold)

        event["result"] = "RESULT"
        event["result_data"] = {f'predicted_{league}_{attribute}': prediction['overall_prediction'],
                'threshold': threshold,
                'over_probability': prediction['prob_over_threshold'],
                'under_probability': prediction['prob_under_threshold']}
        print(event)
        print("Script executed successfully")
        return event

    except Exception as e:
        event["result"] = "ERROR"
        event["result_data"] = []
        event["error_message"] = str(e)
        print(f"Error occurred in handler: {str(e)}")
        return event
