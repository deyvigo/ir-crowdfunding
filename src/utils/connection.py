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
        create table category
        (
          id_category int auto_increment
            primary key,
          name        varchar(100) not null
        );
      """)
      cursor.execute("""
        create table user
        (
          id_user    int auto_increment
            primary key,
          img_user   varchar(255) null,
          username   varchar(40)  not null,
          password   varchar(80)  not null,
          first_name varchar(200) not null,
          last_name  varchar(200) not null,
          biography  text         null,
          created    date         not null,
          birthday   date         not null,
          paypal     varchar(300) null,
          linkedin   varchar(300) null
        );
      """)
      cursor.execute("""
        create table money
        (
          id_register_money int auto_increment
            primary key,
          id_user           int not null,
          quantity          int not null,
          constraint money_user_id_user_fk
            foreign key (id_user) references user (id_user)
        );
      """)
      cursor.execute("""
        create table project
        (
          id_project    int auto_increment
            primary key,
          img_project   varchar(255) null,
          goal          int          not null,
          title         varchar(300) not null,
          description   text         not null,
          current_money int          not null,
          instagram     varchar(200) not null,
          facebook      varchar(200) not null,
          phone         varchar(15)  not null,
          id_category   int          not null,
          id_user       int          not null,
          constraint project_category_id_category_fk
            foreign key (id_category) references category (id_category),
          constraint project_user_id_user_fk
            foreign key (id_user) references user (id_user)
        );
      """)
      cursor.execute("""
        create table comment
        (
          id_comment int auto_increment
            primary key,
          comment    text not null,
          id_project int  not null,
          id_user    int  not null,
          constraint comment_project_id_project_fk
            foreign key (id_project) references project (id_project),
          constraint comment_user_id_user_fk
            foreign key (id_user) references user (id_user)
        );
      """)
      cursor.execute("""
        create table user_category_likes
        (
          id_user_category_likes int auto_increment
            primary key,
          id_category            int not null,
          id_user                int not null,
          constraint user_category_likes_category_id_category_fk
            foreign key (id_category) references category (id_category),
          constraint user_category_likes_user_id_user_fk
            foreign key (id_user) references user (id_user)
        );
      """)
      cursor.execute("""
        create table user_project_likes
        (
          id_user_project_likes int auto_increment
            primary key,
          id_user               int not null,
          id_projects           int not null,
          constraint user_project_likes_project_id_project_fk
            foreign key (id_projects) references project (id_project),
          constraint user_project_likes_user_id_user_fk
            foreign key (id_user) references user (id_user)
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