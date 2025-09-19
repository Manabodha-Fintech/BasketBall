import pandas as pd
import numpy as np
import os
import psycopg2
from psycopg2 import sql

import warnings
warnings.filterwarnings("ignore")
# warnings.simplefilter(action='ignore', category=FutureWarning)
# warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

from nba_columns_details import *
from ncaamb_columns_details import *
from columns_mapping import agg_matrics, drop_columns
# from dotenv import load_dotenv  
# load_dotenv()


# # Connect to the database
con = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT", 5432)
)
# Function to calculate aggregate features
def calculate_agg_features(df, feat_trans_dict, rolling_window, trans_level, min_games = 1):

    '''
    df will be the dataframe containing the raw data to be transformed

    feat_trans_dict is a dictionary that has column - type of transformation as a key value pair. ex. {'ERA' : pd.Series.mean}

    rolling window represents the window for which the aggregation to be done

    trans_level indicates if the pitcher metric aggregation to be done for a specific opponent or entire career
    '''  

    for level in trans_level:
        if level == 'opponent':
            grouped_cols = ['player_id', 'opponent_name']
        else:
            grouped_cols = ['player_id']
        sort_cols = grouped_cols + ['game_date']

        df = df.sort_values(by=sort_cols)
        # print(df.columns)

        for col, transform_type in feat_trans_dict.items():
            # print(col, transform_type)
            df[f'shifted_{col}'] = df.groupby(grouped_cols)[col].shift(1)
            if transform_type == 'sum':
                df[f'{col}_prev_{rolling_window}_games_{level}_sum'] = df.groupby(grouped_cols)[f'shifted_{col}'].transform(lambda x: x.rolling(window=rolling_window, min_periods=min_games).sum())
            elif transform_type == 'mean':
                df[f'{col}_prev_{rolling_window}_games_{level}_mean'] = df.groupby(grouped_cols)[f'shifted_{col}'].transform(lambda x: x.rolling(window=rolling_window, min_periods=min_games).mean())
            df.drop(columns=[ f'shifted_{col}'], inplace=True)
    return df

def calculate_team_agg_features(df, feat_trans_dict, rolling_window, trans_level, min_games = 1):

    '''
    df will be the dataframe containing the raw data to be transformed

    feat_trans_dict is a dictionary that has column - type of transformation as a key value pair. ex. {'ERA' : pd.Series.mean}

    rolling window represents the window for which the aggregation to be done

    trans_level indicates if the pitcher metric aggregation to be done for a specific opponent or entire career
    '''  

    for level in trans_level:
        if level == 'opponent':
            grouped_cols = ['team_id', 'opponent_id']
        else:
            grouped_cols = ['team_id']
        sort_cols = grouped_cols  + ['game_date']

        df = df.sort_values(by=sort_cols)
        # print(df.columns)

        for col, transform_type in feat_trans_dict.items():
            # print(col, transform_type)
            df[f'shifted_{col}'] = df.groupby(grouped_cols)[col].shift(1)
            if transform_type == 'sum':
                df[f'{col}_prev_{rolling_window}_games_{level}_sum'] = df.groupby(grouped_cols)[f'shifted_{col}'].transform(lambda x: x.rolling(window=rolling_window, min_periods=min_games).sum())
            elif transform_type == 'mean':
                df[f'{col}_prev_{rolling_window}_games_{level}_mean'] = df.groupby(grouped_cols)[f'shifted_{col}'].transform(lambda x: x.rolling(window=rolling_window, min_periods=min_games).mean())
            df.drop(columns=[ f'shifted_{col}'], inplace=True)
    return df

def encoding(df):
    # encoding the venue data
    # venue_roof_type
    roof_type = df['venue_roof_type'].unique()
    print(roof_type)

    df['venue_roof_type'] = df['venue_roof_type'].apply(
        lambda x: 0 if x == 'dome' else (1 if x == 'outdoor' else (2 if x == 'retractable_dome' else -1))
    )
    roof_type = df['venue_roof_type'].unique()
    print(roof_type)

    # venue_surface
    surface_type = df['venue_surface'].unique()
    print(surface_type)
    df['venue_surface'] = df['venue_surface'].apply(
        lambda x: 0 if x == 'artificial' else 1
    )
    surface_type = df['venue_surface'].unique()
    print(surface_type)
    
    # Convert the boolean column to integers (1 for True, 0 for False)
    for col in df.columns:
        if df[col].dtype == 'bool':
            df[col] = df[col].astype(int)
    return df
    
