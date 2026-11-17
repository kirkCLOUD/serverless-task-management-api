
import json
import os
import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError

# DynamoDB connection
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=os.environ.get(
        "DYNAMODB_ENDPOINT",
        "http://host.docker.internal:4566"
    ),
    region_name=os.environ.get("AWS_REGION", "us-east-1")
)

table = dynamodb.Table("Tasks")


def response(status_code, body):
    """Format HTTP response for API Gateway."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    """Main Lambda entry point."""

    try:
        method = event.get("httpMethod") or event.get(
            "requestContext", {}
        ).get("http", {}).get("method", "")

        path_parameters = event.get("pathParameters") or {}
        task_id = path_parameters.get("id")

        # CREATE TASK
        if method == "POST":
            body = event.get("body") or "{}"

            if isinstance(body, str):
                body = json.loads(body)

            if not body.get("title"):
                return response(400, {
                    "error": "Task title is required"
                })

            task_id = body.get("task_id")

            if not task_id:
                from uuid import uuid4
                task_id = str(uuid4())

            task = {
                "task_id": task_id,
                "title": body["title"],
                "description": body.get("description", ""),
                "status": "pending",
                "priority": body.get("priority", "medium"),
                "created_at": datetime.now(
                    timezone.utc
                ).isoformat()
            }

            table.put_item(
                Item=task,
                ConditionExpression="attribute_not_exists(task_id)"
            )

            return response(201, {
                "message": "Task created successfully",
                "task": task
            })

        # READ TASKS
        elif method == "GET":

            if task_id:
                result = table.get_item(
                    Key={"task_id": task_id}
                )

                task = result.get("Item")

                if not task:
                    return response(404, {
                        "error": "Task not found"
                    })

                return response(200, task)

            result = table.scan()

            return response(200, {
                "tasks": result.get("Items", [])
            })

        # UPDATE TASK
        elif method == "PUT":

            if not task_id:
                return response(400, {
                    "error": "Task ID is required"
                })

            body = event.get("body") or "{}"

            if isinstance(body, str):
                body = json.loads(body)

            allowed_fields = {
                "title", "description", "status", "priority"
            }

            updates = {
                key: value
                for key, value in body.items()
                if key in allowed_fields
            }

            if not updates:
                return response(400, {
                    "error": "No valid fields provided"
                })

            expression_names = {}
            expression_values = {}
            update_parts = []

            for index, (key, value) in enumerate(updates.items()):
                name = f"#field{index}"
                placeholder = f":value{index}"

                expression_names[name] = key
                expression_values[placeholder] = value

                update_parts.append(
                    f"{name} = {placeholder}"
                )

            result = table.update_item(
                Key={"task_id": task_id},
                UpdateExpression="SET " + ", ".join(update_parts),
                ExpressionAttributeNames=expression_names,
                ExpressionAttributeValues=expression_values,
                ConditionExpression="attribute_exists(task_id)",
                ReturnValues="ALL_NEW"
            )

            return response(200, {
                "message": "Task updated successfully",
                "task": result["Attributes"]
            })

        # DELETE TASK
        elif method == "DELETE":

            if not task_id:
                return response(400, {
                    "error": "Task ID is required"
                })

            result = table.delete_item(
                Key={"task_id": task_id},
                ConditionExpression="attribute_exists(task_id)",
                ReturnValues="ALL_OLD"
            )

            return response(200, {
                "message": "Task deleted successfully",
                "task": result.get("Attributes")
            })

        else:
            return response(405, {
                "error": "Method not allowed"
            })

    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        if error_code == "ConditionalCheckFailedException":
            return response(404, {
                "error": "Task not found or already exists"
            })

        print("DynamoDB error:", error)
        return response(500, {
            "error": "Database operation failed"
        })

    except (ValueError, json.JSONDecodeError):
        return response(400, {
            "error": "Invalid JSON request body"
        })

    except Exception as error:
        print("Unexpected error:", error)
        return response(500, {
            "error": "Internal server error"
        })
