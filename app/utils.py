import numpy as np
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from copy import deepcopy
from config import DEFAULT_STATE, FREE_SPACE


def get_default_state() -> list[list[str]]:
    """Helper function to get default state of the game"""
    # deepcopy need to get clear default state (in game state will changed)
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) \
        -> list[list[InlineKeyboardButton]]:
    """Display the current tic tac toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ] for c in range(3)
    ]


async def update_keyboard(update: Update, state: list[list[str]]) -> None:
    keyboard = generate_keyboard(state)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_reply_markup(
        reply_markup=reply_markup
    )


def ai_model(state: list[list[str]]) -> tuple[int]:
    np_state = np.array(state)
    free_idx = np.where(np_state == FREE_SPACE)
    ai_choose = np.random.randint(0, high=len(free_idx[0]))
    return free_idx[0][ai_choose], free_idx[1][ai_choose]


def won(state: list[list[str]], sym: str) -> bool:
    """Check if crosses or zeros have won the game"""
    np_state = np.array(state)
    bool_mask = np_state == sym
    if any(np.sum(bool_mask, axis=1) == 3) or \
       any(np.sum(bool_mask, axis=0) == 3) or \
       (np.trace(bool_mask) == 3) or \
       (np.trace(np.fliplr(bool_mask)) == 3):
        return True
    return False


def exist_free(state: list[list[str]]) -> bool:
    np_state = np.array(state)
    return (np_state == FREE_SPACE).any()
