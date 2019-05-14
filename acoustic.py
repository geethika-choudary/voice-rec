import acoustid
import chromaprint
duration, fp_encoded = acoustid.fingerprint_file("./manish.mp3")
fingerprint, version = chromaprint.decode_fingerprint(fp_encoded)
print(fingerprint)
print(fp_encoded)
