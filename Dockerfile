FROM python:3.11-slim 

WORKDIR /web

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["bash", "-c", "./prestart.sh"]