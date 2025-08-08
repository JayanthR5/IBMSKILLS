import speech_recognition as sr
import subprocess
import pyttsx3
import webbrowser

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

# Initialize speech recognizer
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Clearing background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language='en-US')
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def main():
    print("🟢 Say: 'chrome', 'google', 'youtube', 'chatgpt', 'nutrition', or 'exit'")
    
    while True:
        command = listen()

        if 'chrome' in command:
            speak("Opening Chrome...")
            program = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            subprocess.Popen([program])

        elif 'google' in command:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com")

        elif 'youtube' in command:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")

        elif 'chat gpt' in command or 'chatgpt' in command:
            speak("Opening ChatGPT...")
            webbrowser.open("https://chat.openai.com")

        elif 'nutrition' in command:
            speak("Opening WHO Nutrition website...")
            webbrowser.open("https://www.who.int/health-topics/nutrition")

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye!")
            break
def get_voice_input():
    return listen()