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
  def get_by_username_for_login(self, username):
    cursor = self.db.cursor()
    try:
      sql = "SELECT id_user, username, password, first_name, last_name FROM user WHERE username = %s"
      cursor.execute(sql, (username,))
      data = cursor.fetchone()
      return { "data": data }, 200
    except Exception as e:
      return { "error": f"Error al consultar tabla user: {str(e)}" }, 500
    
  def update_bio(self, username, biography):
    cursor = self.db.cursor()
    try:
      sql = """
      UPDATE user 
        SET biography = %s,
            paypal = 'paypal'
      WHERE username = %s;
      """
      cursor.execute(sql, (biography, username))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al actualizar tabla user: {str(e)}" }, 500
    
  def update_linkedin(self, username, linkedin):
    cursor = self.db.cursor()
    try:
      sql = """
      UPDATE user 
        SET linkedin = %s,
            paypal = 'paypal'
      WHERE username = %s;
      """
      cursor.execute(sql, (linkedin, username))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al actualizar tabla user: {str(e)}" }, 500
    
  def get_by_id(self, id_user):
    cursor = self.db.cursor()
    try:
      sql = "SELECT id_user, username, first_name, last_name, img_user, biography, created, birthday, paypal, linkedin FROM user WHERE id_user = %s;"
      cursor.execute(sql, (id_user,))
      response = cursor.fetchone()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al consultar tabla user: {str(e)}"}, 500
    
  def get_all_info_by_id(self, id_user):
    cursor = self.db.cursor()
    try:
      sql = """
      SELECT u.id_user, u.username, u.first_name, u.img_user, u.last_name, u.biography, u.created, u.birthday, u.paypal, u.linkedin, m.quantity
      FROM user u
      JOIN money m ON m.id_user = u.id_user
      WHERE u.id_user = %s;
      """
      cursor.execute(sql, (id_user,))
      response = cursor.fetchone()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al consultar tabla user: {str(e)}"}, 500
    
  def get_by_username(self, username):
    cursor = self.db.cursor()
    try:
      sql = "SELECT id_user, first_name, last_name, img_user, biography, created, birthday, linkedin FROM user WHERE username = %s;"
      cursor.execute(sql, (username,))
      response = cursor.fetchone()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al actualizar tabla user: {str(e)}"}, 500
    
  def update_img(self, id_user, img):
    cursor = self.db.cursor()
    try:
      sql = """
      UPDATE user
        SET img_user = %s
      WHERE id_user = %s;
      """
      cursor.execute(sql, (img, id_user))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al actualizar tabla user: {str(e)}" }, 500

  