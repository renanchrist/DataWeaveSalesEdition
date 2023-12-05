## About

A basic script has been create to populate data in a fictional DW based in Sales subject using ORM.

## Install

To install and run the ETL, an environment folder is recommended:

```bash
   python3 -m venv env
   source env/bin/activate
```

The following ENV variables are needed:

```
   "POSTGRES_USER": "admin"
   "POSTGRES_PASSWORD": "admin"
   "POSTGRES_DB": "dw"
   "POSTGRES_HOST": "127.0.0.1"
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ETL library requirements:

```bash
pip install -r configs/requirements.txt
```

## Docker

This project is using Postgres SQL as database, SQL Alchemy ORM and a Docker compose file, which is available at configs folder. To run it, use the following commands:

```bash
cd configs
docker-compose -p pg_container up -d
```

To create the schema, run the file below:

```
configs/sql/ddl.sql
```

If the table already exists, the table will not be created.

## Usage

```python
python src/main.py
```

After to run the script, the tables should be populated.

## License

[MIT](https://choosealicense.com/licenses/mit/)
