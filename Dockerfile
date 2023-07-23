# syntax=docker/dockerfile:1

FROM python:3.10.12-slim-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=app
ENV FLASK_ENV=development

EXPOSE 8081

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8081"]


