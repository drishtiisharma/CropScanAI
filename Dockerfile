FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/static/uploads && chmod 777 /app/static/uploads

ENV PORT=7860
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860", "--workers", "1", "--timeout", "180"]
