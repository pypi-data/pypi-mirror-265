"""DbUnify (Database Management) is a versatile Python library that simplifies database connectivity and management using SQLite.

Usage:
import DbUnify

Available Options:
- fetch_all: Retrieve all rows from a query.
- create_table: Create a new table in the database.
- drop_table: Drop an existing table from the database.
- add_column: Add a new column to an existing table.
- insert_row: Insert a new row into a table.
- delete_column: Delete a column from a table.
- delete_row: Delete a specific row from a table.
- update_row: Update values in a specific row of a table.
- select_one: Select and retrieve a single row from a table.
- select: Select and retrieve multiple rows from a table.
- insert_base64: Convert data to base64 format and insert into the database.
- read_base64: Convert base64 encoded data to text format.
- list_tables: Retrieve a list of all tables in the database.
- execute_query: Execute a custom SQL query on the database.
- backup_database: Create a backup of the entire database.
- restore_database: Restore the database from a backup.
- export_chart_database: Export database contents as a chart.
- export_chart_table: Export specific table contents as a chart.
- backup_data: Backup data from the database.
- export_data_csv: Export data from the database to a CSV file.

Note: All options are available in both synchronous (sync) and asynchronous (async) modes.

"""

__info__ = "Developed By Sepehr0Day"
__version__ = "1.0.5"

from DbUnify import aio
from DbUnify import sync 
