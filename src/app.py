from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from routes import genero_blueprint, inversor_blueprint

app = Flask(__name__)

bcrypt = Bcrypt(app)
CORS(app)

app.register_blueprint(genero_blueprint)
app.register_blueprint(inversor_blueprint)

if __name__ == "__main__":
  app.run(debug=True)
