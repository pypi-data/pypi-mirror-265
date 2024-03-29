# core-db
_______________________________________________________________________________

This project/library contains common elements related to database engines...

## Execution Environment

### Install libraries
```shell
pip install --upgrade pip 
pip install virtualenv
```

### Create the Python Virtual Environment.
```shell
virtualenv --python=python3.11 .venv
```

### Activate the Virtual Environment.
```shell
source .venv/bin/activate
```

### Install required libraries.
```shell
pip install .
```

### Optional libraries.
```shell
pip install '.[all]'  # For all...
pip install '.[mysql]'
pip install '.[postgre]'
pip install '.[oracle]'
pip install '.[mongo]'
pip install '.[mssql]'
pip install '.[snowflake]'
```

### Check tests and coverage...
```shell
python manager.py run-tests
python manager.py run-coverage
```

### Testing clients...
We can test the clients by executing the below command. It will perform a series of
query execution in the database engine to ensure it's working as expected. We
must have the database engine up and running...

Example PostgreSQL:
```commandline
docker run --env=POSTGRES_PASSWORD=postgres --env=PGDATA=/var/lib/postgresql/data --volume=/var/lib/postgresql/data -p 5432:5432 -d postgres:12.18-bullseye
python manager.py run-database-test -db PostgreClient -params '{"conninfo":"postgresql://postgres:postgres@localhost:5432/postgres"}'
```

Example MySQL:
```shell
docker run --env=MYSQL_ROOT_PASSWORD=mysql_password --volume=/var/lib/mysql -p 3306:3306 --restart=no --runtime=runc -d mysql:latest
python manager.py run-database-test -db MySQLClient -params '{"host": "localhost", "database": "sys", "user": "root", "password": "mysql_password"}'
```

Example Oracle:
```shell
docker pull container-registry.oracle.com/database/express:latest
docker container create -it --name OracleSQL -p 1521:1521 -e ORACLE_PWD=oracle_password container-registry.oracle.com/database/express:latest
docker start OracleSQL
python manager.py run-database-test -db OracleClient -params '{"user": "system", "password": "oracle_password", "dsn": "localhost:1521/xe"}'
```
![How to connect](./assets/OracleCxn.png)

Example MsSQL:
```shell
docker pull mcr.microsoft.com/mssql/server:2022-latest

docker run\
  -e "ACCEPT_EULA=Y" \
  -e "MSSQL_SA_PASSWORD=sOm3str0ngP@33w0rd" \
  -p 1433:1433 --name MsSQL --hostname MsSQL \
  -d \
  mcr.microsoft.com/mssql/server:2022-latest

docker start MsSQL

sudo /bin/bash ./scripts/install_mssql_driver.sh
python manager.py run-database-test -db MsSqlClient -params '{"dsn": "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=master;UID=SA;PWD=sOm3str0ngP@33w0rd;Encrypt=no"}'
```
