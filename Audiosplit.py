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


#To split a single audio file into 15 different files
def audio_split(filename, isMP3):
    envdir_list = [os.curdir] + os.environ["PATH"].split(os.pathsep)
    print("******************",envdir_list)
    if isMP3:
        myaudio = AudioSegment.from_wav("./audio_sources/" +filename) 
    else:
        myaudio = AudioSegment.from_wav("./audio_sources/" +filename) 

    chunk_length_ms = 4000 
    chunks = make_chunks(myaudio, chunk_length_ms) 
    direflaskctory_name=os.path.splitext(filename)[0]
    
    #Iterating through chunks
    #Export all the individual chunks as wav files into the speaker's directory 
    for i, chunk in enumerate(chunks):
        chunk_name = os.path.splitext(filename)[0]+"_{0}.wav".format(i)
        print("exporting", chunk_name)
        chunk.export("./uploads/"+chunk_name, format="wav") 

def mp3toWav(fname, replace_filename, sourceDir, destDir):
    subprocess.call([AudioSegment.converter, '-i', sourceDir + '/' + fname, destDir + '/' +replace_filename])
    #AudioSegment.from_mp3(sourceDir + "/" + fname).export(destDir + "/" + replace_filename, format="wav")

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
    #samplingRate=int(argv[2])
    #channels=int(argv[3])
    for f in files:
        e = destDir + os.path.splitext(rf)[0] +  '.wav'
        wavPath = 'avconv -y -i  ' + '\"' + f + '\"' + ' -ar ' + str(samplingRate) + ' -ac ' + str(channels) + ' '  + e
        os.system(wavPath)
