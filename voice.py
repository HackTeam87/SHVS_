#!/usr/bin/env python3
import pyttsx3

#На Linux-ax, скорее всего нужно еще:
#sudo apt update && sudo apt install espeak ffmpeg libespeak1
id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0'

engine = pyttsx3.init()
engine.setProperty('voice', id)
engine.setProperty('rate', 180)				#скорость речи


def speaker(text):
	'''Озвучка текста'''
	engine.say(text)
	engine.runAndWait()