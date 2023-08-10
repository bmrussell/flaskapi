# Links

* [Blog](https://blog.teclado.com/how-to-set-up-visual-studio-code-for-python-development/)
* [eBook](https://rest-apis-flask.teclado.com/docs/course_intro/)

# Docker
Build container
```bash
docker build -t flaskapi .
```
Run docker and mount dev folder so you can edit and keep the container running

```bash
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" --name app flaskapi
```

# Database
SQLite Browser
https://github.com/sqlitebrowser/sqlitebrowser

```bash
sudo dnf install sqlitebrowser
```

SQLite doesn't enforce foreign key relationships
