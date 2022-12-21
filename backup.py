import mysql.connector
from src.config import settings as s
from database import models
from database.database import get_db
import sqlite3
import os
from datetime import datetime
from pathlib import Path

path_file = Path(__file__)
print(path_file)

mysql_connector = mysql.connector.connect(
    host=s.MYSQL_HOSTNAME,
    user=s.MYSQL_USER,
    password=s.MYSQL_PASSWORD,
    database=s.MYSQL_DATABASE
)

time = datetime.now().strftime("%d-%m-%y_%Hh%Mmin%Ss")
backup_db = s.MYSQL_DATABASE + '_backup'
sqlite_connector = sqlite3.connect(f"database/backups/{backup_db}_{time}.db")
sqlite_cursor = sqlite_connector.cursor()

command = "show tables"

mysql_cursor = mysql_connector.cursor()
mysql_cursor.execute(command)
   
tables = [ table_name[0] for table_name in mysql_cursor ]

try:
    sqlite_cursor.execute(f'CREATE DATABASE {backup_db}')
except:
    pass

create_tables_command = ''
create_items_command = ''

# Criar todas as tabelas
for table in tables:
    command = f"""select * from information_schema.columns
    where table_schema = '{s.MYSQL_DATABASE}'
    and table_name = '{table}'"""
    
    mysql_cursor.execute(command)
    itens = [ item for item in mysql_cursor ]
    
    # montar o comando com todas as colunas da tabela em questao
    elements = []
    for item in itens:
        element = {'tablename': item[2], 'column_name': item[3], 'type': item[7], 'len': item[15]}
        elements.append(element)
        
    columns = [element['column_name'] for element in elements]
    types = [element['type'] for element in elements]
    
    columns_command_with_type = '('
    for i, _ in enumerate(columns):
        columns_command_with_type += f'{columns[i]} {types[i]}, '
    columns_command_with_type = columns_command_with_type[:-2] + ')'
    string_columns_command_with_type = f"{table}{columns_command_with_type}"
    
    columns_command = '('
    i = 0
    for i, _ in enumerate(columns):
        columns_command += f'{columns[i]}, '
    columns_command = columns_command[:-2] + ')'
    string_columns_command = f"{table}{columns_command}"
    
    # Executar o comando e criar a tabelas
    command = f"create table {string_columns_command_with_type}; "
    create_tables_command += command
    
    command = f'select * from {table}'
    
    mysql_cursor.execute(command)
    
    rows = [ item for item in mysql_cursor ]
    for row in rows:
        items_command = '('
        for j, _ in enumerate(row):
            cell = str(row[j])
            items_command += f"'{cell}', "
        items_command = items_command[:-2] + ')'
        
        command = f"INSERT INTO {table} {columns_command} VALUES{items_command}; "
        create_items_command += command


sqlite_cursor.executescript(create_tables_command)
sqlite_cursor.executescript(create_items_command)
