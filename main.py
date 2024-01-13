from telegram import Update
from app.app import bot
from logger import LOGGER


if __name__ == '__main__':
    LOGGER(__name__).info("bot successfully started....")
    # Run the bot
    bot.run_polling(allowed_updates=Update.ALL_TYPES)
