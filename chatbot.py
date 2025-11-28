import json
import os
from openai import OpenAI
#/////////////////////////////////////////////////////
HISTORY_FILE = "chat_history.json"
PERSONA_FILE = "persona.txt"
#///////////////////
def load_persona():
    if os.path.exists(PERSONA_FILE):
        with open(PERSONA_FILE, "r") as f:
            return f.read().strip()
    else:
        default_persona = "You are a friendly and helpful AI assistant who always speaks in English. Give detailed answers."
        with open(PERSONA_FILE, "w") as f:
            f.write(default_persona)
        return default_persona
def load_history(persona):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    else:
        return [{"role": "system", "content": persona}]
def reset_all():
    default_persona = "You are a friendly and helpful AI assistant who always speaks in English. Give detailed answers."
    with open(PERSONA_FILE, "w") as f:
        f.write(default_persona)
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    print("Persona and chat history have been reset!\n")
    return default_persona, [{"role": "system", "content": default_persona}]
persona = load_persona()
messages = load_history(persona)
client = OpenAI(
    base_url="ur URL",
    api_key="ur API"
)
print("Type 'finish' to exit the chat.")
print("Type 'persona' to change AI persona.")
print("Type 'reset' to reset persona and chat history.\n")
turn_counter = 1
#//////////////////////////
while True:
    user_input = input(f"Q{turn_counter}: ")
    if user_input.lower() == "finish":
        print("Goodbye!")
        break
    if user_input.lower() == "persona":
        new_persona = input("Enter new persona for AI: ")
        persona = new_persona
        with open(PERSONA_FILE, "w") as f:
            f.write(persona)
        messages = [{"role": "system", "content": persona}]
        print("Persona updated!\n")
        continue
    if user_input.lower() == "reset":
        persona, messages = reset_all()
        turn_counter = 1
        continue
    messages.append({"role": "user", "content": user_input})
    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )
    response = completion.choices[0].message.content
    print(f"A{turn_counter}: {response}\n")
    messages.append({"role": "assistant", "content": response})
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)
    turn_counter += 1
