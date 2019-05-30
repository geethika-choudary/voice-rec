import acoustid
import chromaprint
from fuzzywuzzy import fuzz

duration, fp_encoded = acoustid.fingerprint_file('aryan.mp3')
fingerprint, version1 = chromaprint.decode_fingerprint(fp_encoded)
print(fingerprint)
duration, fp_encoded = acoustid.fingerprint_file('aryan.mp3')
sample_fingerprint, version2 = chromaprint.decode_fingerprint(fp_encoded)
similarity = fuzz.ratio(sample_fingerprint, fingerprint)
print(similarity)

