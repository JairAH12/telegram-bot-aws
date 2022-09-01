"""Este módulo se encarga de hacer las conexiones a la tablas de DynamoDB

AWS provee el SDK boto3 con este se puede interactuar con las tablas de DynamoDB de varias maneras, 
en este módulo se interactúa con DynamoDB con los objetos de tipo “client” y “table”, de esta manera 
se ejemplifican algunas de las diferencias en la sintaxis   

Funciones disponibles:
registrar: Registra un nuevo ítem en la tabla registros 
actualizarCotador: Actualiza el número de consultas 
consultarContador: Obtiene el último valor de la variable relacionada al número de consultas

"""
import boto3

tableName = "registros"
dynamodbClient = boto3.client('dynamodb')

tableCount = "counters"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tableCount)




def registrar(updateCQ, consulta):
    """Registra un nuevo ítem en la tabla registros 

    Esta función utiliza la función actualizarContador para consultar e incrementar la el registro 
    currentValue de la clave importantCounter

    Args:
        - updateQC (update.callback_query): Objeto que proporciona la librería de telegram y contiene los atributos que se registran en la tabla registros	
        - consulta (string): es el nombre de la consulta que realizó el usuario
    """
    numeroConsulta = actualizarContador()
    # Se crea una dicionario con los elementos atributos del objeto Update 
    # Para poder usar el método put_item de table en necesario castear los elementos de Update a  tipo string.
    nuevoRegistro = {
    'consulta' : {'S':consulta},
    'fecha' : {'S': str(updateCQ.message.date)},
    'idMensaje': {'S':str(updateCQ.message.message_id)},
    'usuario': {'S':updateCQ.message.chat.first_name +' ' + updateCQ.message.chat.last_name},
    'numeroConsulta': {'N': str(numeroConsulta)},
    'idUsuario': {'S':str(updateCQ.message.chat.id)} 
    }

    dynamodbClient.put_item(TableName = tableName, Item = nuevoRegistro )


def actualizarContador():
    """Actualiza el único elemento de la tabla counters con el número actual de consultas

    Returns: 
        Decimal: Valor actual del número de consultas
    """
    
    # response es un diccionario que contiene un elemento Item sí get_item encuentra una coincidencia con la clave proporcionada
    response = table.get_item(
    Key={'counterName':'importantCounter'}
    )
    # Se verifica que exista un elemento con la clave proporcionada
    # si existe un elemento Item en el diccionario response actualiza ese registro
    if 'Item' in response:
        update = table.update_item(
            ReturnValues= "UPDATED_NEW",
            ExpressionAttributeValues= {
                ":a": 1
            },
            ExpressionAttributeNames= {
                "#v": "currentValue"
            },
            UpdateExpression= "SET #v = #v + :a",
            Key= {
                "counterName": "importantCounter"
            }
        )
        return update['Attributes']['currentValue']
    else:
        # si no existe, se agrega
        table.put_item(Item= {'counterName': 'importantCounter', 'currentValue':1})
        return 1 

def consultarContador():
    """
    Hace una consulta a la tabla counters para traer el valor del número de consultas
    """
    response = table.get_item(
    Key={'counterName':'importantCounter'}
    )
    if 'Item' in response:
        return response['Item']['currentValue']
    else:
        return 0 