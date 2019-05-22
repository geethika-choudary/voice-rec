import os
import time
from pydub import AudioSegment
from pydub.utils import make_chunks
import subprocess
from pydub.utils import which
AudioSegment.converter = './ffmpeg/ffmpeg'
#from ffprobe import FFProbe
AudioSegment.ffmpeg = "./ffmpeg"
#AudioSegment.converter = "./env/lib/python3.6/site-packages/pydub"
#AudioSegment.converter = "/usr/local/bin/ffmpeg"
#os.environ["PATH"]+="./env/lib/python3.6/site-packages/ffprobe"

#To split a single audio file into 15 different files
def audio_split(filename, isMP3):
    if isMP3:
        myaudio = AudioSegment.from_wav("./uploads/" +filename) 
    else:
        myaudio = AudioSegment.from_wav("./audio_sources/" +filename) 

    chunk_length_ms = 4000 
    chunks = make_chunks(myaudio, chunk_length_ms) 
    direflaskctory_name=os.path.splitext(filename)[0]
    #os.mkdir("./uploads")
    #*********************#
    #Iterating through chunks
    #Export all the individual chunks as wav files into the speaker's directory 
    for i, chunk in enumerate(chunks):
        chunk_name = os.path.splitext(filename)[0]+"_{0}.wav".format(i)
        print("exporting", chunk_name)
        chunk.export("./uploads/"+chunk_name, format="wav") 

def mp3toWav(fname, replace_filename, sourceDir, destDir):
    subprocess.call([AudioSegment.converter, '-i', sourceDir + '/' + fname, destDir + '/' +replace_filename])
    #AudioSegment.from_mp3(sourceDir + "/" + fname).export(destDir + "/" + replace_filename, format="wav")
    '''src="./audio_sources/" + fname
    dst="./audio_sources/" + replace_filename
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")'''