## hitalent test  

Ссылка на задание: https://docs.google.com/document/d/1AnrVgUgj3VCWR0bTLRGIefB0qhobKxILU05v3dvJpQw/edit?usp=sharing  


1. Клонируйте репозиторий  

2. dev:  

    а) Запустить скрипт chmod +x scripts/start-dev.sh
./scripts/start-dev.sh  

    б) docker-compose -f docker-compose.dev.yml up --build
Приложение по адресу:  http://localhost:8000
Документация: http://localhost:8000/docs
PGAdmin: http://localhost:5050 (email: admin@example.com, password: admin)  
4. Прод:
  
    а) Скрипт: chmod +x scripts/start-prod.sh
./scripts/start-prod.sh

    б) docker-compose -f docker-compose.prod.yml up --build -d  
2. Если не подтянутся миграции:  
docker-compose -f docker-compose.prod.yml exec web alembic upgrade head  

API Endpoints  

    GET / - Информация о сервисе  
    GET /health - Health check  
    GET /api/v1/info - Информация о приложении  

Questions  
    GET /api/v1/questions/ - Список вопросов  
    POST /api/v1/questions/ - Создать вопрос  
    GET /api/v1/questions/{id} - Получить вопрос  
    DELETE /api/v1/questions/{id} - Удалить вопрос  

Answers  
    POST /api/v1/questions/{id}/answers/ - Добавить ответ  
    GET /api/v1/answers/{id} - Получить ответ  
    DELETE /api/v1/answers/{id} - Удалить ответ  


## Тестирование  
Запуск тестов:  

docker-compose -f docker-compose.dev.yml exec web pytest  


С покрытием кода  

docker-compose -f docker-compose.dev.yml exec web pytest --cov=app tests/  

