import json
from telegram.ext import Dispatcher, CallbackQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import Update, Bot


from ptb_telegramHandlers import  start, btn_carga, btn_comercio, btn_pasajeros, equipo, combustible, personal, siniestros, robo, vandalismo, bloqueos, desconocido, mensual, anual, tablas, graficas, excel
from aws_lambda_powertools.utilities import parameters

# TelegramBotToken se obtiene del servicio de AWS Systems Manager 
ssm_provider = parameters.SSMProvider()
TelegramBotToken = ssm_provider.get("/telegramartfbot/telegram/bot_token", decrypt=True)

bot = Bot(token=TelegramBotToken)
dispatcher = Dispatcher(bot, None, use_context=True)

# States
FIRST, SECOND, THIRD = range(3)

# Callback data
CARGA, COMERCIO, PASAJEROS, EQUIPO, COMBUSTIBLE, PERSONAL, SINIESTROS, ROBO, VANDALISMO, BLOQUEOS, MENSUAL, ANUAL, GRAFICA, TABLA, EXCEL = range(15)


def lambda_handler(event, context):

    # se configura el conversation handler con los estados FIRST, SECOND y THIRD
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(command='start', callback=start)],
        states={
            FIRST: [CallbackQueryHandler(btn_carga, pattern='^' + str(CARGA) + '$'),
                    CallbackQueryHandler(btn_comercio, pattern='^' + str(COMERCIO) + '$'),
                    CallbackQueryHandler(btn_pasajeros, pattern='^' + str(PASAJEROS) + '$'),
                    CallbackQueryHandler(equipo, pattern='^' + str(EQUIPO) + '$'),
                    CallbackQueryHandler(combustible, pattern='^' + str(COMBUSTIBLE) + '$'),
                    CallbackQueryHandler(personal, pattern='^' + str(PERSONAL) + '$'),
                    CallbackQueryHandler(siniestros, pattern='^' + str(SINIESTROS) + '$'),
                    CallbackQueryHandler(robo, pattern='^' + str(ROBO) + '$'),
                    CallbackQueryHandler(vandalismo, pattern='^' + str(VANDALISMO) + '$'),
                    CallbackQueryHandler(bloqueos, pattern='^' + str(BLOQUEOS) + '$')
                    ],
            SECOND: [CallbackQueryHandler(mensual, pattern='^' + str(MENSUAL) + '$'),
                     CallbackQueryHandler(anual, pattern='^' + str(ANUAL) + '$')
                     ],
            THIRD:  [CallbackQueryHandler(tablas, pattern='^' + str(TABLA) + '$'),
                     CallbackQueryHandler(graficas, pattern='^' + str(GRAFICA) + '$'),
                     CallbackQueryHandler(excel, pattern='^' + str(EXCEL) + '$')
                    ]
        },
        fallbacks=[CommandHandler(command='start', callback=start)]
    )
     
    # 
    dispatcher.add_handler(conv_handler)
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

