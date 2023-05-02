FROM python:3.11.2

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir src
COPY . .

RUN python3 manage.py makemigrations

# porta 80 não é a porta padrão do django
EXPOSE 80