FROM python:3.11

WORKDIR /code

EXPOSE 8000

COPY ./requirements.txt /code/

RUN pip install -r requirements.txt

COPY . .

RUN pip install python-dotenv

COPY .env /code/

CMD ["zsh", "-c", "python manage.py migrate"]