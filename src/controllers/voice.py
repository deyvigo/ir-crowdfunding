from flask import request, current_app
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

from pydub import AudioSegment
import speech_recognition as sr
import os

class VoiceController:
  @staticmethod
  def upload_audio():
    if "audio" not in request.files:
      return { "error": "no se ha mandado ningún audio" }, 400
    
    audio_file = request.files["audio"]

    if audio_file.filename == "":
      return { "error": "no selected file" }, 400
    
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], audio_file.filename)
    audio_file.save(file_path)

    # transform to wav
    try:
      audio = AudioSegment.from_file(file_path)
      output_file = "grabac.wav"
      output_path = os.path.join(current_app.config["UPLOAD_FOLDER"], output_file)
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
      
  @staticmethod
  def transcribe():
    base_dir = os.getcwd()
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], "grabac.wav")
    transcription = VoiceController.transcribe_audio(file_path)

    if transcription.lower() == 'no se pudo entender el audio':
      return { "error": "no se pudo entender el audio" }, 400
    
    # openai api
    api_key = os.getenv("OPENAI_API_KEY")

    openai = OpenAI(api_key=api_key)

    intial = """Eres un asistente de una paǵina web y tienes solo estas rutas a las que puedes acceder.
    /main/buscar
    /main/crear
    /main/inicio
    /main/recargar
    /main/recomendados

    /main/buscar es un buscador de proyectos, /main/crear en para crear un nuevo proyecto, /main/inicio es para editar perfil, /main/recargar es para comprar las monedas de la página, /main/recomendados, es para los proyectos recomendados.

    Según lo siguiente: """

    prompt = transcription

    final = """Quiero que me mandes a una de las rutas. Solo respóndeme con un json de la siguiente forma { link: link }
    En caso de que la ruta sea /main/crear quiero que mandes una respuesta de la siguiente forma { link: link, title: title, description: description, goal: goal}
    goal es solo un número entero.
    """

    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": intial},
        {"role": "user", "content": prompt},
        {"role": "user", "content": final}
      ],
    )

    print(response.choices[0].message.content)

    relink = response.choices[0].message.content

    return relink, 200