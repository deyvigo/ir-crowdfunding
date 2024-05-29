from utils.connection import Database

class GeneroModel:
  def __init__(self):
    self.db = Database().connection()

  def __del__(self):
    if self.db:
      self.db.close()

  def registrar_genero(self, genero):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO genero (nombre_genero) VALUE (%s);"
      cursor.execute(sql, (genero))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }
    except:
      return { "error": "Error al crear en la tabla genero" }, 500
    
  def get_all_generos(self):
    cursor = self.db.cursor()
    try:
      cursor.execute("SELECT * FROM genero;")
      data = cursor.fetchall()
      return { "data": data }
    except:
      return { "error": "Error al consultar la tabla genero" }, 500