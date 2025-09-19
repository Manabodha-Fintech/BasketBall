# from columns_details import qb_rushing_yards_combined_cols_to_drop, qb_passing_yards_combined_cols_to_drop
# from columns_details import rb_rushing_yards_combined_cols_to_drop, wr_te_receiving_yards_combined_cols_to_drop
# from columns_details import qb_passing_yards_aggregation_metrics, qb_rushing_yards_aggregation_metrics
# from columns_details import rb_rushing_yards_aggregation_metrics, wr_te_receiving_yards_aggregation_matrics

# from columns_details import  columns_required_for_qb_passing_yards, columns_required_for_qb_rushing_yards, columns_required_for_wr_te_receiving_yards, columns_required_for_rb_rushing_yards
from nba_columns_details import *
from ncaamb_columns_details import *

agg_matrics = {
    'nba':{
        'qb_rushing_yards':nba_qb_rushing_yards_aggregation_metrics,
        'qb_passing_yards':nba_qb_passing_yards_aggregation_metrics,
        'qb_passing_touchdowns':nba_qb_passing_touchdowns_aggregation_metrics,
        'rb_rushing_yards':nba_rb_rushing_yards_aggregation_metrics,
        'rb_rushing_plus_receiving_yards':nba_rb_rushing_plus_receiving_yards_aggregation_matrics,
        'rb_rushing_touchdowns':nba_rb_rushing_touchdowns_aggregation_metrics,
        'wr_receiving_yards':nba_wr_receiving_yards_aggregation_matrics,
        'wr_receiving_touchdowns':nba_wr_receiving_touchdowns_aggregation_metrics,
        'wr_receptions':nba_wr_receptions_aggregation_metrics,
    },
    'ncaamb':{
        'qb_rushing_yards':ncaamb_qb_rushing_yards_aggregation_metrics,
        'qb_passing_yards':ncaamb_qb_passing_yards_aggregation_metrics,
        'qb_passing_touchdowns':ncaamb_qb_passing_touchdowns_aggregation_metrics,
        'rb_rushing_yards':ncaamb_rb_rushing_yards_aggregation_metrics,
        'rb_rushing_plus_receiving_yards':ncaamb_rb_rushing_plus_receiving_yards_aggregation_matrics,
        'rb_rushing_touchdowns':ncaamb_rb_rushing_touchdowns_aggregation_metrics,
        'wr_receiving_yards':ncaamb_wr_receiving_yards_aggregation_matrics,
        'wr_receiving_touchdowns':ncaamb_wr_receiving_touchdowns_aggregation_metrics,
        'wr_receptions':ncaamb_wr_receptions_aggregation_metrics,
    }
}

drop_columns = {
    'nba':{
        'qb_rushing_yards':nba_qb_rushing_yards_combined_cols_to_drop,
        'qb_passing_yards':nba_qb_passing_yards_combined_cols_to_drop,
        'qb_passing_touchdowns':nba_qb_passing_touchdowns_combined_cols_to_drop,
        'rb_rushing_yards':nba_rb_rushing_yards_combined_cols_to_drop,
        'rb_rushing_plus_receiving_yards':nba_rb_rushing_plus_receiving_yards_combined_cols_to_drop,
        'rb_rushing_touchdowns':nba_rb_rushing_touchdowns_combined_cols_to_drop,
        'wr_receiving_yards':nba_wr_receiving_yards_combined_cols_to_drop,
        'wr_receiving_touchdowns':nba_wr_receiving_touchdowns_combined_cols_to_drop,
        'wr_receptions':nba_wr_receptions_combined_cols_to_drop,
    },
    'ncaamb':{
        'qb_rushing_yards':ncaamb_qb_rushing_yards_combined_cols_to_drop,
        'qb_passing_yards':ncaamb_qb_passing_yards_combined_cols_to_drop,
        'qb_passing_touchdowns':ncaamb_qb_passing_touchdowns_combined_cols_to_drop,
        'rb_rushing_yards':ncaamb_rb_rushing_yards_combined_cols_to_drop,
        'rb_rushing_plus_receiving_yards':ncaamb_rb_rushing_plus_receiving_yards_combined_cols_to_drop,
        'rb_rushing_touchdowns':ncaamb_rb_rushing_touchdowns_combined_cols_to_drop,
        'wr_receiving_yards':ncaamb_wr_receiving_yards_combined_cols_to_drop,
        'wr_receiving_touchdowns':ncaamb_wr_receiving_touchdowns_combined_cols_to_drop,
        'wr_receptions':ncaamb_wr_receptions_combined_cols_to_drop,
    }
    
}

columns_required_for_model = {
    'nba':{
        'qb_rushing_yards':nba_columns_required_for_qb_rushing_yards,
        'qb_passing_yards':nba_columns_required_for_qb_passing_yards,
        'qb_passing_touchdowns':nba_columns_required_for_qb_passing_touchdowns,
        'rb_rushing_yards':nba_columns_required_for_rb_rushing_yards,
        'rb_rushing_plus_receiving_yards':nba_coulumn_required_for_rb_rushing_plus_receiving_yards,
        'rb_rushing_touchdowns':nba_columns_required_for_rb_rushing_touchdowns,
        'wr_receiving_yards':nba_columns_required_for_wr_receiving_yards,
        'wr_receiving_touchdowns':nba_columns_required_for_wr_receiving_touchdowns,
        'wr_receptions':nba_columns_required_for_wr_receptions,
    },
    'ncaamb':{
        'qb_rushing_yards':ncaamb_columns_required_for_qb_rushing_yards,
        'qb_passing_yards':ncaamb_columns_required_for_qb_passing_yards,
        'qb_passing_touchdowns':ncaamb_columns_required_for_qb_passing_touchdowns,
        'rb_rushing_yards':ncaamb_columns_required_for_rb_rushing_yards,
        'rb_rushing_plus_receiving_yards':ncaamb_player_stats_columns_from_databasencaamb_coulumn_required_for_rb_rushing_plus_receiving_yards,
        'rb_rushing_touchdowns':ncaamb_columns_required_for_rb_rushing_touchdowns,
        'wr_receiving_yards':ncaamb_columns_required_for_wr_receiving_yards,
        'wr_receiving_touchdowns':ncaamb_columns_required_for_wr_receiving_touchdowns,
        'wr_receptions':ncaamb_columns_required_for_wr_receptions,
    }
}

