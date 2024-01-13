from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)
from telegram import BotCommand, BotCommandScopeDefault
from config import CONTINUE_GAME, FINISH_GAME, TOKEN
from .handlers import start, game, end


# create the Application and pass it your bot's token.
# bot = Application.builder().token(TOKEN).build()
bot = ApplicationBuilder().token(TOKEN).build()
# setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
# use the pattern parameter to pass CallbackQueries with specific
# data pattern to the corresponding handlers.
# ^ means "start of line/string"
# $ means "end of line/string"
# so ^ABC$ will only allow 'ABC'
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CONTINUE_GAME: [
            CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
            for r in range(3)
            for c in range(3)
        ],
        FINISH_GAME: [
            CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
            for r in range(3)
            for c in range(3)
        ],
    },
    fallbacks=[CommandHandler('end', end), CommandHandler('start', start)],
)
# add ConversationHandler to application that will be used for handling updates
bot.add_handler(conv_handler)
bot.bot.set_my_commands(
    [
        BotCommand("start", "command to start the game"),
        BotCommand("end", "command to finish the game"),
    ],
    scope=BotCommandScopeDefault(),
)
