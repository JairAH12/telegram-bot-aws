import io
import os
import json
from telegram.ext import *
from telegram import *
import pandas as pd
import openpyxl
import urllib.request
from aws_lambda_powertools.utilities import parameters

ssm_provider = parameters.SSMProvider()

TelegramBotToken = ssm_provider.get("/telegramartfbot/telegram/bot_token", decrypt=True)


bot = Bot(token=TelegramBotToken)
dispatcher = Dispatcher(bot, None, use_context=True)
datos = pd.read_excel("https://resources-bot-artf.s3.amazonaws.com/ruta_archivos.xlsx",sheet_name="rutas",index_col=0)
s3Buncket="https://resources-bot-artf.s3.amazonaws.com/"



def start(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text= "Bienvenido al bot de Estadística de la ARTF.\n\n"
                             "Con este bot puedes consultar el avance de los datos más importantes del,"
                             " Sistema Ferroviario Mexicano \U0001F686 /help.")

def help_command(update: Update, context: CallbackContext):
    update.message.chat.send_action(action=ChatAction.TYPING,timeout=None)
    ''' Help'''
    update.message.reply_text(
    "Este bot te permite consultar los datos estadísticos más importantes del ferrocarril \U0001F686.\n\n"
    "Uiliza /start para checar si está activo este bot. "
    "A continuación se muestra la lista de comandos que puedes utilizar:\n\n"
    "/carga - Datos de movimiento de carga\n"
    "/pasajeros - Datos de movimiento de pasajeros\n"
    "/comercio - Datos del comercio exterior\n"
    "/equipo - Datos del equipo del SFM\n"
    "/personal - Datos del personal del SFM\n"
    "/bloqueos - Datos de vandalismo en el SFM\n"
    "/siniestros - Datos de siniestros del SFM\n"
    "/robo - Datos de robos en el SFM\n"
    "/vandalismo - Datos de vandalismo en el SFM\n"
    "/combustible - Datos del consumo energético en el SFM\n"
    )

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id=query.message.chat_id
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING, timeout=None)

    if query.data == '1_carga_anual':
        query.edit_message_text(text="Datos anuales de carga del SFM.")
        carga_anual(update, context, chat_id)
    elif query.data == '1_carga_mensual':
        query.edit_message_text(text="Datos mensuales de carga del SFM.")
        carga_mensual(update, context, chat_id)
    elif query.data == '2_pasajeros_anual':
        query.edit_message_text(text="Datos anuales de pasajeros del SFM.")
        pasajeros_anual(update, context, chat_id)
    elif query.data == '2_pasajeros_mensual':
        query.edit_message_text(text="Datos mensuales de pasajeros del SFM.")
        pasajeros_mensual(update, context, chat_id)
    elif query.data == '3_comercio_anual':
        query.edit_message_text(text="Datos anuales de comercio exterior del SFM.")
        comercio_anual(update, context, chat_id)
    elif query.data == '3_comercio_mensual':
        query.edit_message_text(text="Datos mensuales de comercio exterior del SFM.")
        comercio_mensual(update, context, chat_id)
    ConversationHandler.END


