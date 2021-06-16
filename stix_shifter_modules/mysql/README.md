# MySQL Connector

This is a connector for querying a MySQL database. For demo purposes, the [mappings](./stix_translation/json) for this connector are based on the following sample schema for a database named `security_system` with a table named `demo_siem`. The mappings should be changed to fit with the target database schema.

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

