from utils.connection import Database

class UserModel:
  def __init__(self):
    self.db = Database().connection()
  
  def __del__(self):
    if self.db:
      self.db.close()

  def register(self, username, password, first_name, last_name, birthday):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO user (username, password, first_name, last_name, birthday, created) VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)"
      cursor.execute(sql, (username, password, first_name, last_name, birthday))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al crear en la tabla user: {str(e)}" }, 500
  
  # Para iniciar sesion
  def get_by_username(self, username):
    cursor = self.db.cursor()
    try:
      sql = "SELECT id_user, username, password FROM user WHERE username = %s"
      cursor.execute(sql, (username,))
      data = cursor.fetchone()
      return { "data": data }, 200
    except Exception as e:
      return { "error": f"Error al consultar tabla user: {str(e)}" }, 500
    
  def update_rows(self, username, biography, paypal, linkedin):
    cursor = self.db.cursor()
    try:
      sql = """
      UPDATE user 
        SET biography = %s,
            paypal = %s,
            linkedin = %s
      WHERE username = %s;
      """
      cursor.execute(sql, (biography, paypal, linkedin, username))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al actualizar tabla user: {str(e)}" }, 500
  