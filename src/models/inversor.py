from utils.connection import Database

class InversorModel:
  def __init__(self):
    self.db = Database().connection()
  
  def __del__(self):
    if self.db:
      self.db.close()

  def registrar_inversor(self, username, password, name, last_name, preferencia, linkedin):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO inversor (username, password, name, last_name, preferencia, linkedin) VALUES (%s, %s, %s, %s, %s, %s)"
      cursor.execute(sql, (username, password, name, last_name, preferencia, linkedin))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }
    except Exception as e:
      return { "error": f"Error al crear en la tabla genero: {str(e)}" }, 500
  
  # Para iniciar sesion
  def get_inversor_by_username(self, username):
    cursor = self.db.cursor()
    try:
      sql = "SELECT * FROM inversor WHERE username = %s"
      cursor.execute(sql, (username,))
      data = cursor.fetchone()
      return { "data": data }
    except Exception as e:
      return { "error": f"Error al crear en la tabla genero: {str(e)}" }, 500