##################### ESTADÍSTICA DE CARGA #####################
################################################################
def btn_carga(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Carga anual", callback_data='1_carga_anual'),
                 InlineKeyboardButton("Carga mensual", callback_data='1_carga_mensual')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('¿Con qué periodicidad prefieres la información? \U0001F4C5:', reply_markup=reply_markup)

def carga_anual(update: Update, context: CallbackContext, chat_id):
    ''' toneladas '''
    context.bot.send_message(chat_id, text="Toneladas netas:")
    carpeta = 1
    img = "eta"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    context.bot.sendPhoto(chat_id, photo=imgpath)

    ''' toneladas kilómetro'''
    context.bot.send_message(chat_id, text="Toneladas-kilómetro")
    carpeta = 1
    img = "etkma"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    context.bot.sendPhoto(chat_id, photo=imgpath)


def carga_mensual(update: Update, context: CallbackContext, chat_id):
    context.bot.send_message(chat_id, text="Carros cargados:")
    carpeta = 1
    img = "carros"
    doc = "tcarros"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(chat_id, photo=docpath)
    context.bot.sendPhoto(chat_id, photo=imgpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = img + '.xlsx'
    context.bot.sendDocument(chat_id, document=tab)

    ''' toneladas '''
    context.bot.send_message(chat_id, text="Toneladas netas:")
    carpeta = 1
    img = "toneladas"
    doc = "ttoneladas"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(chat_id, photo=docpath)
    context.bot.sendPhoto(chat_id, photo=imgpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = img + '.xlsx'
    context.bot.sendDocument(chat_id, document=tab)

    ''' toneladas kilómetro'''
    context.bot.send_message(chat_id, text="Toneladas-kilómetro")
    carpeta = 1
    img = "tkm"
    doc = "ttkm"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(chat_id, photo=docpath)
    context.bot.sendPhoto(chat_id, photo=imgpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = img + '.xlsx'
    context.bot.sendDocument(chat_id, document=tab)

def btn_comercio(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Comercio anual", callback_data='3_comercio_anual'),
                 InlineKeyboardButton("Comercio mensual", callback_data='3_comercio_mensual')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('¿Con qué periodicidad prefieres la información? \U0001F4C5:', reply_markup=reply_markup)

def comercio_anual(update: Update, context: CallbackContext, chat_id):
    ''' evolución '''
    context.bot.send_message(chat_id, text="Toneladas netas/Toneladas-kilómetro:")
    carpeta = 2
    img = "etca"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    context.bot.sendPhoto(chat_id, photo=imgpath)

    ''' porcentaje '''
    context.bot.send_message(chat_id, text="Proporción")
    carpeta = 2
    img = "epcea"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    context.bot.sendPhoto(chat_id, photo=imgpath)

    ''' Tablas '''
    ''' carga de comercio '''
    context.bot.send_message(chat_id, text="Toneladas netas:")
    carpeta = 2
    doc = "tccea"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(chat_id, document=tab)

    ''' carga de comercio km '''
    context.bot.send_message(chat_id, text="Toneladas-kilómetro")
    carpeta = 2
    doc = "ttkmcea"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(chat_id, document=tab)

def comercio_mensual(update: Update, context: CallbackContext, chat_id):
    ''' Tablas '''
    ''' carga de comercio '''
    context.bot.send_message(chat_id, text="Toneladas netas:")
    carpeta = 2
    doc = "tccem"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(chat_id, document=tab)

    ''' carga de comercio km '''
    context.bot.send_message(chat_id, text="Toneladas-kilómetro")
    carpeta = 2
    doc = "ttkmcem"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(chat_id, document=tab)


##################### ESTADÍSTICA DE PASAJEROS #####################
################################################################
def btn_pasajeros(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Pasajeros anuales", callback_data='2_pasajeros_anual'),
                 InlineKeyboardButton("Pasajeros mensuales", callback_data='2_pasajeros_mensual')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('¿Con qué periodicidad prefieres la información? \U0001F4C5:', reply_markup=reply_markup)

def pasajeros_anual(update: Update, context: CallbackContext, chat_id):
    ''' pasajeros '''
    context.bot.send_message(chat_id, text="Pasajeros:")
    carpeta = 3
    img = "vpa"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    context.bot.sendPhoto(chat_id, photo=imgpath)

    ''' pkm '''
    context.bot.send_message(chat_id, text="Pasajeros-kilómetro:")
    carpeta = 3
    doc = "tvpa"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(chat_id, document=tab)

def pasajeros_mensual(update: Update, context: CallbackContext, chat_id):
    ''' pasajeros '''
    context.bot.send_message(chat_id, text="Pasajeros:")
    carpeta = 3
    img = "ptm"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    context.bot.sendPhoto(chat_id, photo=imgpath)

    #context.bot.send_message(chat_id, text="Pasajeros-kilómetro:")
    context.bot.send_message(chat_id, text="Tabla con comparativo:")
    carpeta = 3
    doc = "tptm"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(chat_id, document=tab)

##################### ESTADÍSTICA DE EQUIPO FERROVIARIO ##############
################################################################
def equipo(update: Update, context: CallbackContext):
    ''' Composición de flota '''
    context.bot.send_message(update.message.chat_id, text="Datos de equipo ferroviario del SFM.\n\n")
    ''' equipo '''
    context.bot.send_message(update.message.chat_id, text="Equipo ferroviario:")
    carpeta = 4
    doc = "tefa"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    ''' composición de flota '''
    context.bot.send_message(update.message.chat_id, text="Composición de flota:")
    carpeta = 4
    img = "ecfa"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    context.bot.sendPhoto(update.message.chat_id, photo=imgpath)

    ''' evolución '''
    context.bot.send_message(update.message.chat_id, text="Evolución y composición:")
    carpeta = 4
    doc = "tecfa"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

##################### ESTADÍSTICA DE CONSUMO ENERGÉTICO ##############
################################################################
def combustible(update: Update, context: CallbackContext):
    ''' Consumo energético '''
    context.bot.send_message(update.message.chat_id, text="Datos del consumo energético del SFM.\n\n")
    ''' consumo de energía para el transporte de pasajeros '''
    context.bot.send_message(update.message.chat_id, text="Para el transporte de pasajeros:")
    carpeta = 5
    doc = "tcepa"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    ''' consumo de energía para el transporte de carga '''
    context.bot.send_message(update.message.chat_id, text="Para el transporte de carga:")
    carpeta = 5
    doc = "tcdm"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    ''' consumo de energía por tipo de servicio '''
    context.bot.send_message(update.message.chat_id, text="Por tipo de servicio:")
    carpeta = 5
    img = "ecca"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    context.bot.sendPhoto(update.message.chat_id, photo=imgpath)

##################### ESTADÍSTICA DE PERSONAL ##############
################################################################
def personal(update: Update, context: CallbackContext):
    ''' Personal empleado '''
    context.bot.send_message(update.message.chat_id, text="Datos del personal del SFM.\n\n")
    ''' personal '''
    context.bot.send_message(update.message.chat_id, text="Personal empleado:")
    carpeta = 6
    doc = "tpea"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    ''' evolución '''
    context.bot.send_message(update.message.chat_id, text="Personal activo:")
    carpeta = 6
    img = "epa"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    context.bot.sendPhoto(update.message.chat_id, photo=imgpath)

##################### ESTADÍSTICA DE SINIESTROS #####################
################################################################
def siniestros(update: Update, context: CallbackContext):
    ''' Siniestros totales '''
    context.bot.send_message(update.message.chat_id, text="Datos de siniestros en el SFM.\n\n")
    ''' siniestros totales '''
    context.bot.send_message(update.message.chat_id, text="Siniestros totales:")
    carpeta = 7
    img = "rsm"
    doc = "trsm"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    context.bot.sendPhoto(update.message.chat_id, photo=imgpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = img + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    ''' siniestros por grupo '''
    context.bot.send_message(update.message.chat_id, text="Siniestros por grupo:")
    carpeta = 7
    img = "esgt"
    doc = "tsgt"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    context.bot.sendPhoto(update.message.chat_id, photo=imgpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = img + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    ''' siniestros por tipo '''
    context.bot.send_message(update.message.chat_id, text="Siniestros por tipo")
    carpeta = 7
    doc = "trscg"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

def robo(update: Update, context: CallbackContext):
    ''' Robos totales '''
    context.bot.send_message(update.message.chat_id, text="Datos de robo en el SFM.\n\n")
    ''' robo total '''
    context.bot.send_message(update.message.chat_id, text="Robos totales:")
    carpeta = 8
    img = "rrm"
    doc = "trrm"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    context.bot.sendPhoto(update.message.chat_id, photo=imgpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = img + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    ''' robos por categoría '''
    context.bot.send_message(update.message.chat_id, text="Robos por categoría:")
    context.bot.send_message(update.message.chat_id, text="Robo a tren:")
    carpeta = 8
    doc = "trct"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    ''' robos por tipo '''
    context.bot.send_message(update.message.chat_id, text="Robo a vía")
    carpeta = 8
    doc = "trcv"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

def vandalismo(update: Update, context: CallbackContext):
    ''' Vandalismo totales '''
    context.bot.send_message(update.message.chat_id, text="Datos de vandalismo en el SFM.\n\n")
    ''' vandalismo total '''
    context.bot.send_message(update.message.chat_id, text="Vandalismo total:")
    carpeta = 9
    img = "vtm"
    doc = "tvtm"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    context.bot.sendPhoto(update.message.chat_id, photo=imgpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = img + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    carpeta = 9
    img = "vvm"
    doc = "tvvm"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    context.bot.sendPhoto(update.message.chat_id, photo=imgpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = img + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    ''' vandalismo por categoría '''
    context.bot.send_message(update.message.chat_id, text="Vandalismo por categoría:")
    context.bot.send_message(update.message.chat_id, text="Vandalismo al tren:")
    carpeta = 9
    doc = "tvct"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    ''' vandalismo por tipo '''
    context.bot.send_message(update.message.chat_id, text="Vandalismo de vía")
    carpeta = 9
    doc = "tvcv"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

def bloqueos(update: Update, context: CallbackContext):
    ''' Bloqueos totales '''
    context.bot.send_message(update.message.chat_id, text="Datos de bloqueos en el SFM.\n\n")
    carpeta = 10
    doc = "trbva"
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = doc + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

    ''' bloqueos totales '''
    context.bot.send_message(update.message.chat_id, text="Bloqueos totales:")
    carpeta = 10
    img = "ebf"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    context.bot.sendPhoto(update.message.chat_id, photo=imgpath)

    ''' horas de bloqueo '''
    context.bot.send_message(update.message.chat_id, text="Horas de bloqueo:")
    carpeta = 10
    img = "rchb"
    doc = "thvb"
    imgpath =  s3Buncket + datos.loc[str(carpeta) + '_' + img]["ruta"]
    docpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][0]
    tabpath =  s3Buncket + datos.loc[str(carpeta) + '_' + doc]["ruta"][1]
    context.bot.sendPhoto(update.message.chat_id, photo=docpath)
    context.bot.sendPhoto(update.message.chat_id, photo=imgpath)
    tab = urllib.request.urlopen(tabpath)
    tab.name = img + '.xlsx'
    context.bot.sendDocument(update.message.chat_id, document=tab)

def desconocido(update: Update, context: CallbackContext):
    ''' Desconocido '''
    context.bot.send_message(update.message.chat_id, text="Disculpa, no entendí tu mensaje \U0001F641.")

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
