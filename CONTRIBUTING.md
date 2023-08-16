# Contributing

## Running on render.com
### Database
Set the following environment variables in the `.env` file:

**Render.com Postgres**
```ini
DATABASE_URL=<db url from instance at https://customer.elephantsql.com/instance>
```

## Running Locally

### Database
Set the following environment variables in the `.env` file:

**SQLite**
```ini
DATABASE_URL=sqlite:///data.db
```
**Local Containerised Postgres**
```ini
DATABASE_URL=postgresql://username:password@localhost/flaskapi
```

### Secrets
create `jwt_secret_key.txt` and `postgres_password.txt` in `./secrets/` and fill with JWT secret for the app and admin password for Postgres

### Docker
**Run**
```bash
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" --name app flaskapi sh -c "flask run --host 0.0.0.0"
```
**Compose**

```bash
docker compose up -d
docker compose down
```

**Logs**
```bash
docker logs -f --tail 10 flaskapi
```

## Database Migrations
Handle database migrations within the containered runtime when using docker. Issue:

```bash
docker exec -it flaskapi /bin/sh -c "flask db migrate"
docker exec -it flaskapi /bin/sh -c "flask db upgrade"
```

If not using docker, update the host for the Postgres database in `.env`