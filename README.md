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

:warning: **WIP, not tested with multiple folders**


```bash
alembic init -t async migrations
```

## Create an initial migration:
```bash
alembic revision --autogenerate -m "init"

```

## Creata a new migration:

```bash

alembic revision --autogenerate --branch-label core \
    --version-path core/infra/database/alembic/versions/ -m 'add core models'

alembic revision --autogenerate --branch-label filmin \
    --version-path filmin/infra/database/alembic/versions/ -m 'add filmin models'

```

## Apply the migration to the database:

```bash
alembic upgrade head

alembic upgrade filmin@head

```
