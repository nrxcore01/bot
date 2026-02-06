FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV API_TOKEN=${API_TOKEN}

CMD ["python", "main.py"]
