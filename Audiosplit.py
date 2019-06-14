import time
from pydub import AudioSegment
from pydub.utils import make_chunks
import subprocess
from pydub.utils import which
# Commented
#AudioSegment.converter = './ffmpeg/ffmpeg'
#from ffprobe import FFProbe
#Commented
#AudioSegment.ffmpeg = "./ffmpeg"
#AudioSegment.converter = "./env/lib/python3.6/site-packages/pydub"
#AudioSegment.converter = "/usr/local/bin/ffmpeg"
#os.environ["PATH"]+="./env/lib/python3.6/site-packages/ffprobe"
import os,shutil
from flask import Flask,redirect,url_for,jsonify,flash,request,render_template,send_from_directory
from werkzeug import secure_filename
import wave, struct
import uuid
import json
import glob, sys
import wave
import contextlib

#To split a single audio file into 15 different files
def audio_split(filename, isMP3, sourceDir,chunk_length_ms):
    """
    #Calculating the length of each chunk depepnding upon the input file
    with contextlib.closing(wave.open(sourceDir + filename,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    chunk_length_ms=duration/15
    chunk_length_ms=int(chunk_length_ms)*1000
    """

    if isMP3:
        myaudio = AudioSegment.from_wav(sourceDir +filename) 
    else:
        myaudio = AudioSegment.from_wav(sourceDir +filename) 

    chunks = make_chunks(myaudio, chunk_length_ms) 
    direflaskctory_name=os.path.splitext(filename)[0]
    
    #Iterating through chunks
    #Export all the individual chunks as wav files into the speaker's directory 
    for i, chunk in enumerate(chunks):
        chunk_name = os.path.splitext(filename)[0]+"_{0}.wav".format(i)
        print("exporting", chunk_name)
        chunk.export("./uploads/"+chunk_name, format="wav") 



def convertTowav(sourceDir,dirPath):
    dirPath_new = sourceDir + dirPath
    types = (dirPath+os.sep+'*.avi', dirPath+os.sep+'*.mkv', dirPath+os.sep+'*.mp4', dirPath_new, dirPath+os.sep+'*.flac', dirPath+os.sep+'*.ogg')
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))
    return files_grabbed

def getWavfile(samplingRate,channels,filename,replace_filename,sourceDir,destDir):
    files=convertTowav(sourceDir,filename)
    rf=replace_filename
    for f in files:
        e = destDir + os.path.splitext(rf)[0] +  '.wav'
        wavPath = 'avconv -y -i  ' + '\"' + f + '\"' + ' -ar ' + str(samplingRate) + ' -ac ' + str(channels) + ' '  + e
        os.system(wavPath)
