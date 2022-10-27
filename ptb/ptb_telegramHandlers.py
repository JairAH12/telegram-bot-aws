"""Este módulo se definen todos los controladores del bot 

el usuario inicia la conversación con el bot al enviar el comando /start, esto llama a la función start que despliega
un listado de botones para seleccionar el tipo de información, este se considera el estado FIRST,  enseguida se despliega
una nueva lista de botones para escoger el perio, este conforma al estado SECOND, por último se despliegan las opciones
para escoger el formato, este será el estado THIRD, este último estado manda a llamar a las
funciones tablas(), graficas(), excel() dependiendo de la selección de usuario, estas funciones envían los archivos.
Durante el todo el proceso se usan las listas carpeta y frecuencia para almacenar la selecciones del usuario, generar
un identificador y con los diccionarios catalogo_graficas, catologo_tablas y mensajes, recuperar los nombres de los archivos a enviar.


Funciones disponibles:
- start:  Manda el primer mensaje del bot
- help_command: Despliega una lista con los comandos y muestra un el número de consultas
- button: Para las opciones con resolución de información, ejecuta la función correspondiente
- bnt_carga: Despliega el menú para seleccionar la resolución de la información de carga
- carga_anual: Envía la información de la carga con resolución anual y se registra la consulta
- carga_mensual:  Envía la información de la carga con resolución mensual y se registra la consulta
- btn_comercio: Despliega el menú para seleccionar la resolución de la información del comercio exterior
- comercio_anual:Envía la información de comercio exterior con resolución anual y se registra la consulta
- comercio_mensual: Envía la información del comercio exterior con resolución mensual y se registra la consulta
- btn_pasajeros: Despliega el menú para seleccionar la resolución de la información de los pasajeros
- pasajeros_anual:Envía la información de los pasajeros con resolución anual y se registra la consulta
- pasajeros_mesual: Envía la información de los pasajeros con resolución mensual y se registra la consulta
- equipo: Envía la información del equipo ferroviario del SFM
- combustible: Envía la información del consumo de combustible en el SFM
- personal: Envía la información del personal del SFM
- siniestros: Envía la información sobre los siniestros en el SFM
- robo: Envía la información sobre los robos en el SFM
- vandalismo: Envía la información del vandalismo en el SFM
- bloqueos: Envía la información de los bloqueos en el SFM
- desconocido:  Envía un mensaje para indicar que no se reconoce el comando
"""
from telegram.ext import *
from telegram import *
import pandas as pd
import openpyxl
import urllib.request

from ptb_dynamodb import registrar,consultarContador

# s3Bucket se concatenará con la cadena que se obtendrá del dataFrame “datos”  para conformar la ruta de descarga de los elementos almacenados en S3 (imgPath, docPath ó tabPath según corresponda)
datos = pd.read_excel("https://resources-bot-artf1.s3.amazonaws.com/ruta_archivos.xlsx",sheet_name="rutas",index_col=0)
s3Buncket="https://resources-bot-artf1.s3.amazonaws.com/"

# States
FIRST, SECOND, THIRD = range(3)

# Callback data
CARGA, COMERCIO, PASAJEROS, EQUIPO, COMBUSTIBLE, PERSONAL, SINIESTROS, ROBO, VANDALISMO, BLOQUEOS, MENSUAL, ANUAL, GRAFICA, TABLA, EXCEL = range(15)

# Catalogos de nombres de archivos
catalogo_graficas = {'110': ['carros', 'toneladas', 'tkm'],
                     '111': ['eta', 'etkma'],
                     '211': ['etca', 'epcea'],
                     '310': ['ptm'],
                     '311': ['vpa'],
                     '410': ['ecfa'],
                     '510': ['ecca'],
                     '610': ['epa'],
                     '710': ['rsm', 'esgt'],
                     '810': ['rrm'],
                     '910': ['vtm', 'vvm'],
                     '1010': ['ebf']
                     }
# catalogo tablas se usa para tablas y excel
catalogo_tablas = { '110': ['tcarros', 'ttoneladas', 'ttkm'],
                    '210': ['tccem', 'ttkmcem'],
                    '211': ['tccea','ttkmcea'],
                    '310': ['tptm'],
                    '311': ['tvpa'],
                    '410': ['tefa', 'tecfa'],
                    '510': ['tcepa', 'tcdm'],
                    '610': ['tpea'],
                    '710': ['trsm','tsgt','trscg'],
                    '810': ['trrm', 'trct', 'trcv'],
                    '910': ['tvtm', 'tvvm', 'tvct', 'tvcv'],
                    '1010': ['trbva', 'thvb']
                    }

