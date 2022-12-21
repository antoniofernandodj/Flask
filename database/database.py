import logging
from os import getpid
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings as s

from . import models

from .bcolors import bcolors


def get_db():
    DATABASE_URL =  f'mysql+mysqlconnector://{s.MYSQL_USER}:{s.MYSQL_PASSWORD}' + \
                    f'@{s.MYSQL_HOSTNAME}:{s.MYSQL_PORT}/{s.MYSQL_DATABASE}'
                        
    loop = True
    while loop:
        try:
            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            print(bcolors.ok("Conexão com banco de dados realizada com sucesso"))
            loop = False
        except Exception as error:
            print(bcolors.fail("Conexão com banco de dados falhou"))
            print(f"Erro: {error}")
            sleep(2)
    try:
        db = SessionLocal()
        return db
    except Exception as e:
        print(e)
        
def init_tables():
    
    DATABASE_URL =  f'mysql+mysqlconnector://{s.MYSQL_USER}:{s.MYSQL_PASSWORD}' + \
                    f'@{s.MYSQL_HOSTNAME}:{s.MYSQL_PORT}/{s.MYSQL_DATABASE}'
                    
    print(bcolors.warning("Checando as tabelas e criando as que não existam..."))
    loop = True
    while loop:        
        try:
            engine = create_engine(DATABASE_URL)
            models.Base.metadata.create_all(bind=engine)
            loop = False
            msg = f"Checagem concluída!"
            print(bcolors.ok(msg))
        except Exception as error:
            msg = f"Conexão com banco de dados falhou"
            print(bcolors.fail(f"{msg}. Erro: {error}"))
            sleep(2)