import psycopg2
import os
# from dotenv import load_dotenv


csv_table_map = {
    os.path.join("/tmp", "player_stats_nba.csv"): "basketball_nba_player_stats",
    os.path.join("/tmp", "team_stats_nba.csv"): "basketball_nba_team_stats",
    os.path.join("/tmp", "player_stats_ncaamb.csv"): "basketball_ncaamb_player_stats",
    os.path.join("/tmp", "team_stats_ncaamb.csv"): "basketball_ncaamb_team_stats",
    
}

def load_csvs_to_postgres():
    # DB config from .env
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", "5432")

    # Connect to the database
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
    print("csv_table_map")
    # Load each CSV into its respective table
    for csv_file, table_name in csv_table_map.items():
        try:
            # Load into PostgreSQL
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