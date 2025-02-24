from datetime import datetime, date
import json
from random import choice
import string
from uuid import uuid4
import mysql.connector
from mysql.connector import Error

from project.utils.vars import Var

def to_json(result):
    if len(result)==5:
        key_id=4
    else:
        key_id=5
    result=list(result)
    result[key_id]=json.loads(result[key_id])
    return result

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
                    cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s)", (admission_number, name, email, photo, department, password, 0))
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

    def get_pass(self, admid:int=None, key: str=None, regular=None, fromdate=None, todate=None, utype=1):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if admid:
                    if utype==1:
                        cursor.execute("select * from pass where AdmissionId=%s", (admid,))
                    elif utype==2:
                        cursor.execute("select * from staff_pass where Aadhar=%s", (admid,))
                    result=cursor.fetchall()
                elif key:
                    if utype==1:
                        cursor.execute("select * from pass where UKey=%s", (key,))
                    elif utype==2:
                        cursor.execute("select * from staff_pass where UKey=%s", (key,))
                    result=cursor.fetchone()
                elif regular:
                    if utype==1:
                        cursor.execute("select * from pass where (fromtime <= %s AND totime >= %s) ", (fromdate, todate))
                    elif utype==2:
                        cursor.execute("select * from staff_pass where JSON_LENGTH(Traveled) < Days")
                    result=cursor.fetchall()
                if result:
                    if key:
                        result=to_json(result)
                    else:
                        result=map(to_json, result)
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
                    cursor.execute("insert into pass values(%s,%s,%s,%s,%s,%s)", (admid, place, uuid4, fromtime, totime, "[]"))
                elif days:
                    cursor.execute("insert into staff_pass values(%s,%s,%s,%s,%s)", (admid, place, uuid4, days, "[]"))
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

    def get_students(self, utype=0):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if utype==1:
                    cursor.execute("select * from staff")
                else:
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
                    query2="SELECT s.Name, s.Department, po.Days, po.Price, po.Place FROM staff_order po JOIN staff s ON po.email = s.Email WHERE po.Status='PROCESSED' AND (po.Time BETWEEN %s AND %s)"
                    params = [fromdate, todate]
                    if department:
                        query+="AND s.Department = %s"
                        query2+="AND s.Department = %s"
                        params.append(department)
                    cursor.execute(query, params)
                    result=cursor.fetchall()
                    cursor.execute(query2, params)
                    result2=cursor.fetchall()
                    return (result if result else [], result2 if result2 else [])
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

    def remove_student(self, admission_number, utype=1):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if utype==1:
                    cursor.execute("delete from student where AdmissionId=%s", (admission_number, ))
                else:
                    cursor.execute("delete from staff where Aadhar=%s", (admission_number, ))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def remove_pass(self, uuid4:str, utype:int=1):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if utype==1:
                    cursor.execute("delete from pass where UKey=%s", (uuid4, ))
                else:
                    cursor.execute("delete from staff_pass where UKey=%s", (uuid4, ))
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
                code = ''.join(choice(string.digits) for _ in range(6))
                cursor.execute("insert into verification values(%s,%s)", (email, code))
                self.connection.commit()
                return code
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def verify_code(self, email, code):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("select Email from verification where Code=%s AND Email=%s", (code, email))
                result=cursor.fetchone()
                if result:
                    cursor.execute("delete from verification where Email=%s", (result[0],))
                    self.connection.commit()
                    return True
                return False
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def update_pass(self, uuid4:str, date, utype:int=1):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                if utype==1:
                    cursor.execute("select traveled from pass where UKey=%s", (uuid4, ))
                elif utype==2:
                    cursor.execute("select Traveled from staff_pass where UKey=%s", (uuid4, ))
                tickets=list(cursor.fetchone())
                if tickets:
                    tickets=json.loads(tickets[0])
                if not str(date) in tickets:
                    tickets.append(str(date))
                    if utype==1:
                        cursor.execute("update `pass` SET traveled=%s where UKey=%s", (json.dumps(tickets) ,uuid4))
                    elif utype==2:
                        cursor.execute("update `staff_pass` SET Traveled=%s where UKey=%s", (json.dumps(tickets) ,uuid4))
                self.connection.commit()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def gen_otp(self, email: str, utype: str):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute(f"select Email from {utype} where Email=%s", (email, ))
                if not cursor.fetchone():
                    return None
                cursor.execute("delete from forget where Email=%s", (email,))
                otp = ''.join(choice(string.digits) for _ in range(6))
                cursor.execute("insert into forget values(%s,%s,%s)", (email, otp, utype))
                self.connection.commit()
                return otp
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def update_password(self, email, otp, password=None):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("select * from forget where Email=%s and OTP=%s", (email, otp))
                result=cursor.fetchone()
                if result:
                    if password:
                        cursor.execute("delete from forget where Email=%s", (email,))
                        cursor.execute(f"update {result[2]} set Password=%s where Email=%s", (password, email))
                    
                    self.connection.commit()
                    return result
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def email_exist(self, email):
        if self.connection.is_connected():
            try:
                cursor=self.connection.cursor()
                cursor.execute("""SELECT 1 AS Result
    WHERE EXISTS (SELECT 1 FROM admin WHERE Email = %s)
    OR EXISTS (SELECT 1 FROM staff WHERE Email = %s)
    OR EXISTS (SELECT 1 FROM student WHERE Email = %s)""", (email, email, email))
                return cursor.fetchall()
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
