from fastapi import FastAPI
import boto3
import os
from dotenv import load_dotenv

load_dotenv()


dynamodb = boto3.resource(
    "dynamodb", 
    region_name=os.getenv('DB_REGION_NAME'), 
    aws_access_key_id=os.getenv('DB_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('DB_SECRET_ACCESS_KEY')
    ) 

app = FastAPI()

@app.get('/')
def root():
    table = dynamodb.Table('Recipe')
    # response = table.get_item(
    #     Key = {"name": "Ramen"}
    # )

    # return response["Item"]