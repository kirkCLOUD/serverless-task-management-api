
import boto3

# Connect to local DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

table = dynamodb.Table("Tasks")

# Delete the task
response = table.delete_item(
    Key={"task_id": "task-001"},
    ReturnValues="ALL_OLD"
)

print("Task deleted successfully!")

print("Deleted task:", response.get("Attributes"))
