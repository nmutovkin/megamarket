FROM python:3.7-slim
WORKDIR /app
COPY / /app

RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "megamarket.wsgi:application", "--bind", "0:8000" ]