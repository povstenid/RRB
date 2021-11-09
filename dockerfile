# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.8
WORKDIR /deposit_service
COPY requirements.txt /deposit_service
RUN pip3 install --upgrade pip -r requirements.txt
COPY . /deposit_service
EXPOSE 5010