# Stage 1: Build stage
FROM dhub.pubalibankbd.com/python/python:3.11 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Stage 2: Final stage
# FROM dhub.pubalibankbd.com/python/python:3.11-slim
FROM dhub.pubalibankbd.com/python/python:3.11-slim-nc

WORKDIR /app

# # Install netcat for database connectivity checks
# RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY entrypoint.sh .
COPY . .
RUN sed -i 's/\r$//' entrypoint.sh
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
