

import os
import pandas as pd
import sqlite3

def create_tables(conn):
    # TODO: Define primary and foreign keys for each table
    """Define table schemas with primary keys and foreign keys."""
    cursor = conn.cursor()

    # run create.sql
    with open('Database/create.sql', 'r') as f:
        create_sql = f.read()
        cursor.executescript(create_sql)

    """ 
    for reference, here is the content of create.sql:
    
    DROP TABLE IF EXISTS "awards_players";
    DROP TABLE IF EXISTS "coaches";
    DROP TABLE IF EXISTS "players";
    DROP TABLE IF EXISTS "players_teams";
    DROP TABLE IF EXISTS "series_post";
    DROP TABLE IF EXISTS "teams";
    DROP TABLE IF EXISTS "teams_post";

    -- Table: awards_players
    CREATE TABLE "awards_players" (
                "playerID" TEXT,
                "award" TEXT,
                "year" INTEGER,
                "lgID" TEXT,
                PRIMARY KEY ("award", "year", "playerID"),
                FOREIGN KEY ("playerID") REFERENCES "players" ("bioID")
            );

    -- Table: coaches
    CREATE TABLE "coaches" (
            "coachID" TEXT,
            "year" INTEGER,
            "tmID" TEXT,
            "lgID" TEXT,
            "stint" INTEGER,
            "won" INTEGER,
            "lost" INTEGER,
            "post_wins" INTEGER,
            "post_losses" INTEGER,
            PRIMARY KEY ("coachID", "stint", "year", "tmID"),
            FOREIGN KEY ("tmID", "year") REFERENCES "teams" ("tmID", "year")
            );

    -- Table: players
    CREATE TABLE "players" (
            "bioID" TEXT PRIMARY KEY,
            "pos" TEXT,
            "firstseason" INTEGER,
            "lastseason" INTEGER,
            "height" REAL,
            "weight" INTEGER,
            "college" TEXT,
            "collegeOther" TEXT,
            "birthDate" TEXT,
            "deathDate" TEXT
            );

    -- Table: players_teams
    CREATE TABLE "players_teams" (
            "playerID" TEXT,
            "year" INTEGER,
            "stint" INTEGER,
            "tmID" TEXT,
            "lgID" TEXT,
            "GP" INTEGER,
            "GS" INTEGER,
            "minutes" INTEGER,
            "points" INTEGER,
            "oRebounds" INTEGER,
            "dRebounds" INTEGER,
            "rebounds" INTEGER,
            "assists" INTEGER,
            "steals" INTEGER,
            "blocks" INTEGER,
            "turnovers" INTEGER,
            "PF" INTEGER,
            "fgAttempted" INTEGER,
            "fgMade" INTEGER,
            "ftAttempted" INTEGER,
            "ftMade" INTEGER,
            "threeAttempted" INTEGER,
            "threeMade" INTEGER,
            "dq" INTEGER,
            "PostGP" INTEGER,
            "PostGS" INTEGER,
            "PostMinutes" INTEGER,
            "PostPoints" INTEGER,
            "PostoRebounds" INTEGER,
            "PostdRebounds" INTEGER,
            "PostRebounds" INTEGER,
            "PostAssists" INTEGER,
            "PostSteals" INTEGER,
            "PostBlocks" INTEGER,
            "PostTurnovers" INTEGER,
            "PostPF" INTEGER,
            "PostfgAttempted" INTEGER,
            "PostfgMade" INTEGER,
            "PostftAttempted" INTEGER,
            "PostftMade" INTEGER,
            "PostthreeAttempted" INTEGER,
            "PostthreeMade" INTEGER,
            "PostDQ" INTEGER,
            PRIMARY KEY ("playerID","year","tmID"),
            FOREIGN KEY ("playerID") REFERENCES "players" ("bioID"),
            FOREIGN KEY ("tmID", "year") REFERENCES "teams" ("tmID", "year")
            );

    -- Table: series_post
    CREATE TABLE "series_post" (
            "year" INTEGER,
            "round" TEXT,
            "series" TEXT,
            "tmIDWinner" TEXT,
            "lgIDWinner" TEXT,
            "tmIDLoser" TEXT,
            "lgIDLoser" TEXT,
            "W" INTEGER,
            "L" INTEGER,
            PRIMARY KEY ("year", "tmIDWinner", "tmIDLoser"),
            FOREIGN KEY ("tmIDWinner", "year") REFERENCES "teams" ("tmID", "year"),
            FOREIGN KEY ("tmIDLoser", "year") REFERENCES "teams" ("tmID", "year")
            );

    -- Table: teams
    CREATE TABLE "teams" (
            "year" INTEGER,
            "lgID" TEXT,
            "tmID" TEXT,
            "franchID" TEXT,
            "confID" TEXT,
            "divID" REAL,
            "rank" INTEGER,
            "playoff" TEXT,
            "seeded" INTEGER,
            "firstRound" TEXT,
            "semis" TEXT,
            "finals" TEXT,
            "name" TEXT,
            "o_fgm" INTEGER,
            "o_fga" INTEGER,
            "o_ftm" INTEGER,
            "o_fta" INTEGER,
            "o_3pm" INTEGER,
            "o_3pa" INTEGER,
            "o_oreb" INTEGER,
            "o_dreb" INTEGER,
            "o_reb" INTEGER,
            "o_asts" INTEGER,
            "o_pf" INTEGER,
            "o_stl" INTEGER,
            "o_to" INTEGER,
            "o_blk" INTEGER,
            "o_pts" INTEGER,
            "d_fgm" INTEGER,
            "d_fga" INTEGER,
            "d_ftm" INTEGER,
            "d_fta" INTEGER,
            "d_3pm" INTEGER,
            "d_3pa" INTEGER,
            "d_oreb" INTEGER,
            "d_dreb" INTEGER,
            "d_reb" INTEGER,
            "d_asts" INTEGER,
            "d_pf" INTEGER,
            "d_stl" INTEGER,
            "d_to" INTEGER,
            "d_blk" INTEGER,
            "d_pts" INTEGER,
            "tmORB" INTEGER,
            "tmDRB" INTEGER,
            "tmTRB" INTEGER,
            "opptmORB" INTEGER,
            "opptmDRB" INTEGER,
            "opptmTRB" INTEGER,
            "won" INTEGER,
            "lost" INTEGER,
            "GP" INTEGER,
            "homeW" INTEGER,
            "homeL" INTEGER,
            "awayW" INTEGER,
            "awayL" INTEGER,
            "confW" INTEGER,
            "confL" INTEGER,
            "min" INTEGER,
            "attend" INTEGER,
            "arena" TEXT,
            PRIMARY KEY ("year", "tmID")
            );

    -- Table: teams_post
    CREATE TABLE "teams_post" (
            "year" INTEGER,
            "tmID" TEXT,
            "lgID" TEXT,
            "W" INTEGER,
            "L" INTEGER,
            PRIMARY KEY ("year", "tmID"),
            FOREIGN KEY ("tmID", "year") REFERENCES "teams" ("tmID", "year")
            );

    """

    conn.commit()

