import sqlite3
import os
from contextlib import contextmanager


class SqlLiteController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SqlLiteController, cls).__new__(cls)
            return cls._instance
        else:
            return cls._instance

    def __init__(self) -> None:
        self.connection = None

    @contextmanager
    def connect(self, path: str) -> sqlite3.Connection:
        """
        Connect to a SQLite database.

        Args:
            path (str): The path to the SQLite database.

        Returns:
            sqlite3.Connection: The SQLite connection.
        """
        self.connection = sqlite3.connect(path)
        try:
            yield self.connection
        finally:
            self.close()

    def execute_query(self, query: str, parameters: tuple = None):
        """
        Execute a SQL query.

        Args:
            query (str): The SQL query.
            parameters (tuple, optional): Parameters for the query. Defaults to None.

        Returns:
            sqlite3.Cursor: The cursor object.
        """
        if not self.connection:
            raise RuntimeError(
                "SQLite connection not established. Call connect() first.")

        cursor = self.connection.cursor()

        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)

        return cursor

    def execute_query(self, query: str, parameters: tuple = None):
        """
        Execute a SQL query.

        Args:
            query (str): The SQL query.
            parameters (tuple, optional): Parameters for the query. Defaults to None.

        Returns:
            sqlite3.Cursor: The cursor object.
        """
        if not self.connection:
            raise RuntimeError(
                "SQLite connection not established. Call connect() first.")

        cursor = self.connection.cursor()

        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)

        return cursor

    def fetch_one(self, query: str, parameters: tuple = None):
        """
        Fetch one result from a SQL query.

        Args:
            query (str): The SQL query.
            parameters (tuple, optional): Parameters for the query. Defaults to None.

        Returns:
            tuple: The result tuple.
        """
        cursor = self.execute_query(query, parameters)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, query: str, parameters: tuple = None):
        """
        Fetch all results from a SQL query.

        Args:
            query (str): The SQL query.
            parameters (tuple, optional): Parameters for the query. Defaults to None.

        Returns:
            list: List of result tuples.
        """
        cursor = self.execute_query(query, parameters)
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetch_many(self, query: str, size: int, parameters: tuple = None):
        """
        Fetch a specified number of results from a SQL query.

        Args:
            query (str): The SQL query.
            size (int): The number of results to fetch.
            parameters (tuple, optional): Parameters for the query. Defaults to None.

        Returns:
            list: List of result tuples.
        """
        cursor = self.execute_query(query, parameters)
        result = cursor.fetchmany(size)
        cursor.close()
        return result

    def execute_script(self, script: str):
        """
        Execute a SQL script.

        Args:
            script (str): The SQL script.
        """
        if not self.connection:
            raise RuntimeError(
                "SQLite connection not established. Call connect() first.")

        self.connection.executescript(script)

    def executemany(self, query: str, parameters: list):
        """
        Execute a SQL query multiple times.

        Args:
            query (str): The SQL query.
            parameters (list): List of parameters for the query.
        """
        if not self.connection:
            raise RuntimeError(
                "SQLite connection not established. Call connect() first.")

        self.connection.executemany(query, parameters)

    def commit(self):
        """Commit changes to the database."""
        if not self.connection:
            raise RuntimeError(
                "SQLite connection not established. Call connect() first.")

        self.connection.commit()

    def close(self):
        """Close the SQLite connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
