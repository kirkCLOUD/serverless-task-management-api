
import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

table = dynamodb.Table("Tasks")

response = table.update_item(
    Key={"task_id": "task-001"},
    UpdateExpression="SET #s = :status",
    ExpressionAttributeNames={
        "#s": "status"
    },
    ExpressionAttributeValues={
        ":status": "in_progress"
    },
    ReturnValues="ALL_NEW"
)

print("Task updated successfully!")
print("Updated task:", response["Attributes"])

