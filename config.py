from dotenv import load_dotenv
import os

# import from .env file
load_dotenv()

# get bot token by BotFather
TOKEN = os.getenv('TG_TOKEN')

# init game symbols
FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'

# describe default state for game keyboard
DEFAULT_STATE = [[FREE_SPACE for _ in range(3)] for _ in range(3)]

# describe start and finish game state
CONTINUE_GAME, FINISH_GAME = range(2)
