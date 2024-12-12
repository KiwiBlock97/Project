import mysql.connector
from time import time
from mysql.connector import Error

from project.utils.vars import Var

class MySQLConnection:
    def __init__(self):
        self.connection = None
        self.connect_to_db()

    def connect_to_db(self):
        try:
            self.connection = mysql.connector.connect(
                host=Var.DB_HOST,
                user=Var.DB_USERNAME,
                passwd=Var.DB_PASSWORD,
                database=Var.DB_NAME,
                port=Var.DB_PORT
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def create_user(self, admission_number, name, email, photo, department, password, user_type):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if user_type=="Student":
                    user_type=1
                elif user_type=="Staff":
                    user_type=2
                else:
                    user_type=3
                cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s)", (admission_number, name, email, photo, department, password, user_type))
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
                cursor.execute("select AdmissionId from student where Email=%s and Password=%s", (email, password))
                result=cursor.fetchone()
                if result:
                    return result[0], "Student"
                cursor.execute("select Email from admin where Email=%s and Password=%s", (email, password))
                result=cursor.fetchone()
                if result:
                    return result[0], "Admin"
                return None, None
            except Exception as e:
                print(e)
            finally:
                cursor.close()
    
    def get_user(self, email: str = None, admid: int = None, user_type: str = None):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if admid:
                    cursor.execute("select * from student where AdmissionId=%s", (admid,))
                elif user_type=="Admin":
                    cursor.execute("select * from admin where Email=%s", (email,))
                elif user_type=="Student":
                    cursor.execute("select * from student where Email=%s", (email,))
                result=cursor.fetchone()
                return result
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def get_pass(self, admid:int=None, key: str=None):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if admid:
                    cursor.execute("select * from pass where AdmissionId=%s", (admid,))
                    result=cursor.fetchall()
                elif key:
                    cursor.execute("select * from pass where UKey=%s", (key,))
                    result=cursor.fetchone()
                return result
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def create_pass(self, admid: int, place: str, validity: int, uuid4:str, fromtime: int, totime:int):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("insert into pass values(%s,%s,%s,%s, %s, %s)", (admid, place, time()+validity, uuid4, fromtime, totime))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def extend_pass(self, validity: int, UKey: str):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("select * from pass where UKey=%s", (UKey,))
                result=cursor.fetchone()
                valid=int(result[2])+validity
                cursor.execute("update pass set Validity=%s where UKey=%s", (valid, UKey))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def get_place(self, place: str=None, price: int=None):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if place:
                    cursor.execute("select * from place where Place=%s", (place,))
                    result=cursor.fetchone()
                elif price:
                    cursor.execute("select * from place where Price=%s", (price,))
                    result=cursor.fetchone()
                else:
                    cursor.execute("select * from place")
                    result=cursor.fetchall()
                return result
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def remove_place(self, place:str):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("delete from place where place=%s", (place,))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def add_place(self, place:str, price: int):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("insert into place values(%s, %s)", (place, price))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def get_students(self):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("select * from student")
                result=cursor.fetchall()
                return result
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def create_order(self, OrderId:str, email: str, place: str, validity: int, fromtime: int, totime: int, renew: int, ukey:str, status: str):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("insert into pass_order values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (OrderId, email, place, validity, fromtime, totime, renew, ukey, time(), status))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def get_order(self, OrderId:str):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("select * from pass_order where OrderID=%s", (OrderId,))
                result=cursor.fetchone()
                return result
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def modify_order(self, OrderId:str, Status):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("update pass_order set Status=%s where OrderID=%s", (Status, OrderId,))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def remove_student(self, admission_number):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("delete from student where AdmissionId=%s", (admission_number, ))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def remove_pass(self, uuid4:str):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("delete from pass where UKey=%s", (uuid4, ))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
