FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY booking_service/ ./booking_service/

CMD ["uvicorn", "booking_service.main:app", "--host", "0.0.0.0", "--port", "8000"]