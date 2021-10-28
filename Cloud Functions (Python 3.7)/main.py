import json
import re

def handler(event, context):
    body = json.loads(event['body'])
    from dadata import Dadata
    token = "5dad8f1ed25f5eab510071fa3e88182afb06c817"
    dadata = Dadata(token)
    r = "^\d{6}$"

    if 'text' in body['message']:
        if re.match(r, body['message']['text']):
            result = dadata.suggest("postal_unit", body['message']['text'])
            result = str(str(result[0]['unrestricted_value']).encode('utf-8'), 'utf-8')
        else:
            result = "Индекс имеет неверный формат"
    elif 'location' in body['message']:
        location = body['message']['location']
        result = dadata.geolocate(name="postal_unit", lat=location['latitude'], lon=location['longitude'], radius_meters=1000)
        result = str(str(result[0]['unrestricted_value']).encode('utf-8'), 'utf-8')
    else:
        result = "Введите индекс или отправте геолокацию"
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': body['message']['chat']['id'],
            'text': result
        }),
        'isBase64Encoded': False
    }
