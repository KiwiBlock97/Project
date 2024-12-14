# import mysql.connector
from datetime import datetime, timedelta
# from mysql.connector import Error

# connection = mysql.connector.connect(
#     host="127.0.0.1",
#     user="root",
#     passwd="mysql",
#     database="bus",
#     port="3306"
# )

# cursor=connection.cursor()
# cursor.execute("update pass set totime=%s", (datetime.now().date(),))
# connection.commit()
# result=cursor.fetchone()
# cursor.close()
# print(result)
# # for x in result:
# #     print(type(x), ": ", x)
# connection.close()

a=datetime.now().date()
b=datetime.strptime("2024-12-14", "%Y-%m-%d").date()
print(str(a+timedelta(days=1)))
print(b)
print(b<a)
print(bool(b<=a))