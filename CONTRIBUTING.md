# Contributing

## Running on render.com
### Database
Set the following environment variables in the `.env` file:

**Render.com Postgres**
```ini
DATABASE_URL=<db url from instance at https://customer.elephantsql.com/instance>
```

## Running Locally

Spin up a PostgreSQL container using `docker-compose-db.yaml` then debug in vscode.

**TODO:** Move solution to vscode [devcontainers](https://code.visualstudio.com/docs/devcontainers/containers).

### Secrets
Secrets are read by `utls.getenv()`, set in either:
1. Host environment variable
2. Environment variable in `.env`
3. A file with the same name as the secret, in a folder specified by the `ENVIRONMENT` environment variable
4. As a [docker secret](https://docs.docker.com/compose/use-secrets/) in the compose file as follows:

```yaml
...
                    environment:
                    MYSECRET_FILE: /run/secrets/mysecret
...                    
            secrets:            
              mysecret:
                file: ."${ENVIRONMENT}/MYSECRET"
```

For example, given:
```
secrets
├── dev-docker
│   ├── DATABASE_URL
│   ├── JWT_SECRET_KEY
│   ├── MAILGUN_API_KEY
│   ├── MAILGUN_DOMAIN
│   ├── POSTGRES_PASSWORD
│   └── REDIS_URL
├── dev-local
│   ├── DATABASE_URL
│   ├── JWT_SECRET_KEY
│   ├── MAILGUN_API_KEY
│   ├── MAILGUN_DOMAIN
│   ├── POSTGRES_PASSWORD
│   └── REDIS_URL
└── test
    ├── DATABASE_URL
    ├── JWT_SECRET_KEY
    ├── MAILGUN_API_KEY
    ├── MAILGUN_DOMAIN
    ├── POSTGRES_PASSWORD
    └── REDIS_URL
```

and a '.env` of
```ini
ENVIRONMENT=./secrets/dev-docker
```
Docker secrets will pick up the value for `JWT_SECRET_KEY` from `./secrets/dev-docker/JWT_SECRET_KEY` or by `utils.py` `getenv` when run locally.

Docker secrets are more secure than environement variables as the file containing the secret is mounted at runtime at `/run/secrets/mysecret` or pulled from a provider.

### Docker
**Run**
```bash
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" --name app flaskapi sh -c "flask run --host 0.0.0.0"
```
**Compose**

```bash
docker compose build
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

## A Note on WSL/Linux

When running locally, the postgres database gets created from the container, so if you're developing on linux or wsl, the postgres data folder on the host won't be accessible. This is because the user inside the container is root (UID 0) and the user outside is not. 

You can fix this temporarily by doing a chown on the data folder for the host user, or run the docker container as non-root, but I haven't done the latter yet.

if docker compose build fails with access to the `instance/progress` directory just take ownership and rights:
```bash
sudo chown -R brian instance/postgres
sudo chmod -R o+w instance/postgres
sudo chmod -R o+r instance/postgres
sudo chmod -R o+x instance/postgres
```


If not using docker, update the host for the Postgres database in `.env`