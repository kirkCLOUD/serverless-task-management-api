
# Database Design and IAM Security

## 1. Database Overview

The project uses Amazon DynamoDB as its NoSQL database.

**Table Name:** Tasks

**Partition Key:** task_id

**Key Type:** String

The table stores task information used by the Serverless Task Management API.

## 2. Task Data Structure

| Attribute | Description |
|---|---|
| task_id | Unique identifier for each task |
| title | Name or title of the task |
| description | Additional task details |
| status | Current state of the task |
| priority | Task priority level |
| created_at | Date and time the task was created |

### Example Task Record

```json
{
  "task_id": "task-001",
  "title": "Complete cloud project",
  "description": "Document the serverless application",
  "status": "pending",
  "priority": "high",
  "created_at": "2026-11-17T08:00:00"
}
```

## 3. IAM Security Configuration

AWS Identity and Access Management (IAM) controls which AWS resources the Lambda function can access.

**IAM Role:** TaskManagementLambdaRole

**Trusted Service:** AWS Lambda

The role allows the Lambda function to perform the following DynamoDB actions:

| Permission | Purpose |
|---|---|
| dynamodb:GetItem | Retrieve a specific task |
| dynamodb:PutItem | Create a task |
| dynamodb:UpdateItem | Modify an existing task |
| dynamodb:DeleteItem | Delete a task |
| dynamodb:Scan | Retrieve task records |

## 4. Resource-Level Permissions

The DynamoDB permissions are scoped to the following local emulator table ARN:

`arn:aws:dynamodb:us-east-1:000000000000:table/Tasks`

This demonstrates the principle of least privilege by limiting the role's database permissions to the project table rather than granting unrestricted DynamoDB access.

## 5. Security Considerations

- Use IAM roles instead of hardcoding credentials in application code.
- Grant only the permissions required by the Lambda function.
- Restrict resource access where possible.
- Review IAM policies before deploying to production.
- Protect AWS credentials and never commit real credentials to GitHub.

## 6. Deployment Environment

The IAM role and DynamoDB table were configured in the local Floci environment.

A production AWS deployment would require reviewing and configuring the corresponding permissions and resources in the actual AWS account.
