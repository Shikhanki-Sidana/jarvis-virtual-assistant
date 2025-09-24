import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import subprocess
import pyautogui

# Initialize tts engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text: str):
    """Speak out loud and print the text."""
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command(timeout=5, phrase_time_limit=7):
    """Listen from the microphone and return lowercased text. Returns empty string on failure."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.4)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            query = r.recognize_google(audio, language='en-US')
            return query.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""

def tell_time():
    now = datetime.datetime.now().strftime('%I:%M %p')
    speak(f"The time is {now}")

def tell_date():
    today = datetime.date.today().strftime('%B %d, %Y')
    speak(f"Today's date is {today}")

def search_wikipedia(query, sentences=2):
    try:
        summary = wikipedia.summary(query, sentences=sentences)
        speak(summary)
    except Exception as e:
        speak("Sorry, I couldn't find that on Wikipedia.")

def open_website(url_or_query: str):
    if not url_or_query.startswith('http'):
        url = 'https://www.google.com/search?q=' + url_or_query.replace(' ', '+')
    else:
        url = url_or_query
    webbrowser.open(url)
    speak(f"Opened {url_or_query}")

def play_music_from_folder(folder_path: str):
    try:
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp3','.wav'))]
        if not files:
            speak('No music files found in folder.')
            return
        first = os.path.join(folder_path, files[0])
        if os.name == 'nt':
            os.startfile(first)
        else:
            subprocess.Popen(['xdg-open', first])
        speak('Playing music')
    except Exception as e:
        speak('Could not play music: ' + str(e))

def take_screenshot(save_path='screenshot.png'):
    image = pyautogui.screenshot()
    image.save(save_path)
    speak(f'Screenshot saved to {save_path}')

def run_system_command(command: str):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        speak('Command executed')
        print(output)
    except Exception as e:
        speak('Failed to execute command')
