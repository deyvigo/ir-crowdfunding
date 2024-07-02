from utils.connection import Database

class UserProjectsModel:
  def __init__(self) -> None:
    self.db = Database().connection()

  def __del__(self) -> None:
    if self.db:
      self.db.close()

  def create(self, id_user, id_project):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO user_project_likes (id_user, id_projects) VALUES (%s, %s);"
      cursor.execute(sql, (id_user, id_project))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al crear en la tabla user_projects: {str(e)}" }, 500
    
  def delete_by_id(self, id_user, id_project):
    cursor = self.db.cursor()
    try:
      sql = "DELETE FROM user_project_likes WHERE id_user = %s AND id_projects = %s;"
      cursor.execute(sql, (id_user, id_project))
      self.db.commit()
      return { "affected_rows": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al eliminar en la tabla user_projects: {str(e)}" }, 500
    
  def get_by_id_user_and_project(self, id_user, id_project):
    cursor = self.db.cursor()
    try:
      sql = "SELECT * FROM user_project_likes WHERE id_user = %s AND id_projects = %s"
      cursor.execute(sql, (id_user, id_project))
      response = cursor.fetchone()
      return response
    except Exception as e:
      return { "error": f"Error al consultar en la tabla user_projects: {str(e)}" }, 500
    
  def is_liked(self, id_project, id_user):
    cursor = self.db.cursor()
    try:
      sql = """
      SELECT * FROM user_project_likes
      WHERE id_user = %s AND id_projects = %s;
      """
      cursor.execute(sql, (id_user, id_project))
      response = cursor.fetchone()
      return response
    except Exception as e:
      return { "error": f"Error al consultar en la tabla user_projects: {str(e)}" }, 500