mensajes = {         '110': ['carga_mensual', 'Datos mensuales de carga del SFM.'],
                     '111': ['carga_anual', 'Datos anuales de carga del SFM.'],
                     '210': ['comercio_mensual','Datos mensuales de comercio exterior del SFM.'],
                     '211': ['comercio_anual','Datos anuales de comercio exterior del SFM.'],
                     '310': ['pasajeros_mensual','Datos mensuales de pasajeros del SFM.'],
                     '311': ['pasajeros_anual','Datos anuales de pasajeros del SFM.'],
                     '410': ['equipo','Datos de equipo ferroviario del SFM.'],
                     '510': ['combustible','Datos del consumo energético del SFM.'],
                     '610': ['personal','Datos del personal del SFM.'],
                     '710': ['siniestros','Datos de siniestros en el SFM.'],
                     '810': ['robo','Datos de robo en el SFM.'],
                     '910': ['vandalismo','Datos de vandalismo en el SFM.'],
                     '1010': ['bloqueos','Datos de bloqueos en el SFM.']
                     }

carpeta = list()
frecuencia = list()


#  inicia conversación con el bot
def start(update, context):
    carpeta.clear()
    frecuencia.clear()
    fname = update.message.from_user.first_name

    # construye InlineKeyboard
    keyboard1 = [InlineKeyboardButton("Carga", callback_data=str(CARGA))]
    keyboard2 = [InlineKeyboardButton("Comercio", callback_data=str(COMERCIO))]
    keyboard3 = [InlineKeyboardButton("Pasajeros", callback_data=str(PASAJEROS))]
    keyboard4 = [InlineKeyboardButton("Equipo", callback_data=str(EQUIPO))]
    keyboard5 = [InlineKeyboardButton("Combustible", callback_data=str(COMBUSTIBLE))]
    keyboard6 = [InlineKeyboardButton("Personal", callback_data=str(PERSONAL))]
    keyboard7 = [InlineKeyboardButton("Siniestros", callback_data=str(SINIESTROS))]
    keyboard8 = [InlineKeyboardButton("Robo", callback_data=str(ROBO))]
    keyboard9 = [InlineKeyboardButton("Vandalismo", callback_data=str(VANDALISMO))]
    keyboard10 = [InlineKeyboardButton("Boqueos", callback_data=str(BLOQUEOS))]
    
    # creata reply markup
    reply_markup = InlineKeyboardMarkup([keyboard1, keyboard2,keyboard3,keyboard4,keyboard5, keyboard6,keyboard7,keyboard8,keyboard9,keyboard10])

    # actualiza el mensaje y despliega los botones
    update.message.reply_text(
        f"Bienvenido {format(fname)}. Este bot te permite consultar los datos estadísticos más importantes del ferrocarril \U0001F686.\n"
        f"Hasta el momento se han realizado {consultarContador()} consultas.\n\n"
        "A continuación se muestra la lista de comandos que puedes utilizar:",
        reply_markup=reply_markup
    )
    # tell ConversationHandler that we're in state 'FIRST' now
    return FIRST



