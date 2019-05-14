import os
import glob
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture
import matplotlib
import math
#from pyAudioAnalysis import audioBasicIO as aIO
#from pyAudioAnalysis import audioSegmentation as aS
from pydub import AudioSegment
from pydub.playback import play
from pydub.silence import split_on_silence
from pydub import AudioSegment,silence
import wave
from pydub import AudioSegment

"""
a=[1, 2, 3, 4, 5, 6, 7, 8, 9]
probs = np.exp(a) / (np.exp(a)).sum()
print("PROBS=",probs)
print("PROBS SUM=",probs.sum())
log_probs = np.log(probs)
print("LOG PROBS=",log_probs)
print("LOG SUM= ",log_probs.sum())
probabilities = np.exp(log_probs)
print("PROBABILITY=",probabilities)
print("PROBABILITY SUM= ",probabilities.sum())
"""
"""
myaudio = intro = AudioSegment.from_wav("/Users/cb/Desktop/Tanuja_16ktest_Telugu.wav")

silence = silence.detect_silence(myaudio, min_silence_len=1000, silence_thresh=-16)

silence = [((start/1000),(stop/1000)) for start,stop in silence] 
#convert to sec
print("----------",silence)
"""
sound = AudioSegment.from_mp3("/Users/cb/Desktop/full.wav")
folder="./silence/"
chunks = split_on_silence(sound,min_silence_len=280,silence_thresh=-33,keep_silence=150)

#Breaking on silence 

for i, chunk in enumerate(chunks):
    print(i)
    print("\n")
    chunk.export(folder+"/chunk{0}.wav".format(i), format="wav")

#Merging after splitting
outfile = "merged.wav"
print(os.listdir(folder))
infiles=['chunk2.wav', 'chunk3.wav', 'chunk1.wav', 'chunk0.wav', 'chunk4.wav', 'chunk5.wav', 'chunk7.wav', 'chunk6.wav', 'chunk14.wav', 'chunk11.wav', 'chunk10.wav', 'chunk12.wav', 'chunk13.wav', 'chunk8.wav', 'chunk9.wav']
data= []
for clip in infiles:
    print("*****",clip)
    w = wave.open(clip, 'r')
    #w = AudioSegment.from_wav(folder+clip) 
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()
output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
output.writeframes(data[0][1])
output.writeframes(data[1][1])
output.close()
