from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform
import re, requests
from datetime import datetime

def is_hindi(t):
    return any(w in t.lower() for w in ["kya","jod","ghata","guna","bhag","kaun","hai","kitna","batao"])

def speak(txt, lab=None):
    if lab: lab.text = txt
    if platform == 'android':
        try:
            from jnius import autoclass
            Locale = autoclass('java.util.Locale')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            TTS = autoclass('android.speech.tts.TextToSpeech')
            tts = TTS(PythonActivity.mActivity, None)
            loc = Locale("hi","IN") if is_hindi(txt) else Locale.US
            tts.setLanguage(loc)
            tts.setPitch(1.4)
            tts.setSpeechRate(0.9)
            tts.speak(txt, 0, None)
        except: pass

def calc(t):
    try:
        t2 = t.lower().replace("jod","+").replace("plus","+").replace("ghata","-").replace("minus","-").replace("guna","*").replace("bhag","/").replace("into","*")
        ex = "".join(re.findall(r"[0-9+\-*/(). ]+", t2))
        r = eval(ex)
        return f"Jawab {r} hai Boss" if is_hindi(t) else f"Answer is {r} Boss"
    except: return None

def answer(q):
    try:
        ql = q.lower().replace("who is","").replace("kaun hai","").strip()
        r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{ql}", timeout=6)
        j = r.json()
        if "extract" in j: return j["extract"][:350]
    except: pass
    return "Nahi mila Boss"

def do_cmd(cmd, lab):
    def w(dt):
        c = cmd.lower()
        if "time" in c or "samay" in c:
            speak(f"Time {datetime.now().strftime('%I:%M %p')} hai Boss", lab)
            return
        if any(ch.isdigit() for ch in cmd):
            a = calc(cmd)
            if a:
                speak(a, lab)
                return
        if c.startswith(("who","what","kya","kaun")):
            speak(answer(cmd), lab)
            return
        speak(f"Aapne bola {cmd}", lab)
    Clock.schedule_once(w, 0
