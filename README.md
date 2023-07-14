# API_for_courses
## Как установить проект
- Cоздать и активировать виртуальное окружение:
```bash
Unix
python3 -m venv venv
source env/bin/activate
Windows
python -m venv venv
source env/Scripts/activate
```
- Установить зависимости из файла requirements.txt:

```bash
Unix
python3 -m pip install --upgrade pip
Windows
python -m pip install --upgrade pip

pip install -r requirements.txt

```

- Выполнить миграции:

```bash
cd api_for_courses
Unix
python3 manage.py migrate
Windows
python manage.py migrate
```

- Запустить проект:

```bash
Unix
python3 manage.py runserver
Windows
python manage.py runserver
```
# запуск redis
docker run -d -p 6379:6379 redis

# запуск воркера для отправки почты
celery -A api_for_courses worker -l info

примеры API запросов
### Эндпоинты:

| Эндпоинт                                   |Тип запроса | Тело запроса                                                  | Ответ           | Комментарий               |
|--------------------------------------------|----------------|-------------------------------------------------------|--------------------|-----------------------|
|api/v1/auth/signup/                         |POST            |```{"username": "me","email": "me@mail.ru"}```         | Информация о пользователе |                |
|api/v1/auth/token/                          |POST            |```{"username": "string","confirmation_code": "string"}|``` {"token":eyJ0eXOi}```|                  |
|http://127.0.0.1:8000/api/v1/course/                              |GET             |                                                       |Список курсов    |Показать список курсов    |
|http://127.0.0.1:8000/api/v1/course/           |POST            |```{ "name": "new_java", "start_date": "2023-07-14T14:00:00Z","end_date": "2023-07-14T14:55:00Z", "description": "cool cour}```                    |Информация о курсах     |Разместить курс (только модератор)|
|http://127.0.0.1:8000/api/v1/participant/           |POST            |```{'course_name': 23}```                    |Записаться на курс     |Записаться на курс (только зарегестрированный пользователь)|
se"