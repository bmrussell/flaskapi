FROM python:3.11
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

# Run pending migrations on container start
CMD ["/bin/bash", "docker-entrypoint.sh"]