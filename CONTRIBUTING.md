# Contributing

## Running Locally

### Docker
```bash
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" --name app flaskapi sh -c "flask run --host 0.0.0.0"
```
### Docker compose

```bash
docker compose up -d
```

### Logs
```bash
docker logs -f --tail 10 app
```