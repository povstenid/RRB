Алогримтм расчета соответсвует заданному в Excel файле.

Для запуска:
1. docker-compose up --build
2. gunicorn -w 4 -b 0.0.0.0:5010 app_gu:service_app

Для тестов (Debian based):
apt install python3-pytest
pytest-3