def get_player_data_from_rds(league, target_player_id, opponent_team, latest_game_df, attribute):
    table_name = sql.Identifier(f"basketball_{league.lower()}_player_stats")
    # table_column_list = f"{league}_player_stats_columns_from_database"
    # columns_sql = sql.SQL(', ').join(map(sql.Identifier, table_column_list))
    if not table_name:
        raise ValueError(f"Unsupported league: {league}")
    if league == 'nba':
        columns_sql = sql.SQL(', ').join(map(sql.Identifier, nba_player_stats_columns_from_database))
    if league == 'ncaamb':
        columns_sql = sql.SQL(', ').join(map(sql.Identifier, ncaamb_player_stats_columns_from_database))
    # if not table_name:
    #     raise ValueError(f"Unsupported league: {league}")
    with con:
        cur = con.cursor()
        # Fetch the latest 5 games for the target player
        sql_query_career = sql.SQL("""WITH ranked_data AS (
            SELECT *,
                row_number() over(partition by player_id order by game_date desc) career_rank
            FROM {table}
        )
        SELECT {columns} FROM ranked_data
        where player_id = %s
            and career_rank <= 7""").format(table=table_name, columns=columns_sql)
        cur.execute(sql_query_career, (target_player_id,))
        rows = cur.fetchall()
        # print(rows)     
    # Create the DataFrame
    # columns_from_database = f"{league}_player_stats_columns_from_database"
    columns = nba_player_stats_columns_from_database
    if league == 'ncaamb':
        columns = ncaamb_player_stats_columns_from_database
    df_career = pd.DataFrame(rows, columns=columns)
    # print('df_career.head()')
    # print(df_career.head())
    if df_career.empty:
        raise ValueError(f"No data found for player {target_player_id} against opponent {opponent_team} in league {league}")
    # df_career = append_current_game_df(df_career, latest_game_df,table_name,opponent_team)
    # df_career = pd.concat([df_career,latest_game_df])
    # df['const']=1
    print(f"printing df_career-{df_career}") 
    df_career = encoding(df_career)
    if attribute == 'rb_rushing_plus_receiving_yards':
        df_career['rushing_yards'] = df_career['rushing_yards'].fillna(0)
        df_career['receiving_yards'] = df_career['receiving_yards'].fillna(0)
        df_career['player_rushing_plus_receiving_yards'] = df_career['rushing_yards'] + df_career['receiving_yards']

    return df_career

def get_team_data_from_rds(league, target_player_id, opponent_team, latest_game_df):
    table_name = sql.Identifier(f"basketball_{league.lower()}_team_stats")
    if not table_name:
        raise ValueError(f"Unsupported league: {league}")
    if league == 'nba':
        columns_sql = sql.SQL(', ').join(map(sql.Identifier, nba_team_stats_columns_from_database))
    if league == 'ncaamb':
        columns_sql = sql.SQL(', ').join(map(sql.Identifier, ncaamb_team_stats_columns_from_database))

    # if not table_name:
    #     raise ValueError(f"Unsupported league: {league}")
    with con:
        cur = con.cursor()
        # Fetch the latest 5 games for the target player
        sql_query_career = sql.SQL("""WITH ranked_data AS (
            SELECT *,
                row_number() over(partition by team_name order by game_date desc) career_rank
            FROM {table}
        )
        SELECT {columns} FROM ranked_data
        where team_name = %s
            and career_rank <= 7""").format(table=table_name, columns=columns_sql)
        cur.execute(sql_query_career, (opponent_team,))
        rows = cur.fetchall()
        # print(rows)     
    # Create the DataFrame
    # columns_from_database = f"{league}_team_stats_columns_from_database"
    columns = nba_team_stats_columns_from_database
    if league == 'ncaamb':
        columns = ncaamb_team_stats_columns_from_database
    df_career = pd.DataFrame(rows, columns=columns)
    df_team = pd.DataFrame(rows, columns=columns)
    # print('df_career.head()')
    # print(df_career.head())
    if df_team.empty:
        raise ValueError(f"No data found for player {target_player_id} against opponent {opponent_team} in league {league}")
    # df_career = append_current_game_df(df_career, latest_game_df,table_name,opponent_team)
    # df_career = pd.concat([df_career,latest_game_df])
    # df['const']=1
    print(f"printing df_team-{df_team}") 
    # df_team = encoding(df_team)
    return df_team
    
