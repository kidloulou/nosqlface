import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_table():
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    return dynamodb.Table('Users')

def save_user(user_data):
    table = get_db_table()
    table.put_item(Item=user_data)

def fetch_user(email):
    table = get_db_table()
    response = table.get_item(Key={'email': email})
    return response.get('Item')
