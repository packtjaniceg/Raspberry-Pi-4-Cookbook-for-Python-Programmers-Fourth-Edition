#!/usr/bin/python3
''' aws_send_adc.py '''
import time
import datetime
import boto3
import data_adc as dataDevice

TABLE_NAME = 'RaspberryPiData'
DATA_SOURCE = 'Location-A'
DEBUG = True
SAMPLE_PERIOD = 10 # seconds between samples

def get_header(data_names):
    ''' Create formated data header '''
    header = f"{'ID':6}\t{'Time':{len(timestamp(time.time()))}}"
    for name in data_names:
        header += f"\t{name}"
    return header

def get_body(counter, now, data_names, data_values):
    ''' Create formated data body '''
    time_str = timestamp(now)
    body = f"{counter:<6}\t{time_str:{len(time_str)}}"
    for i, name in enumerate(data_names):
        body += f"\t{data_values[i]:{len(name)}}"
    return body

def timestamp(now):
    ''' generate timestamp '''
    return datetime.datetime.fromtimestamp(now).strftime(
        '%Y-%m-%d %H:%M:%S')

def capture_samples(client):
    ''' Capture new samples and send to aws '''
    my_data = dataDevice.Device()
    my_data_names = my_data.get_name()
    if DEBUG:
        print(get_header(my_data_names))
    for count in range(10):
        now = time.time()
        data = my_data.get_new()
        record = {}
        record['data_source'] = {
            'S': DATA_SOURCE
        }
        record['data_ts'] = {
            'N': str(int(now*1000)) #ms epoch
        }
        for i, data_name in enumerate(my_data_names):
            record[data_name] = {
                'N': str(data[i])
            }
        put_data(client, record)
        if DEBUG:
            print(get_body(count, now, my_data_names, data))
        while time.time() <= now+SAMPLE_PERIOD:
            time.sleep(0.1)


def create_table(client, table_name):
    ''' Create a new dynamoDb table if required '''
    try:
        client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'data_source',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'data_ts',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'data_source',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'data_ts',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Wait for table to be created
        client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
        print(f"Table {TABLE_NAME} created")
    except client.exceptions.ResourceInUseException:
        print(f"Table exists - skip create")

def put_data(client, record):
    ''' Send item to AWS dynamoDb '''
    response = client.put_item(
        TableName=TABLE_NAME,
        Item=record
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        print(f"Item {record} Stored")
    else:
        print(f"{response['ResponseMetadata']['HTTPStatusCode']}" +
              f"- Item {record} Store FAILED")

if __name__ == '__main__':
    try:
        DYNAMODB = boto3.client('dynamodb')
        create_table(DYNAMODB, TABLE_NAME)
        capture_samples(DYNAMODB)

    except KeyboardInterrupt:
        print("END")
#End
