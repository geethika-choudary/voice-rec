from pydub import AudioSegment
sound = AudioSegment.from_mp3("aryan.mp3")
sound.export("aryan.wav", format="wav")