from utils.connection import Database

class ProjectModel:
  def __init__(self) -> None:
    self.db = Database().connection()

  def __del__(self) -> None:
    if self.db:
      self.db.close()

  def create(self, goal, title, description, instagram, facebook, phone, id_category, id_user, img):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO project (goal, title, description, current_money, instagram, facebook, phone, id_category, id_user, img_project) VALUES (%s, %s, %s, 0, %s, %s, %s, %s, %s, %s)"
      cursor.execute(sql, (goal, title, description, instagram, facebook, phone, id_category, id_user, img))
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
    
  def get_by_id_user(self, id_user):
    cursor = self.db.cursor()
    try:
      sql = """
      SELECT p.id_project, p.goal, p.title, p.instagram, p.facebook, p.description
      FROM project p
      WHERE p.id_user = %s
      """
      cursor.execute(sql, (id_user,))
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al consultar la tabla project: {str(e)}" }
    
  def get_by_id_category(self, id_category):
    cursor = self.db.cursor()
    try:
      sql = "SELECT * FROM project WHERE id_category = %s;"
      cursor.execute(sql, (id_category,))
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al consultar en la tabla project: {str(e)}" }, 500
    
  def update_current_money(self, id_project, amount):
    cursor = self.db.cursor()
    try:
      sql = """
      UPDATE project
      SET current_money = current_money + %s
      WHERE id_project = %s;
      """
      cursor.execute(sql, (amount, id_project))
      self.db.commit()
      return { "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al actualizar en la tabla project: {str(e)}" }, 500
    
  def get_popular(self):
    cursor = self.db.cursor()
    try:
      sql = """
      SELECT upl.id_projects as id_project, p.title, COUNT(upl.id_user) AS likes_count
      FROM user_project_likes upl
      JOIN project p ON upl.id_projects = p.id_project
      GROUP BY upl.id_projects, p.title
      ORDER BY likes_count DESC;
      """
      cursor.execute(sql)
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al consultar en la tabla project: {str(e)}" }, 500
    