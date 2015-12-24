#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#NOTE: this example requires PyAudio because it uses the Microphone class

import sys
import speech_recognition as sr
import subprocess, shlex
import os
if len(sys.argv) > 1:
    language = sys.argv[1]
    region = sys.argv[2]
# obtain audio from the microphone
r = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
        print "Google Speech Recognition thinks you said " + r.recognize_google(audio)
        text2 = r.recognize_google(audio)
        text = text2.encode('utf-8')
        langspeaker = ''
        try:
            language
        except NameError:
            language = 'en'

        try:
            region
        except NameError:
            region = 'US'

        if (language == 'de') or (language == 'en') or (language == 'es') or (language == 'it') or (language == 'fr'):
            langspeaker = 'pico'

        print "Language: %s" % language
        bashCommand = 'googletranslate "%s" "%s"' % (text, language)
        args = shlex.split(bashCommand)
        output = subprocess.Popen(args, stdout=subprocess.PIPE).stdout.read()
        print output
        if (langspeaker == 'pico'):
            os.popen('pico2wave -l=%s-%s -w=/tmp/test.wav "%s"' % (language, region, output))
            os.popen('aplay /tmp/test.wav')
            os.popen('rm /tmp/test.wav')
        else:
            os.popen('/home/linus/get_voices.sh "%s" "%s"' % (language, output))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
         print("A translator by Linus Claußnitzer")
