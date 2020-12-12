from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, ConversationHandler
import logging
import os

from commands import start, ask_user_info, get_name, get_age, get_sex, get_height, get_weight, show_info, fallback, \
    request_update, specify_update, update_name, update_age, update_height, update_weight,  restart, remove_user, \
    unknown

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

TOKEN = os.environ.get("TOKEN")

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

get_person_info_handler = CommandHandler("show", show_info)
dispatcher.add_handler(get_person_info_handler)

ask_user_info_handler = ConversationHandler(
    entry_points=[
        CommandHandler("register", ask_user_info)
    ],
    states={
        "get_name": [MessageHandler(Filters.text & (~Filters.command), get_name)],
        "get_age": [MessageHandler(Filters.text & (~Filters.command), get_age)],
        "get_sex": [MessageHandler(Filters.text & (~Filters.command), get_sex)],
        "get_height": [MessageHandler(Filters.text & (~Filters.command), get_height)],
        "get_weight": [MessageHandler(Filters.text & (~Filters.command), get_weight)],
    },
    fallbacks=[MessageHandler(Filters.command, fallback)],
)
dispatcher.add_handler(ask_user_info_handler)

update_info_handler = ConversationHandler(
    entry_points=[
        CommandHandler("update", request_update)
    ],
    states={
        "specify_update": [MessageHandler(Filters.text, specify_update)],
        "update_name": [MessageHandler(Filters.text, update_name)],
        "update_age": [MessageHandler(Filters.text, update_age)],
        "update_height": [MessageHandler(Filters.text, update_height)],
        "update_weight": [MessageHandler(Filters.text, update_weight)]
    },
    fallbacks=[]
)
dispatcher.add_handler(update_info_handler)

remove_user_handler = ConversationHandler(
    entry_points=[
        CommandHandler("restart", restart)
    ],
    states={
        "restart": [MessageHandler(Filters.text, remove_user)]
    },
    fallbacks=[]
)
dispatcher.add_handler(remove_user_handler)

# should always be last of the handlers in the code
unknown_handler = MessageHandler(Filters.text, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
