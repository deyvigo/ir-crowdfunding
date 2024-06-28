from flask import Blueprint
from controllers import VoiceController

voice_blueprint = Blueprint("voice", __name__)

@voice_blueprint.route("/upload", methods=["POST"])
def upload():
  return VoiceController.upload_audio()

@voice_blueprint.route("/transcribe", methods=["GET"])
def transcribe():
  return VoiceController.transcribe()