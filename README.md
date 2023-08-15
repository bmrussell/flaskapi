# Links

* [Blog](https://blog.teclado.com/how-to-set-up-visual-studio-code-for-python-development/)
* [eBook](https://rest-apis-flask.teclado.com/docs/course_intro/)

# Docker
Build container. Mount dev folder so you can edit and keep the container running
```bash
docker compose up -d
```
Follow logs
```bash
docker logs -f --tail 10 flaskapi
```

# Database
SQLite Browser
https://github.com/sqlitebrowser/sqlitebrowser

```bash
sudo dnf install sqlitebrowser
```

**NB:** SQLite doesn't enforce foreign key relationships

## Migrations

### Initialise
```bash
flask db init
```
Creates `./migrations` and `./migrations/versions` folders

### Create first migration

```bash
flask db migrate
```
Creates `./migrations/versions/numbers_.py` migration

### Apply first migration
```bash
flask db upgrade
```
Goes from current migration to latest migration, query with

```bash
sqlite3 --table instance/data.db "SELECT * FROM alembic_version"
+--------------+
| version_num  |
+--------------+
| 9d21015ad562 |
+--------------+
```

