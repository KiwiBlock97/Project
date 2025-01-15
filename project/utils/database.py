from datetime import datetime, date
from uuid import uuid4
import mysql.connector
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
        except Error as e:
            print(f"The error '{e}' occurred")

    def create_user(self, admission_number, name, email, photo, department, password, user_type):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if user_type=="Student":
                    cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s)", (admission_number, name, email, photo, department, password, 0))
                elif user_type=="Staff":
                    cursor.execute("insert into staff values(%s,%s,%s,%s,%s,%s,%s)", (admission_number, name, email, photo, department, password, 0))
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
                cursor.execute("select AdmissionId, Verified, Name from student where Email=%s and Password=%s", (email, password))
                result=cursor.fetchone()
                if result:
                    return result, "Student"

                cursor.execute("select Email from admin where Email=%s and Password=%s", (email, password))
                result=cursor.fetchone()
                if result:
                    return result, "Admin"

                cursor.execute("select Aadhar, Verified, Name from staff where Email=%s and Password=%s", (email, password))
                result=cursor.fetchone()
                if result:
                    return result, "Staff"
                return None, None
            except Exception as e:
                print(e)
            finally:
                cursor.close()
    
    def get_user(self, email: str = None, admid: int = None, user_type: str = "Student"):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if admid:
                    if user_type=="Student":
                        cursor.execute("select * from student where AdmissionId=%s", (admid,))
                    elif user_type=="Staff":
                        cursor.execute("select * from staff where Aadhar=%s", (admid,))
                elif user_type=="Admin":
                    cursor.execute("select * from admin where Email=%s", (email,))
                elif user_type=="Student":
                    cursor.execute("select * from student where Email=%s", (email,))
                elif user_type=="Staff":
                    cursor.execute("select * from staff where Email=%s", (email,))
                result=cursor.fetchone()
                return result
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def get_pass(self, admid:int=None, key: str=None, regular=None, fromdate=None, todate=None, type=1):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if admid:
                    if type==1:
                        cursor.execute("select * from pass where AdmissionId=%s", (admid,))
                    elif type==2:
                        cursor.execute("select * from staff_pass where Aadhar=%s", (admid,))
                    result=cursor.fetchall()
                elif key:
                    if type==1:
                        cursor.execute("select * from pass where UKey=%s", (key,))
                    elif type==2:
                        cursor.execute("select * from staff_pass where UKey=%s", (key,))
                    result=cursor.fetchone()
                elif regular:
                    cursor.execute("select * from pass where (fromtime <= %s AND totime >= %s) ", (fromdate, todate))
                    result=cursor.fetchall()
                return result
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def create_pass(self, admid: int, place: str, uuid4:str, fromtime: date=None, totime:date=None, days: int=0):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if fromtime:
                    cursor.execute("insert into pass values(%s,%s,%s,%s, %s)", (admid, place, uuid4, fromtime, totime))
                elif days:
                    cursor.execute("insert into staff_pass values(%s,%s,%s,%s, %s)", (admid, place, uuid4, days, 0))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def extend_pass(self, todate: date, UKey: str):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("update pass set totime=%s where UKey=%s", (todate, UKey))
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

    def create_order(self, OrderId:str, email: str, place: str, fromtime: str=None, totime: str=None, renew: int=None, ukey:str=None, status: str=None, price: int=0, days: int=None):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if fromtime:
                    cursor.execute("insert into pass_order values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (OrderId, email, place, fromtime, totime, renew, ukey, datetime.now().date(), status, price))
                elif days:
                    cursor.execute("insert into staff_order values(%s, %s, %s, %s, %s, %s, %s)", (OrderId, email, place, days, datetime.now().date(), status, price))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def get_order(self, OrderId:str= None, fromdate=None, todate=None, department=None, utype: int=1):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if OrderId:
                    if utype==1:
                        cursor.execute("select * from pass_order where OrderID=%s", (OrderId,))
                    elif utype==2:
                        cursor.execute("select * from staff_order where OrderID=%s", (OrderId,))
                    result=cursor.fetchone()
                    return result
                else:
                    query="SELECT s.Name, s.Department, po.fromtime, po.totime, po.Price, po.Place FROM pass_order po JOIN student s ON po.email = s.Email WHERE po.Status='PROCESSED' AND (po.Time BETWEEN %s AND %s)"
                    params = [fromdate, todate]
                    if department:
                        query+="AND s.Department = %s"
                        params.append(department)
                    cursor.execute(query, params)
                    result=cursor.fetchall()
                    return result if result else []
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def modify_order(self, OrderId:str, Status, utype: int=1):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if utype==1:
                    cursor.execute("update pass_order set Status=%s where OrderID=%s", (Status, OrderId,))
                elif utype==2:
                    cursor.execute("update staff_order set Status=%s where OrderID=%s", (Status, OrderId,))
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

    def get_departments(self):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("select * from departments")
                result=cursor.fetchall()
                return result
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def remove_department(self, department:str):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("delete from departments where department=%s", (department,))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def add_department(self, department:str):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("insert into departments values(%s)", (department, ))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def gen_code(self, email):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("delete from verification where Email=%s", (email,))
                code=str(uuid4())
                cursor.execute("insert into verification values(%s,%s)", (email, code))
                self.connection.commit()
                return code
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def verify_code(self, code):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("select Email from verification where Code=%s", (code, ))
                result=cursor.fetchone()
                if result:
                    cursor.execute("delete from verification where Email=%s", (result[0],))
                    cursor.execute("update student set Verified=1 where Email=%s", (result[0], ))
                    self.connection.commit()
                    return True
                return False
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
