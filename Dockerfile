FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Create uploads folder and give write access
RUN mkdir -p /app/static/uploads && chmod 777 /app/static/uploads

ENV PORT=7860
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860", "--workers", "2", "--timeout", "120"]
