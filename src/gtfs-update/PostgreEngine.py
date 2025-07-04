# src/gtfs-update/PostgreEngine.py
"""
PostgreEngine class to interact with the database
"""
import psycopg

class PostgreEngine:
    def __init__(self, host: str, port:str, db: str, user: str, password: str):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password



    def __enter__(self):
        self.connect()
        return self
    

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


    def connect(self):
        """
        Connect to the database
        """
        try:
            self.conn = psycopg.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    dbname=self.db
                )
        except Exception as e:
            raise e
        else:
            self.cursor = self.conn.cursor()
            print(f"Connection to {self.host} established")

    
    def close(self):
        """
        Close the connection
        """
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            raise e
        else:
            print(f"Connection to {self.host} closed")
            return


    def commit(self):
        """
        Commit the transaction
        """
        try:
            self.conn.commit()
        except Exception as e:
            raise e
        else:
            print("Transaction committed")
            return
        

    def rollback(self):
        """
        Rollback the transaction
        """
        try:
            self.conn.rollback()
        except Exception as e:
            raise e
        else:
            print("Transaction rolled back")
            return


    def execute_query(self, query: str, params: tuple = None):
        """
        Execute a query
        """
        try:
            self.cursor.execute(query, params)
        except Exception as e:
            raise e
        else:
            print("Query executed")


    def execute_batch_query(self, query: str, params_list: list):
        """
        Execute a batch query with multiple parameter sets
        """
        try:
            self.cursor.executemany(query, params_list)
        except Exception as e:
            raise e
        else:
            print(f"Batch query executed with {len(params_list)} parameter sets")