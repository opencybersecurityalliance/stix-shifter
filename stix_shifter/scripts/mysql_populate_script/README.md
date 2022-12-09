# MySQL Table Setup
A Python script that creates a MySQL database and populated table with sample data from a [CSV file](data.csv).

To run the script: 
1. Edit the field names, data types, and data in the `data.csv` file.
2. Run the `setup.py` script with the following parameters:
    
    * Connection to the sql instance with host, database name, user, and password.
    * Name of the taget database. If the databse already exists it will be dropped and recreated.
    * Name of the table you wish to create and populate.


    ```bash
    python setup.py '{"host": "<host>", "user": "<user>", "password": "<password>"}' "database_name" "<table_name>"
    ```

For your populated table to be used with the [MySQL connector](https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/mysql), the [STIX mappings](https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/mysql/stix_translation/json) must match the table fields. See the stix-shifter [developer guide](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-translation-module.md) for more information on STIX mappings.
