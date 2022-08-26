import json
import boto3

TABLE_NAME='my-table'
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    item = table.get_item(Key={
        'MyPrimaryKey': 'Number of Hits'
    })
    
    try:
        count = item['Item']['Count'] + 1
    except KeyError as e:
        print('Count key not found, so assuming it is the first hit')
        count = 1
    
    res = table.put_item(Item={'MyPrimaryKey': 'Number of Hits', 'AnalyticsValue': count})
    res["Count"] = str(count)

    return {
        'statusCode': res["ResponseMetadata"]["HTTPStatusCode"],
        # I needed to pass the headers like this as this is a lambda proxy integration with API gateway.
        # This headers gets passed directly to the client and without it - I get cors issue.
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'count': str(count)})
    }
