import pyjokes.jokes_es
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            talk('uh-huh')
            print('Listening....')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alex' in command:
                command = command.replace('alex', '')
                print(command)
    except:
        pass
    return command

def run_alexa():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        print(song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current time is ' + time)
    elif 'who' in command:
        info = wikipedia.summary(command, 3)
        print(info)
        talk(info)
    elif 'what' in command:
        info = wikipedia.summary(command, 3)
        print(info)
        talk(info)
    elif 'find' in command:
        info = wikipedia.summary(command, 3)
        print(info)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'yourself' in command:
        talk('I am alex, your virtual assistant, created by Team Alpha')
    else:
        talk('Sorry, I am having trouble connecting to the network, Try again in a little while')


run_alexa()
