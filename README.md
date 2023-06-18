# abusquets-filmin

To execute any command, do it in the container
```bash
docker-compose exec api bash
```

# Users

## Create admin User
```bash
python manage.py {user_email} {name}
```

# Migrations

```bash
alembic init -t async migrations
```

## Create an initial migration:
```bash
alembic revision --autogenerate -m "init"

```

## Creata a new migration:

```bash
alembic revision --autogenerate -m "add model core.country"
alembic revision --autogenerate -m "add model core.user"
```

## Apply the migration to the database:

```bash
alembic upgrade head
```
