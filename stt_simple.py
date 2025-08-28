import speech_recognition as sr
#this package is for the speech recognition and other packages are as follows
recognizer = sr.Recognizer()
with sr.Microphone() as source :
    print("hello Say something...")
    audio = recognizer.listen(source)
    try:
        print("you said:"+ recognizer.recognize_google(audio))
    except sr.unknownValueError:
        print("Sorry, i could not understand the audio.")
    except sr.RequestError:
        print("Could not connect to the service.")
import pyttsx3
engine = pyttsx3.init()
engine.say("you said:"+recognizer.recognize_google(audio))
engine.runAndWait()
import tkinter as tk
from tkinter import scrolledtext
window= tk.Tk()
window.geometry("400*200")
text_area =  ScrolledText.ScrolledText(window,width=50,height = 10)
text_area.pack()
