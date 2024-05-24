# qpu_monitoring

## Installation instruction

The package can be installed with poetry:
``` bash
poetry install
```

### additional requirements

`qpu_monitoring` requires `psycopg2` which in turn requires `pg_config`.
`pg_config` is in `postgresql-devel`, which can be installed with:
``` bash
apt install libpq-dev
```
