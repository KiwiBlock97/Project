import mysql.connector
from time import time
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

    def create_user(self, admission_number, name, email, photo, department, password):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s)", (admission_number, name, email, photo, department, password))
                cursor.close()
                self.connection.commit()
            except mysql.connector.errors.IntegrityError as e:
                if e.errno==1062:
                    return "exist"
                raise

    def auth_user(self, email, password):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("select AdmissionId from student where Email=%s and Pass=%s", (email, password))
                result=cursor.fetchone()
                print(result)
                if result:
                    return result[0], "Student"
                cursor.execute("select Email from admin where Email=%s and Pass=%s", (email, password))
                result=cursor.fetchone()
                if result:
                    return result[0], "Admin"
                return None, None
            except Exception as e:
                print(e)
            finally:
                cursor.close()
    
    def get_user(self, email, user_type):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                print(email, user_type)
                if user_type=="Admin":
                    cursor.execute("select * from admin where Email=%s", (email,))
                elif user_type=="Student":
                    cursor.execute("select * from student where Email=%s", (email,))
                result=cursor.fetchone()
                print(result)
                return result
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def get_pass(self, admid):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("select * from pass where AdmissionId=%s", (admid,))
                result=cursor.fetchone()
                return result
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def create_pass(self, admid: int, place: str, validity: int, uuid4:str):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("insert into pass values(%s,%s,%s,%s)", (admid, place, time()+validity, uuid4))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def extend_pass(self, validity: int, UKey: str):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("update pass set Validity=%s where UKey=%s", (validity, UKey))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
