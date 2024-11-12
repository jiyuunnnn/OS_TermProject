import time, os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import openai

openai.api_key = "sk-1234567890abcdef"

def answer(input_text):
    # 로컬에서 간단히 처리 가능한 명령어
    if input_text.lower() in ["stop", "exit"]:
        response_text = "Stopping the assistant."
        print(f"[AI]: {response_text}")
        speak(response_text)
        exit()
    elif input_text.lower() == "hello":
        response_text = "Hello! How can I assist you today?"
        print(f"[AI]: {response_text}")
        speak(response_text)
        return

    # OpenAI API 호출
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text}
            ]
        )
        response_text = response['choices'][0]['message']['content']
        print(f"[AI]: {response_text}")
        speak(response_text)
    except openai.error.RateLimitError:
        print("API 사용 한도를 초과했습니다. 잠시 후 다시 시도해 주세요.")
        speak("I'm sorry, there was an issue with generating a response due to quota limits.")

def speak(text):
    print(f"[AI]: {text}")
    file_name = 'voice.mp3'
    tts = gTTS(text=text, lang='en')
    tts.save(file_name)
    playsound(file_name)
    if os.path.exists(file_name):
        os.remove(file_name)

r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='en')
            print(f'[User]: {text}')
            answer(text)
        except sr.UnknownValueError:
            print("Failed to recognize")
        except sr.RequestError as e:
            print(f"Request failed: {e}")
