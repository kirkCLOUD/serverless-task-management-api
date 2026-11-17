
import boto3
import zipfile
import io

ENDPOINT = "http://localhost:4566"
FUNCTION_NAME = "TaskManagementFunction"
ROLE_NAME = "TaskManagementLambdaRole"

# Connect to local IAM
iam = boto3.client(
    "iam",
    endpoint_url=ENDPOINT,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# Connect to local Lambda
lambda_client = boto3.client(
    "lambda",
    endpoint_url=ENDPOINT,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# Retrieve IAM execution role
role = iam.get_role(RoleName=ROLE_NAME)["Role"]
role_arn = role["Arn"]

print("IAM role retrieved:", role_arn)

# Package Lambda function
zip_buffer = io.BytesIO()

with zipfile.ZipFile(zip_buffer, "w") as zip_file:
    zip_file.write(
        "lambda/lambda_function.py",
        arcname="lambda_function.py"
    )

zip_buffer.seek(0)
deployment_package = zip_buffer.read()

print("Lambda package created successfully.")

# Deploy Lambda
try:
    result = lambda_client.create_function(
        FunctionName=FUNCTION_NAME,
        Runtime="python3.12",
        Role=role_arn,
        Handler="lambda_function.lambda_handler",
        Code={"ZipFile": deployment_package},
        Timeout=30,
        MemorySize=128,
        Environment={
            "Variables": {
                "DYNAMODB_ENDPOINT": "http://host.docker.internal:4566",
                "AWS_REGION": "us-east-1"
            }
        },
        Publish=True
    )

    print("Lambda function created successfully!")

except lambda_client.exceptions.ResourceConflictException:
    print("Function already exists. Updating code...")

    result = lambda_client.update_function_code(
        FunctionName=FUNCTION_NAME,
        ZipFile=deployment_package,
        Publish=True
    )

    print("Lambda code updated successfully!")

print("Function name:", FUNCTION_NAME)
print("Function ARN:", result["FunctionArn"])
print("Runtime:", "Python 3.12")
