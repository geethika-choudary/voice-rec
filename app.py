"""
The flask application package.
"""
from flask import Flask
from pydub import AudioSegment
import os

app = Flask(__name__)
wsgi_app = app.wsgi_app #Registering with IIS

os.environ["PATH"]+="/Users/cb/voice-recognition/voice-recognition/ffmpeg"

AudioSegment.converter = "/Users/cb/voice-recognition/voice-recognition/ffmpeg"
AudioSegment.ffmpeg = "/Users/cb/voice-recognition/voice-recognition/ffmpeg/ffmpeg"
AudioSegment.ffprobe ="/Users/cb/voice-recognition/voice-recognition/ffmpeg/ffprobe"

#import views
import Speaker_Enrollment
import Speaker_Authentication