import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print("speaking:", text)
    engine.say(text)
    engine.runAndWait()

speak("testing voice output")