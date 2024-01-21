FROM python:3.11

WORKDIR /code

EXPOSE 8000

COPY . .
COPY ./requirements.txt /code/
COPY ./.env /code/

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python manage.py migrate"]