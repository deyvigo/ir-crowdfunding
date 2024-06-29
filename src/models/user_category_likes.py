from utils.connection import Database

class UserCategoryModel:
  def __init__(self) -> None:
    self.db = Database().connection()

  def __del__(self) -> None:
    if self.db:
      self.db.close()

  def create(self, user_categories_pairs):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO user_category_likes (id_user, id_category) VALUES (%s, %s);"
      cursor.executemany(sql, user_categories_pairs)
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al crear en la tabla user_category_likes: {str(e)}" }, 500
    
  def get_by_id_user(self, id_user):
    cursor = self.db.cursor()
    try:
      sql = "SELECT id_user_category_likes, id_user, id_category FROM user_category_likes WHERE id_user = %s;"
      cursor.execute(sql, (id_user,))
      response = cursor.fetchall()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al consultar en la tabla user_category_likes: {str(e)}" }, 500