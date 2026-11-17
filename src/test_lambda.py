
import boto3
import json
import uuid

# Connect to local Lambda
lambda_client = boto3.client(
    "lambda",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

FUNCTION_NAME = "TaskManagementFunction"


def invoke_lambda(method, path, body=None, path_parameters=None):
    """Invoke Lambda using an API Gateway-compatible event."""

    event = {
        "version": "2.0",
        "rawPath": path,
        "requestContext": {
            "http": {
                "method": method
            }
        },
        "pathParameters": path_parameters or {},
        "body": json.dumps(body) if body is not None else None,
        "isBase64Encoded": False
    }

    result = lambda_client.invoke(
        FunctionName=FUNCTION_NAME,
        InvocationType="RequestResponse",
        Payload=json.dumps(event)
    )

    payload = json.loads(result["Payload"].read())

    print(f"\n{method} {path}")
    print("Lambda status:", result["StatusCode"])
    print("Response:", json.dumps(payload, indent=2))

    if "FunctionError" in result:
        raise RuntimeError(
            f"Lambda execution failed: {payload}"
        )

    return payload


# Generate a unique task ID for testing
task_id = "test-" + str(uuid.uuid4())[:8]

# 1. CREATE
create_result = invoke_lambda(
    "POST",
    "/tasks",
    {
        "task_id": task_id,
        "title": "Test Lambda deployment",
        "description": "Testing local serverless API",
        "priority": "high"
    }
)

assert create_result["statusCode"] == 201

# 2. READ
read_result = invoke_lambda(
    "GET",
    f"/tasks/{task_id}",
    path_parameters={"id": task_id}
)

assert read_result["statusCode"] == 200

# 3. UPDATE
update_result = invoke_lambda(
    "PUT",
    f"/tasks/{task_id}",
    {
        "status": "completed"
    },
    path_parameters={"id": task_id}
)

assert update_result["statusCode"] == 200

# 4. DELETE
delete_result = invoke_lambda(
    "DELETE",
    f"/tasks/{task_id}",
    path_parameters={"id": task_id}
)

assert delete_result["statusCode"] == 200

print("\nALL FOUR LAMBDA CRUD TESTS PASSED!")
