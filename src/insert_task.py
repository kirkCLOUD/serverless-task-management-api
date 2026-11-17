
import boto3
from datetime import datetime, timezone

# Connect to local DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# Connect to our Tasks table
table = dynamodb.Table("Tasks")

# Define our task
task = {
    "task_id": "task-001",
    "title": "Complete AWS Project 2",
    "description": "Build a serverless task management API",
    "status": "pending",
    "priority": "high",
    "created_at": datetime.now(timezone.utc).isoformat()
}

# Insert task into DynamoDB
table.put_item(Item=task)

print("Task inserted successfully!")

# Retrieve the inserted task
response = table.get_item(
    Key={"task_id": "task-001"}
)

print("\nRetrieved task:")
print(response.get("Item"))
