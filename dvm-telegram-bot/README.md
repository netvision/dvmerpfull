# DVM ERP Telegram Bot

An AI-powered Telegram bot that lets verified staff and guardians query the DVM ERP using natural language.

## How it works

```
User → Telegram → Bot → Groq LLM (function calling) → /api/agent/* → Answer
```

The LLM decides which ERP endpoint to call, fetches the data, and writes a natural-language reply.

## Quick Setup (VPS)

### 1. Clone is already done (this folder is part of the repo)

```bash
cd ~/dvmerpfull/dvm-telegram-bot
```

### 2. Create a virtual environment & install deps

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create your .env

```bash
cp .env.example .env
nano .env
```

Fill in:
- `TELEGRAM_BOT_TOKEN` — from [@BotFather](https://t.me/BotFather) on Telegram
- `GROQ_API_KEY` — from [Groq Console](https://console.groq.com/keys)
- `AGENT_BASE_URL` — e.g. `https://your-vps-ip/api/agent`
- `AGENT_API_KEY` — same value as `AGENT_API_KEY` in the backend `.env`

### 4. Test it manually first

```bash
source venv/bin/activate
python bot.py
```

Message your bot on Telegram. Try: _"How many students?"_

### 5. Install as a systemd service

```bash
sudo cp bot.service /etc/systemd/system/dvmbot.service
sudo systemctl daemon-reload
sudo systemctl enable dvmbot
sudo systemctl start dvmbot

# Check status
sudo systemctl status dvmbot
sudo journalctl -u dvmbot -f
```

## Example Conversations

| User asks | Bot does |
|---|---|
| "How many students in Class 5?" | calls `get_school_stats`, reads class_breakdown |
| "Find Arjun Sharma" | calls `search_students(query="Arjun Sharma")` |
| "What's 2024/101's attendance?" | calls `get_student_attendance(admission_no="2024/101")` |
| "Who teaches Maths?" | calls `search_staff(department="Maths")` |
| "Guardian contact for Priya" | searches student, then calls `get_student_detail` |

## Adding More Users

Users verify themselves by sharing their Telegram contact. The backend matches the
phone number against staff, guardian, and student records.

## File Structure

```
dvm-telegram-bot/
├── bot.py            ← Telegram handler, phone verification, routing
├── agent.py          ← Groq LLM + function calling loop
├── tools.py          ← Functions that call /api/agent/* endpoints
├── requirements.txt
├── .env.example      ← Copy to .env and fill in
├── bot.service       ← Systemd unit file
└── README.md
```