def csv_to_sqlite(csv_dir, conn):
    # Loop over all CSV files in the given directory
    for file_name in os.listdir(csv_dir):
        if file_name.endswith('.csv'):
            # Load CSV into pandas DataFrame
            csv_file_path = os.path.join(csv_dir, file_name)
            df = pd.read_csv(csv_file_path)
            
            # Create table name from file name (without .csv extension)
            table_name = os.path.splitext(file_name)[0]
            
            # Write DataFrame to SQL database (replace if table already exists)
            df.to_sql(table_name, conn, if_exists='append', index=False)
            print(f'Table "{table_name}" created in database.')

def get_schema(conn):
    # Query the sqlite_master table to get the SQL for creating each table
    cursor = conn.cursor()
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    
    schema_sql = ""
    for table_name, create_sql in cursor.fetchall():
        schema_sql += f'-- Table: {table_name}\n{create_sql};\n\n'
    
    return schema_sql

def join_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            -- Series Post columns
            sp.year AS year,
            sp.round AS round,
            sp.series AS series,
            sp.tmIDWinner AS winner_team_id,
            sp.tmIDLoser AS loser_team_id,
            sp.W AS winner_team_wins,
            sp.L AS loser_team_losses,
            
            -- Winning team columns
            tw.year AS winner_team_year,
            tw.lgID AS winner_team_league,
            tw.tmID AS winner_team_id,
            tw.franchID AS winner_team_franchise,
            tw.confID AS winner_team_conference,
            tw.divID AS winner_team_division,
            tw.rank AS winner_team_rank,
            tw.playoff AS winner_team_playoff,
            tw.seeded AS winner_team_seeded,
            tw.firstRound AS winner_team_first_round,
            tw.semis AS winner_team_semis,
            tw.finals AS winner_team_finals,
            tw.name AS winner_team_name,
            tw.o_fgm AS winner_team_off_fg_made,
            tw.o_fga AS winner_team_off_fg_attempted,
            tw.o_ftm AS winner_team_off_ft_made,
            tw.o_fta AS winner_team_off_ft_attempted,
            tw.o_3pm AS winner_team_off_3pt_made,
            tw.o_3pa AS winner_team_off_3pt_attempted,
            tw.o_oreb AS winner_team_off_orebounds,
            tw.o_dreb AS winner_team_off_drebounds,
            tw.o_reb AS winner_team_off_rebounds,
            tw.o_asts AS winner_team_off_assists,
            tw.o_pf AS winner_team_off_pf,
            tw.o_stl AS winner_team_off_steals,
            tw.o_to AS winner_team_off_turnovers,
            tw.o_blk AS winner_team_off_blocks,
            tw.o_pts AS winner_team_off_points,
            tw.d_fgm AS winner_team_def_fg_made,
            tw.d_fga AS winner_team_def_fg_attempted,
            tw.d_ftm AS winner_team_def_ft_made,
            tw.d_fta AS winner_team_def_ft_attempted,
            tw.d_3pm AS winner_team_def_3pt_made,
            tw.d_3pa AS winner_team_def_3pt_attempted,
            tw.d_oreb AS winner_team_def_orebounds,
            tw.d_dreb AS winner_team_def_drebounds,
            tw.d_reb AS winner_team_def_rebounds,
            tw.d_asts AS winner_team_def_assists,
            tw.d_pf AS winner_team_def_pf,
            tw.d_stl AS winner_team_def_steals,
            tw.d_to AS winner_team_def_turnovers,
            tw.d_blk AS winner_team_def_blocks,
            tw.d_pts AS winner_team_def_points,
            tw.tmORB AS winner_team_orb,
            tw.tmDRB AS winner_team_drb,
            tw.tmTRB AS winner_team_trb,
            tw.opptmORB AS winner_team_opp_orb,
            tw.opptmDRB AS winner_team_opp_drb,
            tw.opptmTRB AS winner_team_opp_trb,
            tw.won AS winner_team_wins,
            tw.lost AS winner_team_losses,
            tw.GP AS winner_team_games_played,
            tw.homeW AS winner_team_home_wins,
            tw.homeL AS winner_team_home_losses,
            tw.awayW AS winner_team_away_wins,
            tw.awayL AS winner_team_away_losses,
            tw.confW AS winner_team_conf_wins,
            tw.confL AS winner_team_conf_losses,
            tw.min AS winner_team_minutes,
            tw.attend AS winner_team_attendance,
            tw.arena AS winner_team_arena,

            -- Losing team columns (same structure as winning team)
            tl.year AS loser_team_year,
            tl.lgID AS loser_team_league,
            tl.tmID AS loser_team_id,
            tl.franchID AS loser_team_franchise,
            tl.confID AS loser_team_conference,
            tl.divID AS loser_team_division,
            tl.rank AS loser_team_rank,
            tl.playoff AS loser_team_playoff,
            tl.seeded AS loser_team_seeded,
            tl.firstRound AS loser_team_first_round,
            tl.semis AS loser_team_semis,
            tl.finals AS loser_team_finals,
            tl.name AS loser_team_name,
            tl.o_fgm AS loser_team_off_fg_made,
            tl.o_fga AS loser_team_off_fg_attempted,
            tl.o_ftm AS loser_team_off_ft_made,
            tl.o_fta AS loser_team_off_ft_attempted,
            tl.o_3pm AS loser_team_off_3pt_made,
            tl.o_3pa AS loser_team_off_3pt_attempted,
            tl.o_oreb AS loser_team_off_orebounds,
            tl.o_dreb AS loser_team_off_drebounds,
            tl.o_reb AS loser_team_off_rebounds,
            tl.o_asts AS loser_team_off_assists,
            tl.o_pf AS loser_team_off_pf,
            tl.o_stl AS loser_team_off_steals,
            tl.o_to AS loser_team_off_turnovers,
            tl.o_blk AS loser_team_off_blocks,
            tl.o_pts AS loser_team_off_points,
            tl.d_fgm AS loser_team_def_fg_made,
            tl.d_fga AS loser_team_def_fg_attempted,
            tl.d_ftm AS loser_team_def_ft_made,
            tl.d_fta AS loser_team_def_ft_attempted,
            tl.d_3pm AS loser_team_def_3pt_made,
            tl.d_3pa AS loser_team_def_3pt_attempted,
            tl.d_oreb AS loser_team_def_orebounds,
            tl.d_dreb AS loser_team_def_drebounds,
            tl.d_reb AS loser_team_def_rebounds,
            tl.d_asts AS loser_team_def_assists,
            tl.d_pf AS loser_team_def_pf,
            tl.d_stl AS loser_team_def_steals,
            tl.d_to AS loser_team_def_turnovers,
            tl.d_blk AS loser_team_def_blocks,
            tl.d_pts AS loser_team_def_points,
            tl.tmORB AS loser_team_orb,
            tl.tmDRB AS loser_team_drb,
            tl.tmTRB AS loser_team_trb,
            tl.opptmORB AS loser_team_opp_orb,
            tl.opptmDRB AS loser_team_opp_drb,
            tl.opptmTRB AS loser_team_opp_trb,
            tl.won AS loser_team_wins,
            tl.lost AS loser_team_losses,
            tl.GP AS loser_team_games_played,
            tl.homeW AS loser_team_home_wins,
            tl.homeL AS loser_team_home_losses,
            tl.awayW AS loser_team_away_wins,
            tl.awayL AS loser_team_away_losses,
            tl.confW AS loser_team_conf_wins,
            tl.confL AS loser_team_conf_losses,
            tl.min AS loser_team_minutes,
            tl.attend AS loser_team_attendance,
            tl.arena AS loser_team_arena,

            -- Winning team post-season columns
            tpw.W AS winner_post_W,
            tpw.L AS winner_post_L,

            -- Losing team post-season columns
            tpl.W AS loser_post_W,
            tpl.L AS loser_post_L,

            -- Coach of winning team
            cw.coachID AS winner_coach_id,
            cw.won AS winner_coach_wins,
            cw.lost AS winner_coach_losses,
            cw.stint AS winner_coach_stint,
            cw.post_wins AS winner_coach_post_wins,
            cw.post_losses AS winner_coach_post_losses,
                   
            -- Coach of losing team
            cl.coachID AS loser_coach_id,
            cl.won AS loser_coach_wins,
            cl.lost AS loser_coach_losses,
            cl.stint AS loser_coach_stint,
            cl.post_wins AS loser_coach_post_wins,
            cl.post_losses AS loser_coach_post_losses,
                   
            pt.*,
            p.*,
            ap.*

        FROM 
            series_post AS sp

        -- Join teams (winner and loser)
        JOIN teams AS tw ON sp.tmIDWinner = tw.tmID AND sp.year = tw.year
        JOIN teams AS tl ON sp.tmIDLoser = tl.tmID AND sp.year = tl.year

        -- Join teams_post (winner and loser)
        JOIN teams_post AS tpw ON tw.tmID = tpw.tmID AND tw.year = tpw.year
        JOIN teams_post AS tpl ON tl.tmID = tpl.tmID AND tl.year = tpl.year
                   
        -- Join coaches (winner and loser)
        JOIN coaches AS cw ON cw.tmID = tw.tmID AND cw.year = tw.year
        JOIN coaches AS cl ON cl.tmID = tl.tmID AND cl.year = tl.year

        -- Join players_teams (winner and loser)
        JOIN players_teams AS pt ON pt.tmID = tw.tmID AND pt.year = tw.year
        

        -- Join players
        JOIN players AS p ON p.bioID = pt.playerID
        
        -- Join 
        JOIN awards_players AS ap ON ap.playerID = p.bioID
                   
        ORDER BY sp.year ASC;
    ''')

    rows = cursor.fetchall()
    
    # Get column headers
    headers = [description[0] for description in cursor.description]
    
    # Create a list of dictionaries
    result = [dict(zip(headers, row)) for row in rows]
    
    return result

def init_db():
    # create database
    create_tables(conn) # should we want to define the primary and foreign keys of each table
    csv_to_sqlite(csv_directory, conn)
    print(f'Database "{db_name}" successfully created and CSV files imported.')


csv_directory = './data'  # Path to csv files
db_name = 'Database/database.db' # Path to database

conn = sqlite3.connect(db_name)
conn.row_factory = sqlite3.Row  # This allows access to columns by name

#init_db() # only necesary when the database is not created yet or has changed

#schema = get_schema(conn)
# put schema in a .sql file
#with open('Database/schema.sql', 'w') as f:
#    f.write(schema)

# join all tables
result = join_all_tables(conn)

# put result in a .csv file
file_path = 'Database/result.csv'
df = pd.DataFrame(result)
df.to_csv(file_path, index=False)