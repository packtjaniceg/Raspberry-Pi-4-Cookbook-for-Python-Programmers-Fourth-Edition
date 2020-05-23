#!/usr/bin/python3
''' aws_read_data.py '''
import time
import datetime
from pprint import pprint
import boto3

TABLE_NAME = 'RaspberryPiData'
DATA_SOURCE = 'Location-A'
LAST_MIN = 60
LAST_HOUR = LAST_MIN*60
LAST_DAY = LAST_HOUR*24

def timestamp(now):
    ''' generate timestamp '''
    return datetime.datetime.fromtimestamp(now).strftime(
        '%Y-%m-%d %H:%M:%S')

def query_data(client, from_time, to_time=int(time.time())):
    ''' Query table between given times '''
    print(f"Get items from {timestamp(from_time)} to {timestamp(to_time)}")
    key_exp = 'data_source = :data_source AND ' + \
              'data_ts BETWEEN :from_time AND :to_time'
    response = client.query(
        TableName=TABLE_NAME,
        KeyConditionExpression=key_exp,
        ExpressionAttributeValues={
            ':data_source': {'S': DATA_SOURCE},
            ':from_time': {'N': str(from_time*1000)},
            ':to_time': {'N': str(to_time*1000)}
        }
    )
    return response["Items"]

def scan_data(client, from_time, to_time=int(time.time())):
    ''' Scan items and filter between given times '''
    print(f"Scan and filter items from {timestamp(from_time)}" +
           " to {timestamp(to_time)}")
    fltr_exp = 'data_source = :data_source AND ' + \
               'data_ts BETWEEN :from_time AND :to_time'
    response = client.scan(
        TableName=TABLE_NAME,
        FilterExpression=fltr_exp,
        ExpressionAttributeValues={
            ':data_source': {'S': DATA_SOURCE},
            ':from_time': {'N': str(from_time*1000)},
            ':to_time': {'N': str(to_time*1000)}
        })
    return response["Items"]

if __name__ == '__main__':
    DYNAMODB = boto3.client('dynamodb')

    print(f">> Query data from LAST_HOUR in {TABLE_NAME}")
    TIME_FROM = int(time.time()-LAST_HOUR)
    RESULT = query_data(DYNAMODB, TIME_FROM)
    pprint(RESULT)
    print(f"{len(RESULT)} items returned")

    print(f">> Scan data from {TABLE_NAME} in LAST_HOUR")
    RESULT = scan_data(DYNAMODB, TIME_FROM)
    pprint(RESULT)
    print(f"{len(RESULT)} items returned")
#End
