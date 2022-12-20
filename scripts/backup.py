import mysql.connector

db=mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

cursor=db.cursor()

cursor.execute("SHOW TABLES")
   
tables = [ table_name[0] for table_name in cursor ]

datas = {}
for table in tables:
    cursor.execute(f"Select * from flow.`{table}`")
    itens = [ item for item in cursor ]
    data = {table: itens}
    datas.update(data)

print(datas)