import os,shutil
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture 
from sklearn import mixture
from Feature_Extraction import extract_features
import warnings         
warnings.filterwarnings("ignore")
from flask import Flask,redirect,url_for,jsonify,flash,request,render_template,send_from_directory
from werkzeug import secure_filename
from Model_Train import model_train
from Audiosplit import audio_split,convertTowav,getWavfile
from app import app
import wave, struct
import uuid
import json
import subprocess
import glob, sys
from subprocess import Popen, PIPE


UPLOAD_FOLDER = './audio_sources/'
ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'mp4'])

#app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def start():
    return "Welcome"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        personname = request.form['personname']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            guid = str(uuid.uuid1()).replace("-", "")
            replace_filename = str(personname).replace(" ", "") + '-' + str(guid) + '.wav'
            isMP3 = False

            if filename.endswith(".mp3"):
                isMP3 = True
                file.save(os.path.join('audio_sources',secure_filename(file.filename)))
                #mp3toWav(filename, replace_filename, "./audio_sources", "./uploads")
                getWavfile(8000,1,filename,replace_filename,"./audio_sources/","./audio_sources/")

            else:
                file.save(os.path.join('audio_sources',secure_filename(file.filename)))

            #rename file name
            #os.rename('./audio_sources/' + filename, './audio_sources/' + replace_filename)            
            audio_split(replace_filename, isMP3)
            training_result = model_train(replace_filename)
            responseJson = {}
            appurl = request.url.split("/upload")

            if training_result == "Modelling completed":
                responseJson = jsonify(
                            status = 200,
                            message = "Enrollment Successful",
                            guid = str(guid),
                            name = personname,
                            link =  appurl[0] + "/audiofile/" + replace_filename
                        )
            else: 
                responseJson = jsonify(
                            status = 500,
                            message = "Enrollment Failed",
                            guid = str(guid),
                            name = personname
                        )
            return responseJson
    return '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form action="" method=post enctype=multipart/form-data>
<p><input type=file name=file>
Person Name: <input type=text name=personname value="john david">
<input type=submit value=Upload>
</form>
'''

@app.route('/logindelete')
def index():
   return render_template('delete.html')

#To automatically delete the files when app gets heavy
@app.route('/handle_delete',methods = ['POST', 'GET'])
def handle_delete():
    inputFolder = request.form['inputFolder']
    if inputFolder=="all":
        folder_paths=['./uploads','./audio_sources','./test_samples']
        for folder in folder_paths:
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if the_file.endswith(".wav") or the_file.endswith(".mp3"):
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                except Exception as e:
                    print(e)

    else:
        inputFolder = "./" + request.form['inputFolder']
        for the_file in os.listdir(inputFolder):
            file_path = os.path.join(inputFolder, the_file)
            try:
                if the_file.endswith(".wav") or the_file.endswith(".gmm") or the_file.endswith(".mp3"):
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
            except Exception as e:
                print(e)
    return("***Deleted files***")

@app.route('/delete', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('delete_login.html', error=error)



@app.route('/queryenrolledfiles', methods=['GET'])
def queryaudiofiles():
    error = None
    filesArr = []

    folder_paths=['./Speakers_models']
    for folder in folder_paths:
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if the_file.endswith(".gmm"):
                    if os.path.isfile(file_path):
                        fileNameArr = the_file.split(".gmm")[0].split("-")
                        appurl = request.url.split("/queryenrolledfiles") 
                        link = appurl[0] + "/audiofile/" + fileNameArr[0] + "-" + fileNameArr[1] + ".wav"
                        filesArr.append({ "name": fileNameArr[0], "guid": fileNameArr[1], "link" : link })
            except Exception as e:
                print(e)
    print(filesArr)
    if(len(filesArr) > 0 ):
        responseJson = jsonify(data = filesArr)
    else:
        responseJson = jsonify(data =  [])

    return responseJson


@app.route('/audiofile/<path:fname>',methods=['GET','POST'])
def get_file(fname):
    return send_from_directory(directory = "./audio_sources", filename = fname)





#if __name__ == "__main__":
#app.run(debug=True)