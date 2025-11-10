# Используем официальный базовый образ AWS Lambda для Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Копируем файл с зависимостями
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код Lambda функции
COPY app.py ${LAMBDA_TASK_ROOT}

# Указываем handler для Lambda
CMD [ "app.lambda_handler" ]
