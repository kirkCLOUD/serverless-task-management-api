
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
