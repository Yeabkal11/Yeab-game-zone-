# In database_models/models.py

import asyncpg
import os
import logging # Add this

logger = logging.getLogger(__name__) # Add this
DATABASE_URL = os.getenv("DATABASE_URL")

async def get_pool():
    """Creates a database connection pool."""
    logger.warning("DATABASE CONNECTION IS TEMPORARILY DISABLED FOR DEBUGGING.")
    return None # TEMPORARILY DISABLE DB
    # return await asyncpg.create_pool(dsn=DATABASE_URL)

async def init_db():
    """Initializes the database and creates tables if they don't exist."""
    pool = await get_pool()
    if not pool: # Add this check
        logger.error("Cannot initialize DB, no pool available.")
        return

    async with pool.acquire() as connection:
        # ... (rest of the function is fine)
    # ...