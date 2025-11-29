# AI Reminder Assistant

This project is a lightweight Windows-based assistant written in Python. It provides persistent to-do management, smart reminder scheduling with Windows tray notifications, and an AI-driven chat system with memory.

## Features

### Windows Tray Notifications
The assistant creates a tray icon using the Windows Shell API and triggers balloon notifications whenever a reminder is due.

### To-Do List Management
You can add tasks using:
- `todo:`
- `note:`
- `add:`
- `remember:`
- Quoted text such as `"buy milk"`
- Natural language patterns like:
  `add "clean desk" to my todo list`

All tasks are saved into `notes.txt`.

### Reminder Scheduling
Understands natural phrasing such as:
remind me in 10 seconds
remind me after 2 minutes to stretch
remind me in 1 hour to study

perl
Copy code
Reminders are stored in `reminders.json` and checked every second by a background daemon thread.

### Persistent AI Memory
The assistant keeps conversation state using:
- `chat_history.json`  
- `persona.txt`

The persona file defines the system message loaded at startup.

### Background Reminder Thread
A daemon thread constantly monitors reminder timestamps and triggers system notifications when needed.

## File Structure
your_script.py
chat_history.json
persona.txt
notes.txt
reminders.json

pgsql
Copy code

## Commands

### General
- `finish` — exit the program but keep reminders running
- `reset` — wipe all saved data and restore default settings
- `/notes` — show the current to-do list

### To-Do Examples
todo: fix the robot code
note: clean my desk
"update the report"
add "charge batteries" to my todo list

shell
Copy code

### Reminder Examples
remind me in 30 seconds
remind me after 5 minutes to drink water
remind me in 2 hours to study algorithms

markdown
Copy code

## Requirements
- Windows OS  
- Python 3.8+  
- Dependencies:
pip install openai

sql
Copy code

## Running the Program
Start the assistant using:
python your_script.py

yaml
Copy code

You will see:
AI Ready | reset | /notes | todo: | remind me...

pgsql
Copy code

From here you can enter commands, notes, reminders, or normal chat messages. The assistant will store tasks, schedule reminders, and respond using your configured AI endpoint.

## Notes
- Uses `ctypes` to interact with Windows Shell APIs.
- All data is stored locally on disk.
- Compatible with any OpenAI-style API endpoint you configure in the script.
