import json, sys
from os.path import dirname, abspath

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from models import CategoryModel, UserModel, MoneyModel, UserCategoryModel

# categories
with open('src/script/mocks/categories.json', 'r', encoding='utf-8') as file:
  data_categories = json.load(file)

for category in data_categories:
  CategoryModel().crear(category["name"])

# users
with open('src/script/mocks/users.json', 'r', encoding='utf-8') as file:
  data_users = json.load(file)

for user in data_users:
  UserModel().register(user["username"], bcrypt.generate_password_hash(user["password"]), user["first_name"], user["last_name"], user["birthdate"])

# user_bio
with open('src/script/mocks/biography.json', 'r', encoding='utf-8') as file:
  data_user_bio = json.load(file)

for bio in data_user_bio:
  UserModel().update_bio(bio["username"], bio["biography"])

# user_category_likes
with open('src/script/mocks/user_category.json', 'r', encoding='utf-8') as file:
  data_user_category = json.load(file)

to_insert = []
for user_category in data_user_category:
  to_insert.append((user_category["id_user"], user_category["id_category"]))

UserCategoryModel().create(to_insert)

# money
with open('src/script/mocks/money.json', 'r', encoding='utf-8') as file:
  data_money = json.load(file)

for money in data_money:
  MoneyModel().create(money["id_user"])

for money in data_money:
  MoneyModel().update_quantity(money["id_user"], money["quantity"])

