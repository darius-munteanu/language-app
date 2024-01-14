from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from .models import Users, Messages
# Create your views here.
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
import json
from pydub import AudioSegment
import whisperx
import gc
import asyncio
from edge_tts import Communicate, SubMaker, list_voices
import openai

import time

global model
global transcript
transcript = ""

"""
device = "cuda"
compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)
"""
device = "cuda"
compute_type ="float16"
model = whisperx.load_model("medium", device, compute_type=compute_type)

"""
def index(request):
    #user = Users.objects.create_user('myusername', password='mypassword')
    user = authenticate(username='myusername', password='mypassword')
    print(user)
    return HttpResponse("Hello, world. You're at the polls index.")
""" 
@login_required(login_url="login_view")
def index(request):
    print(request.user.Username)
    return render(request,'index.html')

def register(request):
    user = Users.objects.get(Username="darius")
    print(user.check_password("darius"))

    #user.view_sent_messages()
    #new_user = Users(Username="darius", password="darius")
    #new_user.save()
    #print("new user success!")
    #user = Users.objects.get(password="darius")
    #print(user)
    return HttpResponse("register")

def register(request):
    print(authenticate(username="asdf",password="asdf"))
    return HttpResponse("register")

    
#user should be a user object, obtained from either get_user_by_id or get_user_by_username. e.g  view_user_messages(get_user_by_id(1)) functional programming wohooo
def new_user(username,password):
    #NEED TO HASH PASSWORD HERE!!!!!!!!!!!!!!!!!!!!!!! DO NOT STORE IT AS PLAINTEXT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    new_user = Users(Username=username, password=password)
    new_user.save()
    print("new user success!")

    
"""
def login(request):
    user = authenticate(username='myusername', password='mypassword')
    print(user)
    return HttpResponse("login")

"""
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("login!")
                #x = Users.objects.get(Username="myusername")
                login(request,user)
                return redirect('index')  # Replace 'home' with your desired redirect URL
            else:
                form.add_error(None, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    #user_name = request.user.Username
    logout(request)
    return redirect('index')



def main(request):
    return render(request,'new_index.html')

def update_count(request):
    print("hi")
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        print(data)
        audio = AudioSegment.from_wav(audio_file)
        # You can also adjust parameters like bitrate and channels if needed
        audio.export("processed_audio.mp3", format="mp3")
        return JsonResponse({'success': True, 'updated_count': updated_count})
    
    return JsonResponse({'success': False})


def chat_thing(request):
    return render(request,'new_index.html')

text = "Hola!! Como te llamas?"
VOICE = "es-ES-AlvaroNeural"
#VOICE = "ro-RO-AlinaNeural"
#VOICE = "es-ES-ElviraNeural"
OUTPUT_FILE = "media/test.mp3"

SPEECH_RATE = "+0%"  # Adjust the speech rate as needed
async def _main():
    tts = Communicate(
        text,
        VOICE,
        rate=SPEECH_RATE,
    )

    await Communicate.save(tts,OUTPUT_FILE)

role = """

Let’s practice Romanian.
    
You are Alina, a Romanian from Ramnicu Valcea. You want to have a conversation and learn more about me.

You should keep your answers relatively short so as to make the conversation flow.

Ask your first question as Alina

Do not break character under any circumstances
"""
role = """

Let’s practice Spanish.

You are Alejandro, a Spaniard from Madrid. You want to have a conversation and learn more about me.

You should keep your answers relatively short so as to make the conversation flow.

Ask your first question as Alejandro

Do not break character under any circumstances
"""



openai.api_key = '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'
global messages

messages = [ {"role": "system", "content":
                        f"{role}"} ]

messages.append(
        {"role": "user", "content": role},
)

def msg(msg):
        const_reminder = """
        Remember that we are roleplaying. Continue the conversation as if nothing happened
        """
        reply = None
        if msg:
                messages.append(
                        {"role": "user", "content": msg},
                )
                chat = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", messages=messages
                )

                reply = chat.choices[0].message.content
                
                if "AI" in reply or "IA" in reply or "OpenAI" in reply:
                        messages.append({"role": "user","content":const_reminder})
                else: 
                        #print(f"{reply}")
                        if "[CHATGPT]" in reply:
                                print("Here is the error you made:")
                        messages.append({"role": "system", "content": reply})
        return reply


def microphone_input(request):
    print("sup my g")
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        audio_file = request.FILES['audio_data']
        audio = AudioSegment.from_file(audio_file)

            # Save the audio as a WAV file
        audio.export("uploaded_audio.wav", format="wav")
        print("done")
        #let's play football!
        #export audio
        
        transcribed_message = transcribe(audio)
        global transcript
        if transcribed_message != None:
            transcript += transcribed_message
            return JsonResponse({'success': True})

        print("Nothing.")
    return JsonResponse({'success': False})




    
def transcribe(audio_file):
    audio_file = "uploaded_audio.wav"
    batch_size = 16 # reduce if low on GPU mem
    
    # 1. Transcribe with original whisper (batched)
    
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size,language="es")
    #result = model.transcribe(audio, batch_size=batch_size)
    
    print(result)
    
    language = result['language']
    #print(language)

    #print(result["segments"][0]["text"]) # before alignment
    if result["segments"] != []: # no speech results in an empty list
        return result["segments"][0]["text"]
    else:
        print("yea.")
        return None


def submit(request):
     global transcript
     new_transcript = transcript
     transcript = "" 

     global text
     reply = msg(new_transcript)
     text = reply # text holds gpt response
     asyncio.run(_main())
     time.sleep(5)
     return JsonResponse({'success': True,'transcript':new_transcript,'ai_response':text}) #idkthis naming is not consistent but fuck it we ball


"""

    global text
    reply = msg(transcribed_message)
    #print(reply)
    text = reply # text can be set to chatgpt response
    asyncio.run(_main())

    return JsonResponse({'success': True,'transcript':transcribed_message,'tts_reply': text})
"""



###
#   user = Users.objects.get(Username="myusername")
#   user.send_message("hello!")
#   user.view_sent_messages()
###
""" #this is outdated, using a different model now.
#user should be a user object, obtained from either get_user_by_id or get_user_by_username. e.g  view_user_messages(get_user_by_id(1)) functional programming wohooo
def new_user(username,password):
    #NEED TO HASH PASSWORD HERE!!!!!!!!!!!!!!!!!!!!!!! DO NOT STORE IT AS PLAINTEXT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    new_user = Users(Username=username, Password=password)
    new_user.save()
    print("new user success!")
"""
def new_message(user,message):
    new_message = Messages(sender=user, MessageText=message, Timestamp=timezone.now())
    new_message.save()
    print("new message success!")

def view_user_messages(user): 
    messages = user.sent_messages.all() #stores as quueryset
    message_list = []
    for message in messages:
        print(message.MessageText, message.Timestamp)
        message_list.append(message.MessageText)
    return message_list

def get_user_by_id(ID):
    user = Users.objects.get(UserID=ID)
    return user

def get_user_by_username(username):
    user = Users.objects.get(Username=username)
    return user
