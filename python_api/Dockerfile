FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --timeout=100
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
