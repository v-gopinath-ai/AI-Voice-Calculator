import speech_recognition as sr
import pyttsx3
import time

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
 try:
    engine.stop
    engine.say(text)
    engine.runAndWait()
 except:
    print("Speech error") 

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Speak your calculation")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            speak("No audio incoming")
            return ""
        except OSError:
            speak("Microphone not detected")
            return ""

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Could not understand")
        return ""
    except sr.RequestError:
        speak("Speech service not available")
        return ""

def calculate(command):
    command = command.replace("divided by","/")
    command = command.replace("plus","+")
    command = command.replace("minus","-")
    command = command.replace("multiply","*")
    command = command.replace("divide","/")
    command = command.replace("into","*")

    allowed_chars = "0123456789+-*/.() "
    if not all(char in allowed_chars for char in command):
        return "Invalid Expression"

    command = command.strip()
    if command == "" or command[-1] in "+-*/":
        return "Incomplete Expression"

    try:
        return eval(command)
    except:
        return "Invalid Expression"

def main():
    speak("Voice Calculator Started")
    last_input_time = time.time()

    while True:
        command = listen()

        if command == "":
            if time.time() - last_input_time > 30:
                speak("No activity detected. Exiting")
                break
            continue
        else:
            last_input_time = time.time()

        if "exit" in command:
            speak("Exiting...")
            break

        result = calculate(command)
        print("Result:", result)

        if isinstance(result, str):
            speak(result)
        else:
            speak(f"The answer is {result}")
            time.sleep(1)

if __name__ == "__main__":
    main()