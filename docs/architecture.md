
# System Architecture

## Overview

The Serverless Task Management API uses a serverless architecture in which AWS Lambda handles application logic and Amazon DynamoDB stores task information.

The services were deployed and tested locally using Floci.

## Architecture Flow

```text
              Test Client
                  |
                  | Lambda Invoke
                  v
          AWS Lambda Function
          TaskManagementFunction
                  |
                  | Boto3
                  v
            Amazon DynamoDB
               Tasks Table
```

## Components

### 1. AWS Lambda

AWS Lambda executes the Python backend code without requiring a continuously running server.

The function processes incoming events and performs the requested task operation.

### 2. Amazon DynamoDB

DynamoDB is the NoSQL database used to store task records.

The table is named `Tasks`, with `task_id` as its partition key.

### 3. AWS IAM

IAM controls the permissions assigned to the Lambda execution role.

The role `TaskManagementLambdaRole` grants the function access to the required DynamoDB operations.

### 4. Boto3

Boto3 is the AWS SDK for Python. It allows the Python scripts and Lambda function to communicate with AWS-compatible services.

### 5. Floci

Floci provides a local AWS-compatible environment for development and testing.

The local endpoint is:

`http://localhost:4566`

The Lambda container connects to the local endpoint using:

`http://host.docker.internal:4566`

## Request Processing

1. The test client sends an invocation event to Lambda.
2. Lambda identifies the requested HTTP operation.
3. The function processes the request using Python and Boto3.
4. DynamoDB performs the requested database operation.
5. Lambda returns a response containing the operation result.

## Architecture Scope

The current implementation invokes Lambda directly through the local emulator.

Amazon API Gateway and a frontend application are not yet integrated.
