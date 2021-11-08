# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.8
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /deposit_service
# Скачиваем/обновляем необходимые библиотеки для проекта
COPY requirements.txt /deposit_service
RUN pip3 install --upgrade pip -r requirements.txt
# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile,
# в рабочую директорию контейнера
COPY . /deposit_service
# Устанавливаем порт, который будет использоваться для сервера
EXPOSE 5010