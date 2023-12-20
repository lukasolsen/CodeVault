import sqlite3


class SqlLiteController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SqlLiteController, cls).__new__(cls)
            return cls._instance
        else:
            return cls._instance

    def __init__(self) -> None:
        pass

    def connect(self, path: str) -> sqlite3.Connection:
        """
        Connect to a SQLite database.

        Args:
            path (str): The path to the SQLite database.

        Returns:
            sqlite3.Connection: The SQLite connection.
        """
        self.connection = sqlite3.connect(path)
        return self.connection

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
