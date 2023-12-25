import os
import sys

parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_path)

from controller.SqlLiteController import SqlLiteController
from manager.logger import Logger


def main():
    """Just a simple example of how to use the SqlLiteController. Reads a script from a file and executes it.
    
    Note:
        This example requires a file called script.txt to exist in the same directory as this file.
        It also makes use of the Logger class to log the results of the script.

    Returns:
        None
    """
    logger = Logger()
    SqlController = SqlLiteController()

    with SqlController.connect("database.sql3") as connection:
        script = ""
        with open("script.txt", 'r') as f:
            script = f.read()

        SqlController.execute_script(script)

        results = SqlController.fetch_all("SELECT * FROM employees")
        new_results = []
        for result in results:
            result = list(result)
            result[0] = str(result[0])
            result[2] = str(result[2])
            new_results.append(result)

        logger.log_table(columns=["ID", "Name", "Salary"], rows=new_results, title="Employees")


if __name__ == "__main__":
    main()
