# Settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token='YOUR API ТОКЕN') # Token API to Telegram
dispatcher = updater.dispatcher
# Command processing
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello, how about a talk?')
def textMessage(bot, update):
    request = apiai.ApiAI('YOUR API TOKEN').text_request() # Token API to Dialogflow
    request.lang = 'en' # In what language the request will be sent
    request.session_id = 'BatlabAIBot' # ID Sessions of the dialogue 
    request.query = update.message.text # We send a request to the AI with a message from the user
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Disassemble JSON and pull out the answer
    # If there is an answer from the bot we send it to the user, if not - the bot did not understand it
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='I do not understand you!')
# Handlers
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Add handlers to the dispatch
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Getting started for updates
updater.start_polling(clean=True)
# Stop the bot if Ctrl + C was pressed
updater.idle()
