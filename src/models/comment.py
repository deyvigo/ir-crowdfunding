from utils.connection import Database

class CommentModel:
  def __init__(self) -> None:
    self.db = Database().connection()
  
  def __del__(self) -> None:
    if self.db:
      self.db.close()

  def post_comment(self, id_user, id_project, comment):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO comment (id_user, id_project, comment) VALUES (%s, %s, %s);"
      cursor.execute(sql, (id_user, id_project, comment))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al crear en la tabla comment: {str(e)}" }, 500
    
  def get_all_by_id_project(self, id_project):
    cursor = self.db.cursor()
    try:
      sql = "SELECT * FROM comment WHERE id_project = %s;"
      cursor.execute(sql, (id_project,))
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al consultar en la tabla comment: {str(e)}" }, 500
    
  def get_by_id(self, id_comment):
    cursor = self.db.cursor()
    try:
      sql = "SELECT * FROM comment WHERE id_comment = %s;"
      cursor.execute(sql, (id_comment,))
      response = cursor.fetchone()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al consultar en la tabla comment: {str(e)}" }, 500