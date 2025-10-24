# AWS Bedrock Poem Generator

A serverless application that generates Shakespearean-style poems using AWS Bedrock and Mistral AI models.

## Project Structure

- **`mistral.py`** - Direct use of AWS Bedrock API for poem generation
- **`main.py`** - AWS Lambda function code that connects to AWS API Gateway and S3 bucket

## Features

- Generates poems in Shakespearean style using Mistral Pixtral Large model
- Serverless architecture with AWS Lambda
- Stores generated poems in Amazon S3
- Accesses via AWS API Gateway

## Prerequisites

- Python 3.11+
- AWS Account with Bedrock access
- AWS credentials configured

## Installation

```bash
uv sync
```

## Usage

### Test Bedrock API directly:
```bash
uv run mistral.py
```

### Deploy Lambda Function:
Deploy `main.py` as an AWS Lambda function connected to API Gateway and S3.

## Configuration

Update the model ID and S3 bucket name in the respective files with your AWS resource ARNs.
