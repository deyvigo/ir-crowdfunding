from flask import Flask, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from routes import genero_blueprint, inversor_blueprint, login_blueprint

import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)

import os
UPLOAD_FOLDER = 'upload_audios'
if not os.path.exists(UPLOAD_FOLDER):
  os.makedirs(UPLOAD_FOLDER)

CORS(app, origins=["http://localhost:5173", "http://localhost:5000"])

app.config["JWT_SECRET_KEY"] = "ir-crowdfunding"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

jwt = JWTManager(app)

bcrypt = Bcrypt(app)

app.register_blueprint(genero_blueprint)
app.register_blueprint(inversor_blueprint)
app.register_blueprint(login_blueprint)

@app.route("/helloworld", methods=["GET"])
def hello_world():
  return { "message": "Hello World" }

@app.route("/upload", methods=["POST"])
def upload_audio():
  if "audio" not in request.files:
    return { "error": "no se ha mandado ningún audio" }, 400
  
  audio_file = request.files["audio"]

  if audio_file.filename == "":
    return { "error": "no selected file" }, 400
  
  file_path = os.path.join(app.config["UPLOAD_FOLDER"], audio_file.filename)
  audio_file.save(file_path)

  # transform to wav
  try:
    audio = AudioSegment.from_file(file_path)
    output_file = "grabac.wav"
    output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_file)
    audio.export(output_path, format="wav")
    return { "message": "enviado correctamente" }, 200
  except:
    return { "error": "error mientras se convertía a wav" }, 500

def transcribe_audio(wav_audio):
  recognizer = sr.Recognizer()
  with sr.AudioFile(wav_audio) as source:
    audio = recognizer.record(source)
    try:
      text = recognizer.recognize_google(audio, language="es-ES")
      return text
    except sr.UnknownValueError:
      return "No se pudo entender el audio"
    except sr.RequestError as e:
      return f"Error en el servicio de reconocimiento de voz; {e}"

@app.route("/transcribe", methods=["GET"])
def transcribe():
  base_dir = os.getcwd()
  file_path = os.path.join(app.config["UPLOAD_FOLDER"], "grabac.wav")
  transcription = transcribe_audio(file_path)
  return { "transcription": transcription }

if __name__ == "__main__":
  app.run(debug=True)
