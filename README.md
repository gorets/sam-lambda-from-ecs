# SAM Lambda с Docker образом из ECR

Пример SAM Template для развертывания AWS Lambda функции на Python 3.11 с использованием Docker образа из ECR.

## Структура проекта

```
.
├── template.yaml      # SAM шаблон
├── Dockerfile        # Dockerfile для Lambda
├── app.py           # Python код Lambda функции
└── requirements.txt # Зависимости Python (boto3)
```

## Требования

- AWS CLI
- SAM CLI
- Docker
- Python 3.11

## Установка SAM CLI

```bash
# macOS
brew install aws-sam-cli

# Linux
pip install aws-sam-cli

# Windows
choco install aws-sam-cli
```

## Локальное тестирование

### 1. Собрать образ локально

```bash
sam build
```

### 2. Запустить локально

```bash
sam local start-api
```

Теперь можно обратиться к функции:
```bash
curl http://localhost:3000/hello
```

### 3. Вызвать функцию напрямую

```bash
sam local invoke MyLambdaFunction
```

## Развертывание в AWS

### 1. Первое развертывание

```bash
sam deploy --guided
```

Вам будут заданы вопросы:
- Stack Name: `sam-lambda-ecr-example`
- AWS Region: `us-east-1` (или ваш регион)
- Confirm changes before deploy: `Y`
- Allow SAM CLI IAM role creation: `Y`
- MyLambdaFunction may not have authorization defined, Is this okay?: `Y`
- Save arguments to configuration file: `Y`

### 2. Последующие развертывания

```bash
sam build && sam deploy
```

### 3. Использование существующего ECR репозитория

Если у вас уже есть Docker образ в ECR, можно использовать его напрямую:

```bash
sam deploy --guided \
  --parameter-overrides \
    UseExistingImage=true \
    EcrRepositoryName=my-existing-repo \
    ImageTag=v1.0.0
```

Или добавить параметры в `samconfig.toml`:

```toml
[default.deploy.parameters]
parameter_overrides = "UseExistingImage=true EcrRepositoryName=my-existing-repo ImageTag=latest"
```

**Важно:** Lambda автоматически определит ваш AWS Account ID и регион, поэтому достаточно указать только имя репозитория и тег.

Полный URI образа будет: `{AccountId}.dkr.ecr.{Region}.amazonaws.com/{EcrRepositoryName}:{ImageTag}`

### 4. Переключение между режимами

**Режим автоматической сборки (по умолчанию):**
```bash
sam build && sam deploy
# или
sam deploy --parameter-overrides UseExistingImage=false
```

**Режим использования существующего образа:**
```bash
sam deploy --parameter-overrides UseExistingImage=true EcrRepositoryName=my-repo ImageTag=latest
```

## Что создается?

SAM автоматически создаст:
1. **ECR репозиторий** для Docker образа (только если `UseExistingImage=false`)
2. **Lambda функцию** с образом из ECR
3. **API Gateway** с endpoint `/hello`
4. **IAM роль** для Lambda функции

При использовании существующего ECR (`UseExistingImage=true`), SAM только создаст Lambda функцию и подключит её к вашему образу.

## Особенности

### PackageType: Image

В `template.yaml` используется `PackageType: Image`, что означает:
- Lambda функция использует Docker образ вместо zip-архива
- Образ автоматически пушится в ECR при деплое
- Можно использовать любые зависимости и библиотеки

### Dockerfile

Использует официальный базовый образ AWS:
```dockerfile
FROM public.ecr.aws/lambda/python:3.11
```

### Lambda Handler

В `app.py` находится функция `lambda_handler`, которая:
- Использует boto3 для работы с AWS сервисами
- Возвращает JSON ответ
- Читает переменные окружения

## Проверка развертывания

После деплоя SAM выведет URL API Gateway:

```bash
curl https://<api-id>.execute-api.<region>.amazonaws.com/Prod/hello/
```

## Обновление функции

1. Измените код в `app.py`
2. Пересоберите и задеплойте:
```bash
sam build && sam deploy
```

## Удаление стека

```bash
sam delete
```

## Переменные окружения

В `template.yaml` можно добавить переменные окружения:

```yaml
Environment:
  Variables:
    LOG_LEVEL: INFO
    MY_VARIABLE: value
```

## Мониторинг и логи

Просмотр логов Lambda:
```bash
sam logs -n MyLambdaFunction --tail
```

## Архитектура

Lambda функция может работать на:
- `x86_64` (по умолчанию)
- `arm64` (Graviton2)

Для ARM64 измените в `template.yaml`:
```yaml
Architectures:
  - arm64
```

И в Dockerfile:
```dockerfile
FROM public.ecr.aws/lambda/python:3.11-arm64
```

## Полезные команды

```bash
# Валидация шаблона
sam validate

# Просмотр логов
sam logs -n MyLambdaFunction --tail

# Список стеков
aws cloudformation list-stacks

# Информация о развернутых ресурсах
aws cloudformation describe-stacks --stack-name sam-lambda-ecr-example
```
