#!/usr/bin/env python3

import speech_recognition as sr
import os,sys
import subprocess as sp



'''
ffmpeg -i audio.xxx -c:a flac audio.flac
ffmpeg -i fileout.flac -f segment -segment_time 15 -c copy out/out%03d.flac
'''

# preprocess

video_file = sys.argv[1]
sp.call('rm out/*', shell = True)
sp.call('ffmpeg -i %s -c:a flac audio.flac' % video_file, shell = True)
sp.call('ffmpeg -i audio.flac -f segment -segment_time 15 -c copy out/out\%03d.flac', shell = True)



# obtain path to "english.wav" in the same folder as this script
from os import path

for root, dirs, files in os.walk("out/."):
    for file in files:
        if file == '.DS_Store':
            continue
 
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "out/"+file)

        # use the audio file as the audio source
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source) # read the entire audio file

        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print(r.recognize_google(audio))
        except sr.UnknownValueError:
            print("")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

