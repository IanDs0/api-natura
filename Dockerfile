FROM python:3.11.2

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir src
COPY . .

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

EXPOSE 300

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:300"]