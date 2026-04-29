import psycopg2

conn = psycopg2.connect(
    dbname="snake_game",
    user="daniyar",
    password="",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER NOT NULL,
        level_reached INTEGER NOT NULL,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """)
    conn.commit()

def get_or_create_player(username):
    cursor.execute("SELECT id FROM players WHERE username=%s", (username,))
    player = cursor.fetchone()

    if player:
        return player[0]

    cursor.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
    conn.commit()
    return cursor.fetchone()[0]

def save_game(username, score, level):
    player_id = get_or_create_player(username)

    cursor.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level))

    conn.commit()

def get_top_scores():
    cursor.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        ORDER BY g.score DESC
        LIMIT 10
    """)
    return cursor.fetchall()

def get_personal_best(username):
    cursor.execute("""
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        WHERE p.username=%s
    """, (username,))
    result = cursor.fetchone()[0]
    return result if result else 0