import time, os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import openai

def listen(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio, language='en')
        print(f"[user] {text}")
        answer(text)
    except sr.UnknownValueError:
        print("Failure to recognize")
    except sr.RequestError as e:
        print('요청실패 : {0}'.format(e))

def answer(input_text):
    answer_text = ''
    if 'hi' in input_text:
        answer_text = 'hello'
    elif "How is the weather today" in input_text:
        answer_text = 'sunny day'
    elif "How's the exchange rate" in input_text:
        answer_text = "It went up"
    elif "thanks" in input_text:
        answer_text = "No problem"
    elif "exit" in input_text:
        answer_text = "okay ending the program..."
        stop_listening(wait_for_stop=False)
    else:
        answer_text = "Say it once again, please"
    speak(answer_text)

def speak(text):
    print(f"[AI]: {text}")
    file_name = 'voice.mp3'
    tts = gTTS(text=text, lang='en')
    tts.save(file_name)
    playsound(file_name)
    if os.path.exists(file_name):
        os.remove(file_name)

r = sr.Recognizer()
m = sr.Microphone()

speak('Can I help you with anything?')

stop_listening = r.listen_in_background(m, listen)
#stop_listening(wait_for_stop=False)

while True:
    time.sleep(0.1)
