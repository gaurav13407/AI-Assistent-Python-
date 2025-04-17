import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary  # User-defined music library with song:link mapping
import requests

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# News API key
NEWS_API_KEY = "f1fc07e7429b4b95882e235d4f1234b2"

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen_command(timeout=3, phrase_time_limit=2):
    """Listen to user voice and return the command as text"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("Could not connect to the speech service.")
            return None

def open_website(name, url):
    """Open a website and provide voice feedback"""
    speak(f"Opening {name}")
    webbrowser.open(url)

def play_song(song_name):
    """Play song from the music library"""
    song = song_name.lower()
    print(f"Trying to play: {song}")
    if song in musiclibrary.music:
        speak(f"Playing {song}")
        webbrowser.open(musiclibrary.music[song])
    else:
        speak("Sorry, I could not find the song.")

def read_news():
    """Fetch and read top headlines"""
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            speak("Here are the top headlines.")
            for article in articles[:5]:  # Limit to 5 articles
                speak(article['title'])
                print(f"News: {article['title']}")
                speak("Say 'stop' to end or wait for next.")
                command = listen_command(timeout=3, phrase_time_limit=2)
                if command and "stop" in command:
                    speak("News reading stopped.")
                    break
        else:
            speak("Failed to fetch news.")
    except Exception as e:
        speak("Something went wrong while getting news.")
        print(f"Error: {e}")

def process_command(command):
    """Process the recognized command"""
    if "open google" in command:
        open_website("Google", "https://google.com")
    elif "open youtube" in command:
        open_website("YouTube", "https://youtube.com")
    elif "open facebook" in command:
        open_website("Facebook", "https://facebook.com")
    elif "open netflix" in command:
        open_website("Netflix", "https://pcmirror.cc/home")
    elif "open chatgpt" in command:
        open_website("ChatGPT", "https://chatgpt.com")
    elif command.startswith("play"):
        play_song(command.replace("play", "").strip())
        if play_song in musiclibrary.music:
                link = musiclibrary.music[song]  # Get the song link from the music library
                webbrowser.open(link)
    elif "news" in command:
        read_news()
    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            print("Say 'Jarvis' to activate.")
            trigger = listen_command(timeout=3, phrase_time_limit=2)
            if trigger and "jarvis" in trigger:
                speak("Yes?")
                user_command = listen_command()
                if user_command:
                    print(f"Command received: {user_command}")
                    process_command(user_command)
                else:
                    speak("I didn't catch that. Please repeat.")
        except Exception as e:
            print(f"Unexpected Error: {e}")