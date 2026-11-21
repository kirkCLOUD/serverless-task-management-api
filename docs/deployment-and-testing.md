
# Deployment and Testing

## 1. Local Development Environment

The project was developed and tested using a local AWS-compatible environment.

| Tool | Purpose |
|---|---|
| Docker Desktop | Runs the Floci environment |
| Floci | Emulates AWS services locally |
| Python | Runs the project scripts |
| Boto3 | Communicates with AWS-compatible services |
| Visual Studio Code | Development environment |

**Floci endpoint:**

`http://localhost:4566`

## 2. Deployment Process

The following steps were performed to configure the project.

### Step 1: Start Floci

Start Docker Desktop and verify that the Floci container is running.

### Step 2: Create the DynamoDB Table

Run:

```powershell
python .\src\create_table.py
```

This creates the `Tasks` table with `task_id` as its partition key.

### Step 3: Configure the IAM Role

Run:

```powershell
python .\src\setup_iam.py
```

This creates the `TaskManagementLambdaRole` execution role and configures DynamoDB permissions.

### Step 4: Deploy the Lambda Function

Run:

```powershell
python .\src\deploy_lambda.py
```

This packages and deploys the `TaskManagementFunction` Lambda function.

## 3. Testing Process

The Lambda function was tested using the following command:

```powershell
python .\src\test_lambda.py
```

The test script invokes the Lambda function with different events to simulate task management operations.

## 4. CRUD Test Results

| HTTP Method | Operation | Expected Status | Result |
|---|---|---|---|
| POST | Create task | 201 | Passed |
| GET | Retrieve task | 200 | Passed |
| PUT | Update task | 200 | Passed |
| DELETE | Delete task | 200 | Passed |

**Overall Result:** All four CRUD tests passed successfully.

## 5. Test Evidence

Screenshots are stored in the project's `screenshots/` directory.

| Screenshot | Evidence |
|---|---|
| 01 | DynamoDB table created |
| 02 | Task inserted |
| 03 | Task updated |
| 04 | Task deleted |
| 05 | Floci environment running |
| 06 | Lambda handler code |
| 07 | IAM execution role |
| 08 | Lambda deployment |
| 09 | Lambda invocation |
| 10 | CRUD test results |

## 6. Deployment Limitations

This deployment was performed locally using Floci.

The project has not yet been deployed to a live AWS account. Production deployment would require configuring the actual AWS resources, permissions, networking, monitoring, and cost controls.
