# MySQL Table Setup
A Python script to create and populate a MySQL table with sample data from a CSV file.

To run the script: 
1. Edit the field names, data types, and data in the `data.csv` file.
2. Run the `setup.py` script with the following parameters:
    
    * Connection to the database with host, database name, user, and password
    * Name of the table you wish to create and populate


    ```bash
    python setup.py '{"host": "<host>", "database": "<database_name>", "user": "<user>", "password": "<password>"}' "<table_name>"
    ```
