from groq import Groq
import pyttsx3 as p
import datetime
import speech_recognition as sr
import json
import pyaudio as py
import wave

def start():

    prompt_header ="""You are a humorous Voice Assistant . Your role is to help me with all the tasks i give you  .
      Greet me in your way only once at the beginning of the conversation.
    Keep the conversation short and crisp . Do not wrtie actions and gestures in asteriks.
                    """
    system_Set =  prompt_header

    id = "1"

    with open("history_db.json", 'r') as f:
            history= json.load(f)

    if id not in history:
        next_key=len(list(history.keys()))+1
        with open("history_db.json",'w') as f:
                    history[next_key]=[{
                    "role":"system",
                    "content":system_Set
                            }]
                    json.dump(history,f)                  
        groq(next_key)

    else:
        system =p.init()

        #rate of speech
        rate =system.getProperty('rate')
        system.setProperty(rate,170)
        
        #voice type
        voices = system.getProperty('voices')
        system.setProperty('voice',voices[1].id)


        greet ="Hey there , what's the problem?"
        system.say(greet)
        print(greet)
        system.runAndWait()

                     
def continue_conv(id,prompt):
    with open("history_db.json",'r') as f:
        message_prompt= json.load(f)
    
        if str(id) not in message_prompt:
             message_prompt[str(id)]=[]


        x=  {"role":"user",
        "content":prompt}
        message_prompt[str(id)].append(x)

    with open("history_db.json",'w') as f:
          json.dump(message_prompt,f)
    groq(1)     


def groq(id):
    with open('G:/dem/turtle voice/key1.json') as f:
        key = json.load(f)
        keys = key['key']
    client = Groq(api_key = keys)


    with open("history_db.json", 'r') as f:
        chat_history = json.load(f)    
    message = chat_history[str(id)]

    completion = client.chat.completions.create(
        model = "llama3-70b-8192",
        messages = message,
        temperature = 0.8,
        max_tokens = 1024,
        top_p = 1,
        stream = True,
        stop = None,
    )

    answer=""""""

    for chunk in completion:
        response =chunk.choices[0].delta.content if hasattr(chunk.choices[0].delta,'content')else None
        answer += response if response is not None else ""   
    system =p.init()
    rate =system.getProperty('rate')
    system.setProperty(rate,170)

    system.say(answer)
    print(answer)

    system.save_to_file(answer,"G:/dem/turtle voice/ouput.wav")
    system.runAndWait()


if __name__ == "__main__":    

    start()

    while True:
        audio = py.PyAudio()
        chunks = []
        stream = audio.open(format=py.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        try:
            while True:
                data = stream.read(1024)
                chunks.append(data)
        except KeyboardInterrupt:
            print("Recording stopped.")
        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open("convo.wav", "wb") as sound_file:
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(py.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b"".join(chunks))


        r = sr.Recognizer()
        audio_file=sr.AudioFile('convo.wav')
        with audio_file as source:
            audio = r.record(source)
        try:
            prompt = r.recognize_google(audio)
            
        except Exception as e:
            print("Exception: "+str(e))

        if prompt in ["alright thanks" , "thanks" , "thank you" , "bye-bye" , "see you later","alright thank you","okay thanks"] :
                    bye = print("It was fun helping you Shriyash . Let me know if you need any help!")
                    system =p.init()
                    rate =system.getProperty('rate')
                    system.setProperty(rate,170)
                    system.say(bye)
                    break
        else :
                    continue_conv(1,prompt)