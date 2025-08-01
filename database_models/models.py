import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def get_pool():
    """Creates a database connection pool."""
    return await asyncpg.create_pool(dsn=DATABASE_URL)

async def init_db():
    """Initializes the database and creates tables if they don't exist."""
    pool = await get_pool()
    async with pool.acquire() as connection:
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id BIGINT PRIMARY KEY,
                username TEXT,
                balance DECIMAL(10, 2) DEFAULT 0.00
            );
        """)
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS games (
                game_id SERIAL PRIMARY KEY,
                creator_id BIGINT REFERENCES users(telegram_id),
                opponent_id BIGINT REFERENCES users(telegram_id),
                stake DECIMAL(10, 2),
                pot DECIMAL(10, 2),
                win_condition INT,
                status TEXT, -- 'new', 'active', 'finished', 'forfeited'
                winner_id BIGINT,
                last_action_timestamp TIMESTAMPTZ,
                game_state JSONB -- To store board, player positions etc.
            );
        """)
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                user_id BIGINT REFERENCES users(telegram_id),
                amount DECIMAL(10, 2),
                type TEXT, -- 'deposit', 'withdrawal'
                status TEXT, -- 'pending', 'completed', 'failed'
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)
    await pool.close()

# You would add more functions here to interact with the database, e.g.:
# - create_user(telegram_id, username)
# - get_user(telegram_id)
# - update_balance(telegram_id, amount)
# - create_game(...)
# - get_game(game_id)
# - update_game_state(...)