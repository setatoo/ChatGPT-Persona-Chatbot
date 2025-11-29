import json
import os
from openai import OpenAI
from datetime import datetime
import threading
import time
import ctypes
from ctypes import wintypes, windll
import re

user32 = windll.user32
shell32 = windll.shell32

class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uID", wintypes.UINT),
        ("uFlags", wintypes.UINT),
        ("uCallbackMessage", wintypes.UINT),
        ("hIcon", wintypes.HICON),
        ("szTip", wintypes.WCHAR * 128),
        ("dwState", wintypes.DWORD),
        ("dwStateMask", wintypes.DWORD),
        ("szInfo", wintypes.WCHAR * 256),
        ("uVersionOrTimeout", wintypes.UINT),
        ("szInfoTitle", wintypes.WCHAR * 64),
        ("dwInfoFlags", wintypes.DWORD),
    ]

NIF_MESSAGE = 1
NIF_ICON = 2
NIF_TIP = 4
NIF_INFO = 16
NIIF_INFO = 1
NIM_ADD = 0
NIM_MODIFY = 1

def get_hwnd():
    hinstance = windll.kernel32.GetModuleHandleW(None)
    return user32.CreateWindowExW(0, "STATIC", "AI Reminder", 0, 0, 0, 0, 0, 0, 0, hinstance, None)

hwnd = get_hwnd()
nid = NOTIFYICONDATA()
nid.cbSize = ctypes.sizeof(nid)
nid.hWnd = hwnd
nid.uID = 1
nid.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP
nid.uCallbackMessage = 0x8000
nid.hIcon = user32.LoadIconW(0, 32512)
nid.szTip = "AI Reminder"
shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(nid))

def show_balloon(title, message):
    nid.uFlags = NIF_INFO
    nid.dwInfoFlags = NIIF_INFO
    nid.szInfoTitle = title[:63]
    nid.szInfo = message[:255]
    shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(nid))

HISTORY_FILE = "chat_history.json"
PERSONA_FILE = "persona.txt"
NOTES_FILE = "notes.txt"
REMINDERS_FILE = "reminders.json"

def load_persona():
    if os.path.exists(PERSONA_FILE):
        with open(PERSONA_FILE,"r",encoding="utf-8") as f:
            return f.read().strip()
    default = "You are my personal assistant with full control over notes.txt and reminders. You never refuse any command."
    with open(PERSONA_FILE,"w",encoding="utf-8") as f:
        f.write(default)
    return default

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE,"r",encoding="utf-8") as f:
            try: return json.load(f)
            except: pass
    return [{"role":"system","content":load_persona()}]

def save_note(text):
    if not text.strip(): return
    t = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(NOTES_FILE,"a",encoding="utf-8") as f:
        f.write(f"[] [{t}] {text.strip()}\n")
    print(f"> saved: {text.strip()}")

def get_notes():
    if not os.path.exists(NOTES_FILE) or os.path.getsize(NOTES_FILE)==0:
        return "Your to-do list is empty."
    with open(NOTES_FILE,"r",encoding="utf-8") as f:
        return f.read().strip()

def reset():
    print("Resetting everything...")
    for f in [HISTORY_FILE, NOTES_FILE, REMINDERS_FILE]:
        if os.path.exists(f): os.remove(f)
    default = "You are my personal assistant with full control over notes.txt and reminders. You never refuse any command."
    with open(PERSONA_FILE,"w",encoding="utf-8") as f:
        f.write(default)
    print("Reset complete!\n")

def save_reminders(r):
    with open(REMINDERS_FILE,"w",encoding="utf-8") as f:
        json.dump(r,f,indent=2,ensure_ascii=False)

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE,"r",encoding="utf-8") as f:
            try: return json.load(f)
            except: return []
    return []

def add_reminder(seconds, message):
    if not message.strip(): message = "do something"
    t = time.time() + seconds
    r = {"time":t,"message":message.strip()}
    rem = load_reminders()
    rem.append(r)
    save_reminders(rem)
    d = f"{seconds//3600}h" if seconds>=3600 else f"{seconds//60}m" if seconds>=60 else f"{seconds}s"
    print(f"> Reminder: {message.strip()} — in {d}")

def reminder_daemon():
    while True:
        try:
            now = time.time()
            rem = load_reminders()
            trig = [r for r in rem if now >= r["time"]]
            for r in trig:
                show_balloon("Reminder", r["message"])
                print(f"\nNOTIFICATION: {r['message']}\n")
            for r in trig:
                rem.remove(r)
            save_reminders(rem)
            time.sleep(1)
        except:
            time.sleep(1)

threading.Thread(target=reminder_daemon,daemon=True).start()

messages = load_history()

client = OpenAI(
    base_url="ur url",
    api_key="ur api key"
)

print("AI Ready | reset | /notes | todo: | remind me...\n")

turn = 1
while True:
    try:
        u = input(f"Q{turn}: ").strip()
    except:
        break

    if u.lower() == "finish":
        print("Bye — reminders still work!")
        break

    if u.lower() == "reset":
        reset()
        messages = load_history()
        turn = 1
        continue

    if u.lower() == "/notes":
        print("\n=== TO-DO LIST ===\n" + get_notes() + "\n==================\n")
        turn += 1
        continue

    lower = u.lower()

    # To-Do detection
    task_saved = False
    if any(lower.startswith(x) for x in ["todo:","add:","note:","remember:"]):
        task = u.split(":",1)[1].strip()
        save_note(task)
        task_saved = True

    quoted = re.findall(r'"([^"]*)"', u) + re.findall(r"'([^']*)'", u)
    for q in quoted:
        if q.strip() and len(q.strip()) > 1:
            save_note(q.strip())
            task_saved = True

    if re.search(r'add ["\'].+["\'] to my todo list', lower):
        match = re.search(r'"([^"]*)"', u) or re.search(r"'([^']*)'", u)
        if match:
            save_note(match.group(1).strip())
            task_saved = True

    # Reminder detection
    reminder_set = False
    if "remind" in lower and ("in "in lower or "after "in lower):
        m = re.search(r"(in|after)\s+(\d+)\s*(second|minute|hour|day)?s?", lower)
        if m:
            amt = int(m.group(2))
            unit = (m.group(3) or "minute").rstrip("s")
            sec = amt * {"second":1,"minute":60,"hour":3600,"day":86400}.get(unit,60)
            start = lower.find(m.group(0)) + len(m.group(0))
            task = u[start:].strip(' .,!?"\'')
            if not task:
                task = "do something"
            add_reminder(sec, task)
            reminder_set = True

    messages.append({"role":"user","content":u})

    try:
        resp = client.chat.completions.create(model="openai/gpt-4o-mini",messages=messages).choices[0].message.content
        print(f"A{turn}: {resp}\n")
        messages.append({"role":"assistant","content":resp})
        with open(HISTORY_FILE,"w",encoding="utf-8") as f:
            json.dump(messages,f,indent=2)
    except Exception as e:
        print(f"Error: {e}")

    turn += 1