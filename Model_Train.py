import os
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture 
from sklearn import mixture
from Feature_Extraction import extract_features
import warnings   
import wave,struct      
warnings.filterwarnings("ignore")


def model_train():
    source   = "./uploads/"   
    dest = "./Speakers_models/"
    #train_file = "trainingDataPath.txt"        
    #file_paths = open(train_file,'r')
    count = 1
    features = np.asarray(())
    """for path in file_paths:    
        path = path.strip()   
        print ("This is path",path)"""
    for path in os.listdir(source):
        if path.endswith(".wav"):
            print(path)
        # Read the audio
        sample_rate,audio = read(source + path)
    
        # Extract 40 dimensional MFCC & delta MFCC features
        #vector   = extract_features(audio,sr)
        vector   = extract_features(audio,sample_rate)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
        # When features of 15 files of speaker are generated, then train the model   
        if count == 15:    
            gmm = GaussianMixture(n_components = 16, covariance_type='diag',n_init = 3)
            gmm.fit(features)
            # Dumping the trained gaussian model
            picklefile = path.split("_")[0]+".gmm"
            print("****** ", picklefile)
            print(dest+picklefile)
            cPickle.dump(gmm,open(dest + picklefile,'wb'))
            print ('Modeling completed for speaker:',picklefile," with data point = ",features.shape  )  
            features = np.asarray(())
            count = 0
        count = count + 1
    return "Modelling completed"