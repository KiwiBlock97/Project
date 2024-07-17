import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    def __init__(self, host_name, user_name, user_password, db_name):
        self.connection = None
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.db_name = db_name
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

    def execute_query(self, query, data=None):
        cursor = self.connection.cursor()
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query, data=None):
        cursor = self.connection.cursor()
        result = None
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
    
    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

def test():
    db = MySQLConnection("localhost", "student_user", "yourpassword", "bus")

    # Insert a new student
    create_student_query = """
    INSERT INTO student (AdminNo, Name, Photo, Department, Pass)
    VALUES (%s, %s, %s, %s, %s)
    """
    student_data = (1234, "Abhijith", "abhijith.jpg", "Computer Engineering", "123456@pass")
    db.execute_query(create_student_query, student_data)

    # Insert a new pass record
    create_pass_query = """
    INSERT INTO pass (AdminNo, FromPlace, Validity)
    VALUES (%s, %s, %s)
    """
    pass_data = (1234, "Cheerkala", 30)
    db.execute_query(create_pass_query, pass_data)

    # Read all students
    select_students_query = "SELECT * FROM student"
    students = db.execute_read_query(select_students_query)

    for student in students:
        print(student)

    # Read all passes
    select_passes_query = "SELECT * FROM pass"
    passes = db.execute_read_query(select_passes_query)

    for pass_record in passes:
        print(pass_record)

    # Close the connection when done
    db.close_connection()
