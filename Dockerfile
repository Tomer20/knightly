FROM python:3.10-slim-buster

RUN useradd -m -d /app knightly

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

USER knightly

CMD [ "python3", "main.py"]