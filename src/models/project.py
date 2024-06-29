from utils.connection import Database

class ProjectModel:
  def __init__(self) -> None:
    self.db = Database().connection()

  def __del__(self) -> None:
    if self.db:
      self.db.close()

  def create(self, goal, title, description, instagram, facebook, phone, id_category, id_user):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO project (goal, title, description, current_money, instagram, facebook, phone, id_category, id_user) VALUES (%s, %s, %s, 0, %s, %s, %s, %s, %s)"
      cursor.execute(sql, (goal, title, description, instagram, facebook, phone, id_category, id_user))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al crear en la tabla project: {str(e)}" }, 500
    
  def get_all(self):
    cursor = self.db.cursor()
    try:
      sql = "SELECT * FROM project;"
      cursor.execute(sql)
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al consultar en la tabla project: {str(e)}" }, 500
    
  def get_by_id(self, id_project):
    cursor = self.db.cursor()
    try:
      sql = "SELECT * FROM project WHERE id_project = %s;"
      cursor.execute(sql, (id_project,))
      response = cursor.fetchone()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al consultar en la tabla project: {str(e)}" }, 500
    