from pydub import AudioSegment

sound = AudioSegment.from_file("memo.mp3", format="mp3")
loudness = sound.dBFS
print(loudness)
