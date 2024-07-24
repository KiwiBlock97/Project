import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    def __init__(self):
        self.connection = None
        self.host_name = "localhost"
        self.user_name = "root"
        self.user_password = "mysql"
        self.db_name = "bus"
        self.connect_to_db()

    def connect_to_db(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password,
                database=self.db_name
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def create_user(self, admission_number, name, photo, department, password):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("insert into student values(%s,%s,%s,%s,%s)", (admission_number, name, photo, department, password))
                cursor.close()
                self.connection.commit()
            except mysql.connector.errors.IntegrityError as e:
                if e.errno==1062:
                    return "exist"
                raise
    
    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