##################### ESTADÍSTICA DE CARGA #####################
################################################################
def btn_carga(update, context):
    query = update.callback_query
    query.answer()
    carpeta.append(1)
    keyboard = [[InlineKeyboardButton("Carga anual", callback_data=str(ANUAL)),
                 InlineKeyboardButton("Carga mensual", callback_data=str(MENSUAL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué periodicidad prefieres la información de carga del SFM? \U0001F4C5:', reply_markup=reply_markup)
    return SECOND

def btn_comercio(update, context):
    query = update.callback_query
    query.answer()
    carpeta.append(2)
    keyboard = [[InlineKeyboardButton("Comercio anual", callback_data=str(ANUAL)),
                 InlineKeyboardButton("Comercio mensual", callback_data=str(MENSUAL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué periodicidad prefieres la información de comercio exterior del SFM? \U0001F4C5:', reply_markup=reply_markup)
    return SECOND


##################### ESTADÍSTICA DE PASAJEROS #####################
################################################################
def btn_pasajeros(update, context):
    query = update.callback_query
    query.answer()
    carpeta.append(3)
    keyboard = [[InlineKeyboardButton("Pasajeros anuales", callback_data=str(ANUAL)),
                 InlineKeyboardButton("Pasajeros mensuales", callback_data=str(MENSUAL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué periodicidad prefieres la información de pasajeros del SFM? \U0001F4C5:', reply_markup=reply_markup)
    return SECOND

##################### ESTADÍSTICA DE EQUIPO FERROVIARIO ##############
################################################################
def equipo(update, context):
    query = update.callback_query
    query.answer()
    carpeta.append(4)
    # se omite el estado SECOND, se asigna la frecuencia mensual  por defecto 
    frecuencia.append(10)
    keyboard = [[InlineKeyboardButton("Tablas", callback_data=str(TABLA)),
                 InlineKeyboardButton("Graficas", callback_data=str(GRAFICA)),
                 InlineKeyboardButton("Excel", callback_data=str(EXCEL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué formato prefieres la información del equipo ferroviario del SFM? \U0001F4C5:', reply_markup=reply_markup)   
    return THIRD


##################### ESTADÍSTICA DE CONSUMO ENERGÉTICO ##############
################################################################
def combustible(update, context):
    query = update.callback_query
    query.answer()
    carpeta.append(5)
    # se omite el estado SECOND, se asigna la frecuencia mensual  por defecto 
    frecuencia.append(10)
    keyboard = [[InlineKeyboardButton("Tablas", callback_data=str(TABLA)),
                 InlineKeyboardButton("Graficas", callback_data=str(GRAFICA)),
                 InlineKeyboardButton("Excel", callback_data=str(EXCEL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué formato prefieres la información del consumo energético del SFM? \U0001F4C5:', reply_markup=reply_markup)
    return THIRD

##################### ESTADÍSTICA DE PERSONAL ##############
################################################################
def personal(update, context):
    query = update.callback_query
    query.answer()
    carpeta.append(6)
    # se omite el estado SECOND, se asigna la frecuencia mensual  por defecto 
    frecuencia.append(10)
    keyboard = [[InlineKeyboardButton("Tablas", callback_data=str(TABLA)),
                 InlineKeyboardButton("Graficas", callback_data=str(GRAFICA)),
                 InlineKeyboardButton("Excel", callback_data=str(EXCEL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué formato prefieres la información del personal del SFM? \U0001F4C5:', reply_markup=reply_markup)
    return THIRD

##################### ESTADÍSTICA DE SINIESTROS #####################
################################################################
def siniestros(update, context):
    query = update.callback_query
    query.answer()
    carpeta.append(7)
    # se omite el estado SECOND, se asigna la frecuencia mensual  por defecto 
    frecuencia.append(10)
    keyboard = [[InlineKeyboardButton("Tablas", callback_data=str(TABLA)),
                 InlineKeyboardButton("Graficas", callback_data=str(GRAFICA)),
                 InlineKeyboardButton("Excel", callback_data=str(EXCEL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué formato prefieres la información de siniestros en el SFM? \U0001F4C5:', reply_markup=reply_markup)
    return THIRD

def robo(update, context):
    query = update.callback_query
    query.answer()
    carpeta.append(8)
    # se omite el estado SECOND, se asigna la frecuencia mensual  por defecto 
    frecuencia.append(10)
    keyboard = [[InlineKeyboardButton("Tablas", callback_data=str(TABLA)),
                 InlineKeyboardButton("Graficas", callback_data=str(GRAFICA)),
                 InlineKeyboardButton("Excel", callback_data=str(EXCEL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué formato prefieres la información de robo en el SFM? \U0001F4C5:', reply_markup=reply_markup)
    return THIRD

def vandalismo(update, context):
    query = update.callback_query
    query.answer()
    carpeta.append(9)
    # se omite el estado SECOND, se asigna la frecuencia mensual  por defecto 
    frecuencia.append(10)
    keyboard = [[InlineKeyboardButton("Tablas", callback_data=str(TABLA)),
                 InlineKeyboardButton("Graficas", callback_data=str(GRAFICA)),
                 InlineKeyboardButton("Excel", callback_data=str(EXCEL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué formato prefieres la información de vandalismo en el SFM? \U0001F4C5:', reply_markup=reply_markup)
    return THIRD

def bloqueos(update, context):
    query = update.callback_query
    query.answer()
    carpeta.append(10)
    # se omite el estado SECOND, se asigna la frecuencia mensual  por defecto 
    frecuencia.append(10)
    keyboard = [[InlineKeyboardButton("Tablas", callback_data=str(TABLA)),
                 InlineKeyboardButton("Graficas", callback_data=str(GRAFICA)),
                 InlineKeyboardButton("Excel", callback_data=str(EXCEL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué formato prefieres la información de bloqueos en el SFM? \U0001F4C5:', reply_markup=reply_markup)
    return THIRD

def desconocido(update: Update, context: CallbackContext):
    ''' Desconocido '''
    context.bot.send_message(update.message.chat_id, text="Disculpa, no entendí tu mensaje \U0001F641.")

##################### FUNCIONES PARA EL SEGUNDO ESTADO #####################
################################################################

def mensual(update, context):
    query = update.callback_query
    query.answer()
    # se asigna la frecuencia en 10 porque es el indice de MENSUAL en callback
    frecuencia.append(10)
    keyboard = [[InlineKeyboardButton("Tablas", callback_data=str(TABLA)),
                 InlineKeyboardButton("Graficas", callback_data=str(GRAFICA)),
                 InlineKeyboardButton("Excel", callback_data=str(EXCEL))]]
    # pasajeros no cuenta con graficas, quitamos la opcion del teclado
    if carpeta[0] == 2:
        keyboard[0].pop(1)
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué formato prefieres la información? \U0001F4C5:', reply_markup=reply_markup)
    return THIRD

def anual(update, context):
    query = update.callback_query
    query.answer()
    frecuencia.append(11)
    # Caso especial de carga anual 
    if carpeta[0] == 1: 
        graficas(update, context)
        return ConversationHandler.END

    keyboard = [[InlineKeyboardButton("Tablas", callback_data=str(TABLA)),
                 InlineKeyboardButton("Graficas", callback_data=str(GRAFICA)),
                 InlineKeyboardButton("Excel", callback_data=str(EXCEL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('¿Con qué formato prefieres la información? \U0001F4C5:', reply_markup=reply_markup)
    return THIRD


##################### FUNCIONES PARA EL SEGUNDO ESTADO #####################
################################################################
def graficas(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    # se genera el identificador para los diccionarios
    graficas = catalogo_graficas[str(carpeta[0]) + str(frecuencia[0])]
    mensaje = mensajes[str(carpeta[0]) + str(frecuencia[0])]
    query.edit_message_text(
        text=mensaje[1]
    )
    # se asignan el valor de valores de “img”  para obtener la ruta con con el método loc del dataFrame “datos”
    for img in graficas:
        imgpath =  s3Buncket + datos.loc[str(carpeta[0]) + '_' + img]["ruta"]
        context.bot.sendPhoto(chat_id, photo=imgpath)
    frecuencia.clear()
    carpeta.clear()
    # la función “registrar” almacena la hora, id del mensaje que provienen del objeto update  y el tipo de consulta que se realizó en tablas de DynamoDB
    registrar(update.callback_query, mensaje[0])
    
    return ConversationHandler.END

def tablas(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    # con la frecuencia y catalogo se genera el identificador para los diccionarios
    tablas = catalogo_tablas[str(carpeta[0]) + str(frecuencia[0])]
    mensaje = mensajes[str(carpeta[0]) + str(frecuencia[0])]
    query.edit_message_text(
        text=mensaje[1]
    )
    # para el caso de “doc” datos.loc regresa una lista porque encuentra dos coincidencias el elemento [0] tiene terminación .xlsx el elemento [1] tiene terminación .png
    for doc in tablas:
        docpath =  s3Buncket + datos.loc[str(carpeta[0]) + '_' + doc]["ruta"][0]
        context.bot.sendPhoto(chat_id, photo=docpath)
    frecuencia.clear()
    carpeta.clear()
    # la función “registrar” almacena la hora, id del mensaje que provienen del objeto update  y el tipo de consulta que se realizó en tablas de DynamoDB
    registrar(update.callback_query, mensaje[0])
    return ConversationHandler.END


def excel(update, context):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    # con la frecuencia y catalogo se genera el identificador para los diccionarios
    excel = catalogo_tablas[str(carpeta[0]) + str(frecuencia[0])]
    mensaje = mensajes[str(carpeta[0]) + str(frecuencia[0])]
    query.edit_message_text(
        text=mensaje[1]
    )
    # para el caso de “doc” datos.loc regresa una lista porque encuentra dos coincidencias el elemento [0] tiene terminación .xlsx el elemento [1] tiene terminación .png
    # para poder implementar el método sendDocument de bot es necesario pasarle cómo argumento come tipo _UrlopenRet 
    for doc in excel:
        tabpath =  s3Buncket + datos.loc[str(carpeta[0]) + '_' + doc]["ruta"][1]
        tab = urllib.request.urlopen(tabpath)
        tab.name = doc + '.xlsx'
        context.bot.sendDocument(chat_id, document=tab)
    frecuencia.clear()
    carpeta.clear()
    # la función “registrar” almacena la hora, id del mensaje que provienen del objeto update  y el tipo de consulta que se realizó en tablas de DynamoDB
    registrar(update.callback_query, mensaje[0])
    return ConversationHandler.END