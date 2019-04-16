import os
from pydub import AudioSegment
from pydub.utils import make_chunks
#from ffprobe import FFProbe
AudioSegment.ffmpeg = "./env/Lib/site-packages/pydub"



#To split a single audio file into 15 different files
def audio_split(filename):
    #myaudio = AudioSegment.from_file("./audio-source/" +filename , "wav")
    myaudio = AudioSegment.from_wav("./audio_sources/" +filename) 
    chunk_length_ms = 4000 
    chunks = make_chunks(myaudio, chunk_length_ms) 
    directory_name=os.path.splitext(filename)[0]
    #os.mkdir("./uploads")

    #Iterating through chunks
    #Export all the individual chunks as wav files into the speaker's directory 
    for i, chunk in enumerate(chunks):
        chunk_name = os.path.splitext(filename)[0]+"_{0}.wav".format(i)
        print("exporting", chunk_name)
        chunk.export("./uploads/"+chunk_name, format="wav") 

def mp3toWav(fname, replace_filename):
        src="./audio_sources/" + fname
        dst="./audio_sources/" + replace_filename
        sound = AudioSegment.from_mp3(fname)
        sound.export(dst, format="wav")
