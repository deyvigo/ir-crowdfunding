from utils.connection import Database

class MoneyModel:
  def __init__(self) -> None:
    self.db = Database().connection()

  def __del__(self) -> None:
    if self.db:
      self.db.close()

  # for first creation of user
  def create(self, id_user):
    cursor = self.db.cursor()
    try:
      sql = "INSERT INTO money (id_user, quantity) VALUES (%s, 0);"
      cursor.execute(sql, (id_user,))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al crear en la tabla money: {str(e)}" }, 500
    
  def update_quantity(self, id_user, quantity):
    cursor = self.db.cursor()
    try:
      sql = "UPDATE money SET quantity = %s WHERE id_user = %s;"
      cursor.execute(sql, (quantity, id_user))
      self.db.commit()
      return { "last_row_id": cursor.lastrowid, "row_count": cursor.rowcount }, 200
    except Exception as e:
      return { "error": f"Error al actualizar en la tabla money: {str(e)}" }, 500
    
  def get_by_id_user(self, id_user):
    cursor = self.db.cursor()
    try:
      sql = "SELECT id_register_money, id_user, quantity FROM money WHERE id_user = %s;"
      cursor.execute(sql, (id_user,))
      response = cursor.fetchone()
      return { "data": response }, 200
    except Exception as e:
      return { "error": f"Error al consultar en la tabla money: {str(e)}" }, 500

