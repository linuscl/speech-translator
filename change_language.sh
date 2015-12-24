#!/bin/bash
languagename=$1
regionname=$2

file="/usr/local/lib/python2.7/dist-packages/SpeechRecognition-3.1.3-py2.7.egg/speech_recognition/__init__.py"
cp "$file" "$file.bak"
numberdel=$(cat $file | grep -n 'def recognize_google' | sed 's/^\([0-9]\+\):.*$/\1/')
sed "$numberdel"d "$file" > /tmp/languagechange
insert="\ \ \ \ def recognize_google(self, audio_data, key = None, language = '$languagename-$regionname', show_all = False):"
sed -i "$numberdel"i"$insert" /tmp/languagechange
cp /tmp/languagechange "$file"
