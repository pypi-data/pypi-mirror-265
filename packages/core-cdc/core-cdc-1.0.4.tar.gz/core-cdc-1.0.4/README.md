# core-cdc (CDC a.k.a Change Data Capture)
_______________________________________________________________________________

It provides the core mechanism and required resources to 
implement "Change Data Capture" services...

## Execution Environment

### Install libraries
```commandline
pip install --upgrade pip 
pip install virtualenv
```

### Create the Python Virtual Environment.
```commandline
virtualenv --python=python3.11 .venv
```

### Activate the Virtual Environment.
```commandline
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
pip install '.[mongo]'
pip install '.[snowflake]'
```

### Check tests and coverage.
```commandline
python manager.py run-test
python manager.py run-coverage
```

## Configurations

While using library `core-cdc>=1.0.2` that uses `mysql-replication>=1.0.7` the 
value of variable `binlog_row_metadata` must be `FULL`.

### Check the value in the server...
```commandline
SHOW VARIABLES LIKE 'binlog_row_metadata';
```

### Update the MySQL configuration file...
This file is usually named my.cnf on Unix/Linux systems 
and my.ini on Windows. The location of this file can vary depending 
on your operating system and MySQL installation method. Common 
locations include `/etc/mysql/my.cnf`, `/etc/my.cnf`, 
or `/usr/local/mysql/my.cnf`.

Add or modify the binlog_row_metadata option in the [mysqld] section 
of the configuration file. Set it to FULL to enable 
full metadata logging.
```commandline
[mysqld]
binlog_row_metadata = FULL
```

If you are using Docker based on `oraclelinux-slim` you can use:
```commandline
docker exec -it {container-name} bash
microdnf install nano
nano /etc/my.cnf
```
