from utils.connection import Database

class CategoryModel:
  def __init__(self):
    self.db = Database().connection()

  def __del__(self):
    if self.db:
      self.db.close()

  def crear(self, category):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO category (name) VALUE (%s);"
      cursor.execute(sql, (category,))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except:
      return { "error": "Error al crear en la tabla category" }, 500
    
  def get_all(self):
    cursor = self.db.cursor()
    try:
      cursor.execute("SELECT id_category, name FROM category;")
      data = cursor.fetchall()
      return { "data": data }, 200
    except:
      return { "error": "Error al consultar la tabla category" }, 500