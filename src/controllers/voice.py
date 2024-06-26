from flask import request, current_app

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
    return { "transcription": transcription.lower() }