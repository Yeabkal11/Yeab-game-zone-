from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
# Placeholder for database functions
async def get_user_balance(user_id): return 100.00
async def create_game(creator_id, stake, win_condition): return "game_id_123"
async def get_game(game_id): return {"stake": 50, "creator_id": 12345, "status": "new"}
async def join_game(game_id, player_id): return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    user = update.effective_user
    welcome_message = (
        f"Welcome to Yeab Game Zone, {user.mention_html()}!\n\n"
        "Here you can play Ludo for real money.\n\n"
        "Commands:\n"
        "/play - Start a new Ludo game\n"
        "/balance - Check your wallet balance\n"
        "/deposit - Add funds to your wallet\n"
        "/withdraw - Withdraw funds from your wallet"
    )
    await update.message.reply_html(welcome_message)

async def play_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /play command to initiate game creation."""
    keyboard = [
        [
            InlineKeyboardButton("20 ETB", callback_data="stake_20"),
            InlineKeyboardButton("50 ETB", callback_data="stake_50"),
            InlineKeyboardButton("100 ETB", callback_data="stake_100"),
        ],
        [InlineKeyboardButton("Custom Amount", callback_data="stake_custom")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Step 1: Choose your stake amount.", reply_markup=reply_markup)

async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    
    # Store game creation data in user_data
    if 'game_setup' not in context.user_data:
        context.user_data['game_setup'] = {}

    data = query.data
    
    if data.startswith("stake_"):
        if data == "stake_custom":
            await query.edit_message_text(text="Please enter a custom stake amount (min 10 ETB):")
            # We'll need a message handler to catch the user's text input
            return
        
        stake = int(data.split("_")[1])
        context.user_data['game_setup']['stake'] = stake
        
        keyboard = [
            [
                InlineKeyboardButton("1 Token Home", callback_data="win_1"),
                InlineKeyboardButton("2 Tokens Home", callback_data="win_2"),
                InlineKeyboardButton("4 Tokens Home (Full House)", callback_data="win_4"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Stake set to {stake} ETB.\n\nStep 2: Choose the winning condition.", reply_markup=reply_markup)

    elif data.startswith("win_"):
        win_condition = int(data.split("_")[1])
        context.user_data['game_setup']['win_condition'] = win_condition
        stake = context.user_data['game_setup']['stake']
        creator = update.effective_user
        
        # Create game in database (conceptual)
        game_id = await create_game(creator.id, stake, win_condition)

        # Create lobby message
        lobby_text = (
            f"{creator.first_name} has started a Ludo game for {stake} ETB.\n"
            f"Winner needs {win_condition} token(s) home to win."
        )
        keyboard = [[InlineKeyboardButton("Join Game", callback_data=f"join_{game_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(text=lobby_text, reply_markup=reply_markup)
        
    elif data.startswith("join_"):
        game_id = data.split("_")[1]
        player = update.effective_user
        
        # Logic to join the game
        # 1. Get game details
        game = await get_game(game_id)
        if not game:
            await query.edit_message_text("This game is no longer available.")
            return

        # 2. Check balances
        creator_balance = await get_user_balance(game['creator_id'])
        joiner_balance = await get_user_balance(player.id)
        
        if creator_balance < game['stake'] or joiner_balance < game['stake']:
             await query.edit_message_text("One of the players has insufficient funds. Game cannot start.")
             return
        
        # 3. Deduct stakes & start game (conceptual)
        # In a real app: use a database transaction here
        # await deduct_stake(game['creator_id'], game['stake'])
        # await deduct_stake(player.id, game['stake'])
        # await update_game_status(game_id, "active", player.id)
        
        await query.edit_message_text("Game is starting! Both players have been charged. The board will appear shortly.")
        # Here you would trigger the actual game start logic
        
async def handle_custom_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles when the user sends a custom stake amount."""
    if 'game_setup' in context.user_data and 'stake' not in context.user_data['game_setup']:
        try:
            stake = int(update.message.text)
            if stake < 10:
                await update.message.reply_text("Minimum stake is 10 ETB. Please enter a higher amount.")
                return
            
            context.user_data['game_setup']['stake'] = stake
            
            keyboard = [
                [
                    InlineKeyboardButton("1 Token Home", callback_data="win_1"),
                    InlineKeyboardButton("2 Tokens Home", callback_data="win_2"),
                    InlineKeyboardButton("4 Tokens Home (Full House)", callback_data="win_4"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(text=f"Stake set to {stake} ETB.\n\nStep 2: Choose the winning condition.", reply_markup=reply_markup)

        except ValueError:
            await update.message.reply_text("Invalid amount. Please enter a number.")