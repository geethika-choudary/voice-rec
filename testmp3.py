import subprocess
import os

from pydub import AudioSegment

from pydub import AudioSegment
from pydub.utils import which
AudioSegment.converter = './ffmpeg/ffmpeg'
#AudioSegment.ffmpeg = "/Users/cb/ffmpeg"
#print("************** ",AudioSegment.converter)
#AudioSegment.converter = which("ffmpeg")
#print("ABC   ",AudioSegment.converter)
#print("****** " ,os.environ)
subprocess.call([AudioSegment.converter, '-i', 'aryan.mp3', 'output.wav'])