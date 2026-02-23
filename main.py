import datetime
from respons import run_jarvis
from voice_output import say

import sounddevice as sd
import speech_recognition as sr


recognizer = sr.Recognizer()

def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        say("Good Morning")
        print("Good Morning")
    elif 12 <= hour < 18:
        say("Good Afternoon")
        print("Good Afternoon")
    else:
        say("Good Evening")
        print("Good Evening")

def listen_audio():
    fs = 16000
    seconds = 5

    print("Listening...")
    say("I'm listening.")

    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    audio_data = recording.tobytes()
    audio = sr.AudioData(audio_data, fs, 2)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except:
        say("Sorry, I didn't catch that.")
        return ""

# def save_memory(user, ai):
#     file_name= "memory.json"
#     if not os.path.exists(file_name):
#         with open(file_name, "w") as f:
#             json.dump({}, f)
#     memory = {"user": user, "ai": ai}
#     with open(file_name , "a") as f:
#         f.write(json.dumps(memory) + "\n")



def command(mode):
    if mode == "audio":
        query = listen_audio()
    elif mode == "text":
        query = input("You: ").lower()
    else:
        return
    run_jarvis(query)

def main_ai():
    wish()
    while True:
        command("text")

main_ai()
