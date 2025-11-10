import json
import os
import boto3
from datetime import datetime

# Инициализация boto3 клиента (пример с S3)
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Lambda handler функция

    Args:
        event: Событие, которое запустило Lambda
        context: Контекст выполнения Lambda

    Returns:
        dict: Ответ с status code и body
    """

    # Получаем переменные окружения
    log_level = os.environ.get('LOG_LEVEL', 'INFO')

    # Получаем информацию о регионе
    region = os.environ.get('AWS_REGION', 'us-east-1')

    # Пример использования boto3 - получаем список S3 buckets
    try:
        # Раскомментируйте следующие строки, если хотите реально обращаться к S3
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        # buckets = ["Пример работы с boto3 - закомментировано для безопасности"]
    except Exception as e:
        buckets = [f"Ошибка при получении списка buckets: {str(e)}"]

    # Формируем ответ
    response_body = {
        'message': 'Hello from Lambda with Docker!',
        'timestamp': datetime.now().isoformat(),
        'region': region,
        'log_level': log_level,
        'python_version': '3.11',
        'boto3_example': buckets,
        'event': event
    }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(response_body, ensure_ascii=False, indent=2)
    }
