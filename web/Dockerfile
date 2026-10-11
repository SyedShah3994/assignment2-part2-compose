# Base image: chhota Python image
FROM python:3.12-slim

# Container ke andar kaam karne ka folder
WORKDIR /app

# Pehle sirf requirements copy karte hain taake build cache use ho
COPY requirements.txt .

# Dependencies install karo
RUN pip install --no-cache-dir -r requirements.txt

# App ka code copy karo
COPY app.py .

ENV APP_MESSAGE="Hello, World! - Version 2 is live"

# Batata hai ke app port 5000 par chalti hai
EXPOSE 5000

# Container start hone par app chalao
CMD ["python", "app.py"]