import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".enviromentvars")

class Database:
  def __init__(self):
    db = self.connection()
    try:
      cursor = db.cursor()
      cursor.execute("SHOW TABLES;")
      db_tables = cursor.fetchall()
      if (db_tables.__len__() > 0):
        print("Las tablas ya están creadas.")
      else:
        self.create_tables()
    except Exception as e:
      print(f"Error durante la creación de las tablas. (constructor) {e}")
    finally:
      db.close()

  def create_tables (self):
    db = self.connection()
    try:
      cursor = db.cursor()
      cursor.execute("""
        create table if not exists genero
        (
          id_genero     int auto_increment
            primary key,
          nombre_genero varchar(100) not null
        );
      """)
      cursor.execute("""
        create table if not exists inversor
        (
          id_inversor int auto_increment
            primary key,
          name        varchar(200) not null,
          username    varchar(20)  not null,
          last_name   varchar(200) not null,
          password    varchar(80)  not null,
          preferencia varchar(100) not null,
          linkedin    varchar(300) not null
        );
      """)
      cursor.execute("""
        create table if not exists solicitante
        (
          id_solicitante int auto_increment
            primary key,
          name           varchar(200) not null,
          last_name      varchar(200) not null,
          password       varchar(80)  not null,
          phone          varchar(12)  not null,
          username       varchar(20)  not null,
          paypal         varchar(100) not null,
          linkedin       varchar(300) not null
        );
      """)
      cursor.execute("""
        create table if not exists post
        (
          id_post        int auto_increment
            primary key,
          title          varchar(200) not null,
          body           text         not null,
          goal           int          not null,
          url_img        varchar(300) null,
          id_genero      int          not null,
          id_solicitante int          not null,
          constraint post_genero_id_genero_fk
            foreign key (id_genero) references genero (id_genero),
          constraint post_solicitante_id_solicitante_fk
            foreign key (id_solicitante) references solicitante (id_solicitante)
        );
      """)
      cursor.execute("""
        create table if not exists post_inversor
        (
          id_post_inversor int auto_increment
            primary key,
          id_inversor      int not null,
          id_post          int not null,
          constraint post_inversor_inversor_id_inversor_fk
            foreign key (id_inversor) references inversor (id_inversor),
          constraint post_inversor_post_id_post_fk
            foreign key (id_post) references post (id_post)
        );
      """)
    except Exception as e:
      print(f"Error durante la creación de las tablas {e}")
    finally:
      db.close()

  def connection (self):
    db = pymysql.connections.Connection(
      host=os.getenv("DATABASE_HOST"),
      database=os.getenv("DATABASE_NAME"),
      user=os.getenv("DATABASE_USER"),
      password=os.getenv("DATABASE_PASSWORD"),
      port=3306,
      cursorclass=pymysql.cursors.DictCursor
    )
    return db