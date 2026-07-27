import speech_recognition as sr
import pyttsx3
import time

def speak(text):
    print("Assistant:", text)
    engine = pyttsx3.init("sapi5")
    engine.setProperty("rate",150)
    voices=engine.getProperty("voices")
    if voices:
        engine.setProperty("voice",voices[0].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def listen(prompt="Speak your calculation"):
    r=sr.Recognizer()
    speak(prompt)
    time.sleep(0.5)
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio=r.listen(source,timeout=10,phrase_time_limit=8)
    except sr.WaitTimeoutError:
        speak("No audio detected. Goodbye.")
        return None
    except OSError:
        speak("Microphone not detected.")
        return None
    try:
        txt=r.recognize_google(audio).lower()
        print("You said:",txt)
        return txt
    except:
        speak("Sorry, I could not understand.")
        return None

def ask_yes_no(q):
    while True:
        ans=listen(q+" Please say yes or no.")
        if ans is None:
            return False
        if "yes" in ans:
            return True
        if "no" in ans:
            return False

def calculate(cmd):
    rep={"divided by":"/","multiplied by":"*","plus":"+","minus":"-","times":"*","into":"*","divide":"/","multiply":"*"}
    for k,v in rep.items():
        cmd=cmd.replace(k,v)
    for w in ["what is","calculate","please","equals","equal to","is"]:
        cmd=cmd.replace(w,"")
    try:
        return True,eval(cmd)
    except ZeroDivisionError:
        return False,"Cannot divide by zero."
    except:
        return False,"Invalid expression."

def main():
    speak("Voice calculator started.")
    while True:
        cmd=listen()
        if cmd is None:
            break
        if "exit" in cmd or "quit" in cmd:
            speak("Thank you for using AI Voice Calculator. Goodbye.")
            break
        speak(f"You said {cmd}")
        if not ask_yes_no("Is this correct?"):
            speak("Please say your calculation again.")
            continue
        ok,res=calculate(cmd)
        speak(f"Your answer is {res}" if ok else res)
        if ask_yes_no("Do you have more questions?"):
            continue
        speak("Thank you for using AI Voice Calculator. Goodbye.")
        break

if __name__=="__main__":
    main()
