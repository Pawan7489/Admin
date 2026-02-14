# File: aws_lambda/lambda_function.py
# Purpose: Serverless micro-task execution.
# Logic: "Musk Rule" - Execute fast, shut down immediately.

import json

def lambda_handler(event, context):
    """
    Indore se Bhopal mesh ke liye chote tasks handle karta hai.
    """
    # Task identity nikalna
    task_type = event.get('task_type', 'ping')
    payload = event.get('payload', {})

    print(f"⚡ [AWS Lambda]: Executing task -> {task_type}")

    if task_type == 'calculate_tokens':
        # Example: Token counting for cost control
        text = payload.get('text', '')
        token_count = len(text.split()) # Simplified logic
        return {
            'statusCode': 200,
            'body': json.dumps({'tokens': token_count})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'A1 Serverless Node is Online'})
    }
  
