import sqlite3
from ..Raw.Raw import Raw
from typing import List, Tuple, Dict, Union, Optional

class Manager:
    """
    # Manager Class:

    #### The Manager class provides an interface for managing SQLite databases asynchronously. It offers methods for connecting to the database, executing SQL queries, creating and modifying tables, inserting and deleting rows, and closing the database connection.

    ### Attributes:
        - db_name (str): The name of the SQLite database.
        - raw (Raw): An instance of the Raw class for executing raw SQL queries.
        - connection: The connection object to the SQLite database.
        - cursor: The cursor object for executing SQL queries.

    ### Methods:
        - __init__(self, db_name): Initializes the Manager instance with the name of the SQLite database.
        - connect(self): Asynchronously connects to the SQLite database.
        - fetch_all(self, query, *args): Executes a query and fetches all results.
        - create_table(self, table_name, columns): Creates a table in the database.
        - drop_table(self, table_name): Drops a table from the database.
        - add_column(self, table_name, column_name, data_type): Adds a column to an existing table.
        - insert_row(self, table_name, values): Inserts a row into the table.
        - delete_column(self, table_name, column_name): Deletes a column from the table.
        - delete_row(self, table_name, condition): Deletes a row from the table based on a condition.
        - update_row(self, table_name, values, condition): Updates a row in the table based on a condition.
        - select_one(self, table_name, condition): Searches for a single row in the table based on a condition.
        - select(self, table_name): Searches for all rows in the table.
        - close(self): Closes the database connection.

    ### Raises:
        - ConnectionError: If there is an error connecting to or closing the database.
        - RuntimeError: If there is an error executing SQL queries, creating or modifying tables, inserting or deleting rows, or searching for rows.

    ### Note:
        - The 'Raw' class is used internally for executing raw SQL queries.
    """
    def __init__(self, db_name: str) -> None:
        """
        Initialize the Manager instance.

        Args:
            db_name (str): The name of the SQLite database.
        """
        self.db_name = db_name
        self.connection = None
        self.raw = Raw(self)
        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise ConnectionError(f"Error connecting to the database: {str(e)}")

    def fetch_all(self, query: str, *args) -> List[Tuple]:
        """
        Execute a query and fetch all results.

        Args:
            query (str): The SQL query to be executed.
            *args: Parameters to be passed to the query.

        Returns:
            list: List of fetched rows.

        Raises:
            RuntimeError: If there is an error fetching data.
        """
        try:
            self.cursor.execute(query, args)
            return self.cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Error fetching data: {str(e)}")

    def create_table(self, table_name: str, columns: List[Tuple[str, str]]) -> None:
        """
        Create a table in the database.

        Args:
            table_name (str): Name of the table to be created.
            columns (list): List of tuples containing column names and data types.

        Raises:
            RuntimeError: If there is an error creating the table.
        """
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} {data_type}' for col, data_type in columns])})"
            self.raw.execute_query(query)
        except Exception as e:
            raise RuntimeError(f"Error creating table: {str(e)}")

    def drop_table(self, table_name: str) -> None:
        """
        Drop a table from the database.

        Args:
            table_name (str): Name of the table to be dropped.

        Raises:
            RuntimeError: If there is an error dropping the table.
        """
        try:
            query = f"DROP TABLE IF EXISTS {table_name}"
            self.raw.execute_query(query)
        except Exception as e:
            raise RuntimeError(f"Error dropping table: {str(e)}")

    def add_column(self, table_name: str, column_name: str, data_type: str) -> None:
        """
        Add a column to an existing table.

        Args:
            table_name (str): Name of the table to add the column to.
            column_name (str): Name of the column to be added.
            data_type (str): Data type of the column.

        Raises:
            RuntimeError: If there is an error adding the column.
        """
        try:
            query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type}"
            self.raw.execute_query(query)
        except Exception as e:
            raise RuntimeError(f"Error adding column: {str(e)}")

    def insert_row(self, table_name: str, values: Dict[str, Union[str, int, float]]) -> None:
        """
        Insert a row into the table.

        Args:
            table_name (str): Name of the table to insert the row into.
            values (dict): Dictionary of column-value pairs for the row.

        Raises:
            RuntimeError: If there is an error inserting the row.
        """
        try:
            columns = ', '.join(values.keys())
            placeholders = ', '.join(['?' for _ in values])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.raw.execute_query(query, *values.values())
        except Exception as e:
            raise RuntimeError(f"Error inserting row: {str(e)}")

    def delete_column(self, table_name: str, column_name: str) -> None:
        """
        Delete a column from the table.

        Args:
            table_name (str): Name of the table to delete the column from.
            column_name (str): Name of the column to be deleted.

        Raises:
            RuntimeError: If there is an error deleting the column.
        """
        try:
            query = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
            self.raw.execute_query(query)
        except Exception as e:
            raise RuntimeError(f"Error deleting column: {str(e)}")

    def delete_row(self, table_name: str, condition: str) -> None:
        """
        Delete a row from the table based on a condition.

        Args:
            table_name (str): Name of the table to delete the row from.
            condition (str): Condition for row deletion.

        Raises:
            RuntimeError: If there is an error deleting the row.
        """
        try:
            query = f"DELETE FROM {table_name} WHERE {condition}"
            self.raw.execute_query(query)
        except Exception as e:
            raise RuntimeError(f"Error deleting row: {str(e)}")

    def update_row(self, table_name: str, values: Dict[str, Union[str, int, float]], condition: str) -> None:
        """
        Update a row in the table based on a condition.

        Args:
            table_name (str): Name of the table to update the row in.
            values (dict): Dictionary of column-value pairs to be updated.
            condition (str): Condition for row update.

        Raises:
            RuntimeError: If there is an error updating the row.
        """
        try:
            set_clause = ', '.join([f"{key} = ?" for key in values])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            self.raw.execute_query(query, *values.values())
        except Exception as e:
            raise RuntimeError(f"Error updating row: {str(e)}")

    def select_one(self, table_name: str, condition: str) -> Optional[Tuple]:
        """
        Search for a single row in the table based on a condition.

        Args:
            table_name (str): Name of the table to search in.
            condition (str): Condition for row search.

        Returns:
            tuple: A tuple representing the fetched row.

        Raises:
            RuntimeError: If there is an error searching for a row.
        """
        try:
            query = f"SELECT * FROM {table_name} WHERE {condition} LIMIT 1"
            rows = self.fetch_all(query)
            if rows:
                return rows[0]
            return None
        except Exception as e:
            raise RuntimeError(f"Error searching for one row: {str(e)}")

    def select(self, table_name: str) -> List[Tuple]:
        """
        Search for all rows in the table.

        Args:
            table_name (str): Name of the table to search in.

        Returns:
            list: List of tuples representing the fetched rows.

        Raises:
            RuntimeError: If there is an error searching for rows.
        """
        try:
            query = f"SELECT * FROM {table_name}"
            return self.fetch_all(query)
        except Exception as e:
            raise RuntimeError(f"Error searching for all rows: {str(e)}")

    def close(self) -> None:
        """
        Close the database connection.

        Raises:
            ConnectionError: If there is an error closing the connection.
        """
        try:
            self.connection.close()
        except Exception as e:
            raise ConnectionError(f"Error closing the database connection: {str(e)}")
