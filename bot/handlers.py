# In bot/handlers.py

# ... other imports
import logging # Add this

logger = logging.getLogger(__name__)

# --- MODIFY THESE FUNCTIONS ---

async def get_user_balance(user_id):
    logger.warning("DB DISABLED: Returning dummy balance 100.00")
    return 100.00

async def create_game(creator_id, stake, win_condition):
    logger.warning("DB DISABLED: Returning dummy game_id")
    return "dummy_game_123"

async def get_game(game_id):
    logger.warning("DB DISABLED: Returning dummy game data")
    return {"stake": 50, "creator_id": 12345, "status": "new"}

async def join_game(game_id, player_id):
    logger.warning("DB DISABLED: Simulating successful join")
    return True

# ... the rest of your handlers file