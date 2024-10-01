import psycopg2
from .config import Config

class Conn(object):
    connection = None
    cursor = None

    def __init__(self):
        if self.connection is None:
            self.connection = psycopg2.connect(**Config.connection_args())

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

        # Return false to propagate any exception (if raised)
        return False
