import os
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture 
from Feature_Extraction import extract_features
import warnings
warnings.filterwarnings("ignore")
import time
import sklearn.mixture.gaussian_mixture
from flask import Flask,redirect,url_for,jsonify,flash,request
from werkzeug import secure_filename
from Model_Test import test_sample
from app import app

#app=Flask(__name__)
UPLOAD_FOLDER = './test_samples/'
ALLOWED_EXTENSIONS = set(['wav', 'mp3', 'mp4'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/authentication-upload', methods=['GET', 'POST'])
def upload_testfile():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(os.getcwd()+"/"+app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join('test_samples',secure_filename(file.filename)))
            flag, _speakerMatch, _confidence= test_sample(filename)
            
            responseJson = {}
            _speakerName = ""
            _guid = ""

            if(_speakerMatch != ""):
                filenNameArr = _speakerMatch.split("-") #get the name of the speaker
                _speakerName = filenNameArr[0]
                _guid = filenNameArr[1]

            if(flag == True):
                responseJson = jsonify(
                            status = 200,
                            message = "Match found",
                            name = _speakerName,
                            guid = _guid,
                            confidence=_confidence
                        )
            elif(flag == False):
                responseJson = jsonify(
                            status = 200,
                            message = "Match not found",
                            guid = _guid,
                            speaker = "null",
                            confidence=_confidence
                        )
            else: 
                responseJson = jsonify(
                            status = 500,
                            message = "Internal server error"
                        )

            return responseJson
    return '''
<!doctype html>
<title>Upload test File</title>
<h1>Upload Test File</h1>
<form action="" method=post enctype=multipart/form-data>
<p><input type=file name=file>
<input type=submit value=Test>
</form>
'''

"""if __name__ == "__main__":
    app.run(debug=True)"""