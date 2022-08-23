import boto3

tableName = "registros"
dynamodbClient = boto3.client('dynamodb')

tableCount = "counters"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tableCount)

tableCount2 = "registros"
dynamodb2 = boto3.resource('dynamodb')
table2 = dynamodb2.Table(tableCount2)



def registrar(updateCQ, consulta):

    numeroConsulta = actualizarContador()
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
    response = table.get_item(
    Key={'counterName':'importantCounter'}
    )
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
        table.put_item(Item= {'counterName': 'importantCounter', 'currentValue':1})
        return 1 

def consultarContador():
    response = table.get_item(
    Key={'counterName':'importantCounter'}
    )
    if 'Item' in response:
        return response['Item']['currentValue']
    else:
        return 0 