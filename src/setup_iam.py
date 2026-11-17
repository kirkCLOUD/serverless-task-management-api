
import boto3
import json

ENDPOINT = "http://localhost:4566"
ROLE_NAME = "TaskManagementLambdaRole"

iam = boto3.client(
    "iam",
    endpoint_url=ENDPOINT,
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# Trust policy: allow Lambda service to assume this role
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

# Create or retrieve the execution role
try:
    role = iam.get_role(RoleName=ROLE_NAME)["Role"]
    print("IAM role already exists.")

except iam.exceptions.NoSuchEntityException:
    role = iam.create_role(
        RoleName=ROLE_NAME,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description="Execution role for Task Management Lambda"
    )["Role"]

    print("IAM execution role created.")

# Restrict DynamoDB access to our Tasks table
table_arn = (
    "arn:aws:dynamodb:us-east-1:000000000000:table/Tasks"
)

policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem",
                "dynamodb:Scan"
            ],
            "Resource": table_arn
        }
    ]
}

iam.put_role_policy(
    RoleName=ROLE_NAME,
    PolicyName="TasksTableAccess",
    PolicyDocument=json.dumps(policy)
)

print("DynamoDB permissions configured.")
print("Role ARN:", role["Arn"])
