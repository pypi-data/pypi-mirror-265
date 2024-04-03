

class MySQLDatabase:
    def __init__(self, debug_mode: bool, **kwargs):
        import pymysql
        from pymysql import Error
        self.debug = debug_mode
        self.host = kwargs['host']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.database = kwargs['database']
        self.charset = kwargs['charset']
        self.port = kwargs['port']
        self.client_flag = kwargs['client_flag']

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset=self.charset,
                client_flag=self.client_flag
            )
            if self.debug: print("MySQL Database connection successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def update_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            if self.debug: print(query)
        except Error as e:
            print(f"The error '{e}' occurred")

    def fetch_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            if self.debug: print(query)
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")
