from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from config import CONTINUE_GAME, FINISH_GAME, CROSS, FREE_SPACE, ZERO
from .utils import (
    get_default_state,
    generate_keyboard,
    update_keyboard,
    ai_model,
    won,
    exist_free
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Start new game!'
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='X (your) turn! Please, put X to the free place',
        reply_markup=reply_markup
    )
    return CONTINUE_GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Main processing of the game"""
    # get current state
    state = context.user_data['keyboard_state']
    # get user step
    user_step = [int(i) for i in update.callback_query.data]
    # =========================================================
    # check if user input is right
    if state[user_step[0]][user_step[1]] != FREE_SPACE:
        await update.callback_query.message.edit_text(
            'You need to select an empty cell'
        )
        return CONTINUE_GAME
    # =========================================================
    # continue if user input is right
    state[user_step[0]][user_step[1]] = CROSS
    # =========================================================
    # check if user win
    if won(state, sym=CROSS):
        await update_keyboard(update, state)
        await update.effective_chat.send_message(
            text="You win! Use /start to play again"
        )
        return FINISH_GAME
    # =========================================================
    # check if exist free space
    if not exist_free(state):
        await update_keyboard(update, state)
        await update.effective_chat.send_message(
            text="Draw! Use /start to play again"
        )
        return FINISH_GAME
    # =========================================================
    # make AI game step
    ai_step = ai_model(state)
    state[ai_step[0]][ai_step[1]] = ZERO
    # =========================================================
    # check if AI win
    if won(state, sym=ZERO):
        await update_keyboard(update, state)
        await update.effective_chat.send_message(
            text="AI win! Use /start to play again"
        )
        return FINISH_GAME
    # =========================================================
    # if game continue -> gen update keyboard
    await update_keyboard(update, state)
    return CONTINUE_GAME


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default so you can play again with /start
    context.user_data['keyboard_state'] = None
    return ConversationHandler.END
