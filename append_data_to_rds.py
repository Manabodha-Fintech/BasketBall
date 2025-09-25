import psycopg2
import os

# Mapping of CSV files to tables
csv_table_map = {
    "nba": {
        os.path.join("/tmp", "player_stats_nba.csv"): "basketball_nba_player_stats",
        os.path.join("/tmp", "team_stats_nba.csv"): "basketball_nba_team_stats",
    },
    "ncaamb": {
        os.path.join("/tmp", "player_stats_ncaamb.csv"): "basketball_ncaamb_player_stats",
        os.path.join("/tmp", "team_stats_ncaamb.csv"): "basketball_ncaamb_team_stats",
    }
}

def load_csvs_to_postgres(league):
    # DB config from environment
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", "5432")

    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return

    cur = conn.cursor()

    # Get CSVs for the selected league
    league_csvs = csv_table_map.get(league.lower())
    if not league_csvs:
        print(f"No CSV files configured for league '{league}'")
        return

    # Load each CSV for this league
    for csv_file, table_name in league_csvs.items():
        try:
            with open(csv_file, 'r') as f:
                print(f"Loading {csv_file} into {table_name}...")
                cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", f)
            conn.commit()
            print(f"Successfully loaded {csv_file} into {table_name}")
        except Exception as e:
            conn.rollback()
            print(f"Error loading {csv_file} into {table_name}: {e}")

    # Clean up
    cur.close()
    conn.close()
