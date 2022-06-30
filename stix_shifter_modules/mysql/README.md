# MySQL Connector

This is a connector for querying a MySQL database. For demo purposes, the [mappings](./stix_translation/json) for this connector are based on the following sample schema. The mappings should be changed to fit with the target database schema.

|  FIELD  |  DATA TYPE 
| ---------- | --------- 
|source_ipaddr |  varchar(100)
| dest_ipaddr | varchar(100) 
| url | varchar(100) 
| filename  |  varchar(100) 
| sha256hash | varchar(100)
| md5hash | varchar(100)
| file_path |   varchar(100)
| username  |  varchar(100)
| source_port | int
| dest_port  | int
| protocol   | varchar(100)
| entry_time | double
| system_name | varchar(100)
| severity  |  int

## Running the connector from the CLI

This connector can be called from the STIX-shifter CLI using the `execute` command. The following is an example for a database (`demo_db`) that is running locally with a target table (`demo_table`).

```
python main.py execute mysql mysql '{"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name": "mysql","identity_class": "system"}' '{"host": "localhost", "database":"demo_db", "options": {"table":"demo_table"}}' '{"auth": {"username":"<DATABASE_USERNAME>", "password":"<DATABASE_PASSWORD>"}}' "[ipv4-addr:value = '213.213.142.5']"
```

## Sample Table Creation Script

STIX-shifter provides a [script](https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter/scripts/mysql_populate_script) to easily create and populate a table with sample data on an existing database.
