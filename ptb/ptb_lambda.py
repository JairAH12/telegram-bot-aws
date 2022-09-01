
import json
from telegram.ext import Dispatcher, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from telegram import Update, Bot


from ptb_telegramHandlers import button, start, help_command, btn_carga, btn_comercio, btn_pasajeros, equipo, combustible, personal, siniestros, robo, vandalismo, bloqueos, desconocido
from aws_lambda_powertools.utilities import parameters

# TelegramBotToken se obtiene del servicio de AWS Systems Manager 
ssm_provider = parameters.SSMProvider()
TelegramBotToken = ssm_provider.get("/telegramartfbot/telegram/bot_token", decrypt=True)

bot = Bot(token=TelegramBotToken)
dispatcher = Dispatcher(bot, None, use_context=True)


def lambda_handler(event, context):

    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help',help_command))
    dispatcher.add_handler(CommandHandler('carga', btn_carga))
    dispatcher.add_handler(CommandHandler('comercio',btn_comercio))
    dispatcher.add_handler(CommandHandler('pasajeros', btn_pasajeros))
    dispatcher.add_handler(CommandHandler('equipo',equipo))
    dispatcher.add_handler(CommandHandler('combustible',combustible))
    dispatcher.add_handler(CommandHandler('personal',personal))
    dispatcher.add_handler(CommandHandler('siniestros',siniestros))
    dispatcher.add_handler(CommandHandler('robo',robo))
    dispatcher.add_handler(CommandHandler('vandalismo', vandalismo))
    dispatcher.add_handler(CommandHandler('bloqueos', bloqueos))
    dispatcher.add_handler(MessageHandler(Filters.command, desconocido))

    try:
        dispatcher.process_update(
            Update.de_json(json.loads(event["body"]), bot)
        )

    except Exception as e:
        print(e)
        return {"statusCode": 500}

    return {
        'statusCode': 200
    }
