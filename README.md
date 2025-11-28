# ChatGPT Persona Chatbot

A Python chatbot using the OpenAI API via Liara service, with:

- Customizable AI persona
- Chat history saved between runs
- English-only responses
- Numbered Q&A
- Reset history and persona
- Exit with `finish`

---

## Features

- **Custom Persona**: Change the AI's personality anytime by typing `persona`.
- **History**: Chat history is saved locally in `chat_history.json` and will be loaded on next run.
- **Reset**: Use the `reset` command to clear both the persona and chat history.
- **Numbered Q&A**: Each question and answer is numbered for easy reference.
- **Exit**: Type `finish` to exit the chatbot.
- **English-only**: All responses are in English.

---

## Setup & Requirements

1. **Python 3.x**: Make sure Python 3 is installed on your system.  
2. **Install dependencies**:

```bash
pip install openai
Get API credentials from Liara AI:

Visit Liara AI and get your Base URL and API Key.

Update the chatbot script:
Open chatbot.py and replace placeholders:

python
Copy code
client = OpenAI(
    base_url="YOUR_URL_HERE",
    api_key="YOUR_API_KEY_HERE"
)
⚠️ Important: Never commit your API key to GitHub or share it publicly.
For extra security, use a .env file and python-dotenv.

Usage
Run the chatbot:

bash
Copy code
python chatbot.py
Chat commands:

finish → Exit the chatbot.

persona → Change AI persona dynamically.

reset → Reset both chat history and persona.

Files
chatbot.py – Main chatbot script

chat_history.json – Saved chat history (auto-generated)

persona.txt – Saved AI persona (auto-generated)
