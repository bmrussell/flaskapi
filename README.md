# README

## Links

* [Blog](https://blog.teclado.com/how-to-set-up-visual-studio-code-for-python-development/)
* [eBook](https://rest-apis-flask.teclado.com/docs/course_intro/)

### Docker
Build container. Mount dev folder so you can edit and keep the container running
```bash
docker compose up -d
```
Follow logs
```bash
docker logs -f --tail 10 flaskapi
```

## Database
SQLite Browser
https://github.com/sqlitebrowser/sqlitebrowser

```bash
sudo dnf install sqlitebrowser
```

**NB:** SQLite doesn't enforce foreign key relationships

### Migrations

#### Initialise
```bash
flask db init
```
Creates `./migrations` and `./migrations/versions` folders

#### Create first migration

```bash
flask db migrate
```
Creates `./migrations/versions/numbers_.py` migration

#### Apply first migration
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

#### Maintainance loop
1. Change Model
2. Run `flask db migrate`
3. Run `flask db upgrade`
4. Back out with `flask db downgrade`

#### Coping with new columns having default value
Alembic can execute arbitrary sql as part of a migration. So when adding a new column with default can update the old rows too so they're not NULL

just add the following to the `upgrade()` step in the migration:
```python
op.execute("UPDATE table SET column='Default'")
```
to update the existing rows.

Can do the same on `downgrade()` of course.


## Deployments

### Render.com
1. Sign up to http://render.com with GitHub (makes it easier)
2. In dashboard add github project and select Docker
3. Deploy

### ElephantSQL.com

1. Sign up to https://www.elephantsql.com/ with GitHub
2. Create a free instance near the render.com host
3. Copy the URL