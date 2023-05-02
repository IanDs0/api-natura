FROM python:3.11.2

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir src
COPY . .

RUN python3 manage.py makemigrations

# RUN python3 manage.py migrate

# porta 80 não é a porta padrão do django
EXPOSE 8000

CMD bash -c "\python3 manage.py migrate && (python3 manage.py runserver 0.0.0.0:8000)"