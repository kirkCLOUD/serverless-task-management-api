
# Serverless Task Management API

A serverless backend application built using Python, AWS Lambda, Amazon DynamoDB, and AWS IAM.

This project demonstrates how cloud services work together to build a serverless application that supports Create, Read, Update, and Delete (CRUD) operations.

The project was developed and tested locally using Floci, an AWS service emulator, to avoid deploying resources to a live AWS account during development.

## Project Objectives

- Build a serverless backend using AWS Lambda.
- Store task records using Amazon DynamoDB.
- Configure IAM roles and permissions.
- Implement CRUD operations using Python and Boto3.
- Test AWS service integrations in a local environment.

## Key Features

- Create new tasks.
- Retrieve existing tasks.
- Update task information and status.
- Delete tasks.
- Generate unique task identifiers.
- Restrict Lambda access through IAM permissions.

## Technology Stack

- Python 3.12
- AWS Lambda
- Amazon DynamoDB
- AWS IAM
- Boto3
- Floci
- Docker Desktop
- Visual Studio Code
---

## Project Architecture

The application follows a serverless architecture:

```text
Test Client
    |
    v
AWS Lambda
    |
    v
Amazon DynamoDB
```

Floci provides the local AWS-compatible environment used to deploy and test the services.

## Database

**DynamoDB Table:** `Tasks`

**Partition Key:** `task_id` (String)

Task attributes include:

- task_id
- title
- description
- status
- priority
- created_at

## Lambda Configuration

| Setting | Value |
|---|---|
| Function Name | TaskManagementFunction |
| Runtime | Python 3.12 |
| Handler | lambda_function.lambda_handler |
| Memory | 128 MB |
| Timeout | 30 seconds |

## IAM Security

The Lambda function uses an execution role named `TaskManagementLambdaRole`.

The role grants the function the following DynamoDB permissions:

- dynamodb:GetItem
- dynamodb:PutItem
- dynamodb:UpdateItem
- dynamodb:DeleteItem
- dynamodb:Scan

Permissions are scoped to the project's Tasks table in the local emulator.

## Testing Results

The Lambda function was tested using Python and Boto3.

| Operation | HTTP Method | Result |
|---|---|---|
| Create Task | POST | Passed |
| Retrieve Task | GET | Passed |
| Update Task | PUT | Passed |
| Delete Task | DELETE | Passed |

**Result:** All four CRUD operations passed in the local testing environment.

## Documentation

Detailed project documentation:

- [System Architecture](docs/architecture.md)
- [Database Design and IAM Security](docs/database-and-security.md)
- [Deployment and Testing](docs/deployment-and-testing.md)

## Screenshots

Implementation screenshots are available in the `screenshots/` folder.

## Future Improvements

- Integrate Amazon API Gateway.
- Build a frontend application.
- Add authentication and authorization.
- Implement automated testing.
- Deploy to actual AWS infrastructure.
- Configure monitoring and logging.

## Deployment Note

This project was deployed and tested locally using Floci. It has not yet been deployed to a live AWS account.
