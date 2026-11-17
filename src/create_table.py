
import boto3

# Connect to local Floci DynamoDB
dynamodb = boto3.client(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

TABLE_NAME = "Tasks"

def create_tasks_table():
    existing_tables = dynamodb.list_tables()["TableNames"]

    if TABLE_NAME in existing_tables:
        print(f"{TABLE_NAME} already exists.")
        return

    dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                "AttributeName": "task_id",
                "KeyType": "HASH"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "task_id",
                "AttributeType": "S"
            }
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    print(f"{TABLE_NAME} created successfully!")

    dynamodb.get_waiter("table_exists").wait(
        TableName=TABLE_NAME
    )

    response = dynamodb.describe_table(
        TableName=TABLE_NAME
    )

    print("Table status:", response["Table"]["TableStatus"])
    print("Partition key: task_id")


if __name__ == "__main__":
    create_tasks_table()