# path = 'player_stats_spain_laliga_with_opponent.csv'
# df = pd.read_csv(path)


def preprocessing_and_feature_engineering(league, target_player_id, opponent_team, latest_game_df,player_info, attribute):

    df_career = get_player_data_from_rds(league, target_player_id, opponent_team, latest_game_df,attribute=attribute)
    df_team = get_team_data_from_rds(league, target_player_id, opponent_team, latest_game_df)
    print(df_career)
    for column in df_career.columns:
        if column not in latest_game_df.columns:
            latest_game_df[column] = np.nan
    latest_game_df = latest_game_df[df_career.columns]
    latest_game_df['player_id'] = target_player_id
    df_career = pd.concat([df_career, latest_game_df], ignore_index=True)
    
    print('df_career')
    print(df_career.shape, df_career.columns.to_list())

    df_team_last_row = df_team.tail(1).reset_index(drop=True)
    df_team = pd.concat([df_team, df_team_last_row], ignore_index=True) # to make an extra row that will store the aggregated values
    
    print('df_team')
    print(df_team.shape, df_team.columns.to_list())
   
    aggregation_metrics = agg_matrics[league][attribute]
    # team_aggregation_metrics = f'{league}_team_aggregation_metrics'
    team_aggregation_metrics = nba_team_aggregation_metrics if league == 'nba' else ncaamb_team_aggregation_metrics

    df_career_transformed = calculate_agg_features(df_career.copy(), aggregation_metrics, rolling_window=7, min_games=1, trans_level=['career'])
    df_team_transformed = calculate_team_agg_features(df_team.copy(), team_aggregation_metrics, rolling_window=7, min_games=1, trans_level=['career'])
 
 
    print('after aggregation')
    print('after df_career_transformed')
    print(df_career_transformed.shape, df_career_transformed.columns.to_list())
    print('after df_team_transformed')
    print(df_team_transformed.shape, df_team_transformed.columns.to_list())

    df_combined = pd.merge(df_career_transformed, df_team_transformed, left_on = ['opponent_name'], right_on = ['team_name'])
    unmatched = set(df_career_transformed['opponent_name']) - set(df_team_transformed['team_name'])
    print(set(df_career_transformed['opponent_name']))
    print(set(df_team_transformed['team_name']))
    print("Unmatched opponent names:", unmatched)
    df_combined = df_combined.drop(columns=['game_id_y'])
    df_combined = df_combined.rename(columns={'game_id_x': 'game_id'})

    print("df_combined after merge")
    print(df_combined.shape, df_combined.columns.to_list())
    
    cols_to_drop = drop_columns[league][attribute]
    
    df_combined.drop(columns=cols_to_drop, inplace= True)
    # df_transformed.drop(columns=attribute, inplace=  True)
    final_training_df = df_combined.copy()
    final_training_df = encoding(final_training_df)
    print(final_training_df.columns.to_list)
    # final_training_df = final_training_df[~final_training_df['assists_prev_10_games_opponent_mean'].isnull()]
    # final_training_df.columns =  [col.lower().replace(" ", "_").replace(",", "") for col in final_training_df.columns]
    print('final_training_df')
    print(final_training_df.shape, final_training_df.columns.to_list())
    
    X = final_training_df.copy()
    for column in X.columns:
        # Check if the column is of boolean type
        if X[column].dtype == 'bool':
            # Convert the boolean column to integers (1 for True, 0 for False)
            X[column] = X[column].astype(int)
    print('final_training_df')
    # print(final_training_df)
    # print(X)
    data = X.tail(1)
    # adding player position as a columns
    # if player_info['position'].iloc[0] in ['WR','TE']:
    #     data['team_position_wr'] = 1 if player_info['position'].iloc[0] == 'WR' else 0 
    #     data['team_position_te'] = 1 if player_info['position'].iloc[0] == 'TE' else 0
    print(data)
    # data.to_csv('final_input.csv')
    return data
# ans = preprocessing_and_feature_engineering(df, 'shots_on_target')