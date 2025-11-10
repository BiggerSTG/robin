import boto3
from config import settings
import os


# Load the environment variables for AWS credentials
os.environ['AWS_ACCESS_KEY_ID'] = settings.AWS_ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = settings.AWS_SECRET_ACCESS_KEY


# Create connection to DynamoDB
dynamodb = boto3.resource('dynamodb')


# Create User Table
user_table = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
user_table.wait_until_exists()


# Create Quiz Table
quiz_table = dynamodb.create_table(
    TableName='quizzes',
    KeySchema=[
        {
            'AttributeName': 'quiz_id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'username',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'quiz_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
quiz_table.wait_until_exists()


# Example: Insert a user
user_table.put_item(
    Item={
        'username': 'johndoe',
        'last_name': 'Doe',
        'hashed_password': 'hashedpassword',  # Replace with actual hash
        'email': 'johndoe@example.com',
        'created_at': '2025-06-08T10:00:00Z'
    }
)


# Example: Insert a quiz result
quiz_table.put_item(
    Item={
        'quiz_id': 'quiz-001',
        'username': 'johndoe',
        'quiz_name': 'Math Quiz',
        'score': 85,
        'timestamp': '2025-06-08T11:00:00Z',
        'answers': {
            'q1': 'A',
            'q2': 'C'
        }
    }
)