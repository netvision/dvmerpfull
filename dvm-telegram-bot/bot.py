"""
bot.py — Telegram bot with phone-number-based authentication.

Flow:
  1. Anyone can message the bot (no allowlist).
  2. On first message, the bot asks the user to share their phone number via Telegram's Contact button.
  3. Once shared, the phone is verified against the school DB via /api/agent/verify-phone.
  4. Role is determined:
       - staff    → full access to all student/staff data
       - guardian → can only query their own linked children
       - unknown  → school-level stats only, no personal data
  5. Session is persisted to sessions.json so auth survives bot restarts.
"""

import json
import logging
import os
import requests
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

import agent  # noqa — imports after dotenv so GROQ_API_KEY is set

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
AGENT_BASE_URL = os.getenv("AGENT_BASE_URL", "http://localhost:8000/api/agent")
AGENT_API_KEY = os.getenv("AGENT_API_KEY", "")
SESSIONS_FILE = Path(__file__).parent / "sessions.json"

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Session store (persisted to JSON)
# ---------------------------------------------------------------------------

def _load_sessions() -> dict:
    try:
        if SESSIONS_FILE.exists():
            return json.loads(SESSIONS_FILE.read_text())
    except Exception:
        pass
    return {}


def _save_sessions(sessions: dict):
    try:
        SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=SESSIONS_FILE.parent,
            delete=False,
        ) as tmp:
            json.dump(sessions, tmp, indent=2, ensure_ascii=False)
            tmp_path = Path(tmp.name)
        tmp_path.replace(SESSIONS_FILE)
    except Exception as e:
        logger.error(f"Failed to save sessions: {e}")


SESSIONS: dict = _load_sessions()  # {str(telegram_user_id): {phone, role, name, student_ids, student_names}}


# ---------------------------------------------------------------------------
# Phone verification via backend
# ---------------------------------------------------------------------------

def _verify_phone(phone: str) -> dict:
    """Call the backend /api/agent/verify-phone and return the result."""
    try:
        resp = requests.get(
            f"{AGENT_BASE_URL}/verify-phone",
            params={"phone": phone},
            headers={"X-API-Key": AGENT_API_KEY},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error(f"Phone verification error: {e}")
        return {"role": "unknown", "name": None, "authorized_student_ids": [], "natural_summary": "Verification failed."}


def _is_own_contact(update: Update) -> bool:
    contact = update.message.contact if update.message else None
    user = update.effective_user
    if not contact or not user:
        return False
    return contact.user_id is None or contact.user_id == user.id


# ---------------------------------------------------------------------------
# Keyboards
# ---------------------------------------------------------------------------

SHARE_PHONE_KEYBOARD = ReplyKeyboardMarkup(
    [[KeyboardButton("📱 Share my phone number", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

REMOVE_KEYBOARD = ReplyKeyboardRemove()


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start — greet and ask for phone if not yet verified."""
    uid = str(update.effective_user.id)
    name = update.effective_user.first_name or "there"

    if uid in SESSIONS:
        sess = SESSIONS[uid]
        role = sess.get("role", "unknown")
        role_str = "school staff 👨‍🏫" if role == "staff" else ("guardian 👨‍👧" if role == "guardian" else "guest")
        await update.message.reply_text(
            f"Welcome back, *{sess.get('name', name)}*! You're verified as {role_str}.\n\n"
            "Ask me anything about students, attendance, or school stats.",
            parse_mode="Markdown",
            reply_markup=REMOVE_KEYBOARD,
        )
        return

    await update.message.reply_text(
        f"👋 Hello *{name}*! I'm the *DVM School Assistant*.\n\n"
        "To get started, please share your phone number so I can verify your identity "
        "and show you the right information.",
        parse_mode="Markdown",
        reply_markup=SHARE_PHONE_KEYBOARD,
    )


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the contact share — verify phone and store session."""
    contact = update.message.contact
    if not contact:
        return

    if not _is_own_contact(update):
        await update.message.reply_text(
            "Please share your own phone number using the button. For privacy, I cannot verify another person's contact.",
            reply_markup=SHARE_PHONE_KEYBOARD,
        )
        return

    phone = contact.phone_number
    uid = str(update.effective_user.id)
    tg_name = update.effective_user.first_name or "User"

    await update.message.reply_text("🔍 Verifying your number...", reply_markup=REMOVE_KEYBOARD)

    result = _verify_phone(phone)
    role = result.get("role", "unknown")
    name = result.get("name") or tg_name
    student_ids = result.get("authorized_student_ids", [])
    student_names = result.get("authorized_student_names", [])

    SESSIONS[uid] = {
        "phone": phone,
        "role": role,
        "name": name,
        "student_ids": student_ids,
        "student_names": student_names,
    }
    _save_sessions(SESSIONS)

    logger.info(f"Verified user {uid} ({phone}) → role={role}, students={student_ids}")

    if role == "staff":
        await update.message.reply_text(
            f"✅ Verified! Welcome, *{name}*.\n\n"
            "You have *full staff access*. You can query any student, attendance, or school statistics.\n\n"
            "Try: _How many students are in Class 5?_",
            parse_mode="Markdown",
        )
    elif role == "guardian":
        kids = ", ".join(student_names) if student_names else "your children"
        await update.message.reply_text(
            f"✅ Verified! Welcome, *{name}*.\n\n"
            f"I can show you information about: *{kids}*\n\n"
            "Try: _Show me my child's attendance_",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            "⚠️ Your phone number was not found in our school records.\n\n"
            "You can still ask about general school information (like class counts or statistics), "
            "but personal student data is restricted.\n\n"
            "If you believe this is an error, please contact the school office.",
            parse_mode="Markdown",
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages — route to agent with role context."""
    uid = str(update.effective_user.id)
    user_text = update.message.text.strip()
    if not user_text:
        return

    # Not yet verified — ask for phone
    if uid not in SESSIONS:
        await update.message.reply_text(
            "Please share your phone number first so I can verify your identity.",
            reply_markup=SHARE_PHONE_KEYBOARD,
        )
        return

    sess = SESSIONS[uid]
    role = sess.get("role", "unknown")
    student_ids = sess.get("student_ids", [])
    student_names = sess.get("student_names", [])
    name = sess.get("name", "User")

    logger.info(f"Message from {uid} ({name}, role={role}): {user_text!r}")

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        reply = agent.ask(
            user_message=user_text,
            role=role,
            authorized_student_ids=student_ids,
            authorized_student_names=student_names,
            user_name=name,
        )
    except Exception as e:
        err_str = str(e)
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
            reply = "⏳ The AI is a bit busy right now. Please try again in a few seconds."
        elif "403" in err_str or "API_KEY" in err_str.upper():
            reply = "⚠️ AI service configuration issue. Please contact the administrator."
        else:
            logger.error(f"Agent error: {e}", exc_info=True)
            reply = "⚠️ Something went wrong. Please try again."

    await update.message.reply_text(reply)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    sess = SESSIONS.get(uid, {})
    role = sess.get("role", "unknown")

    if role == "staff":
        help_text = (
            "*Staff Access — What I can help with:*\n\n"
            "🎓 *Students* — search by name, class, section\n"
            "📊 *Attendance* — any student by name or admission no\n"
            "👨‍🏫 *Staff* — search by name or department\n"
            "📈 *Statistics* — total students, class breakdown\n\n"
            "Just ask naturally in English or Hindi!"
        )
    elif role == "guardian":
        kids = ", ".join(sess.get("student_names", [])) or "your children"
        help_text = (
            f"*Parent Access — Viewing data for: {kids}*\n\n"
            "You can ask:\n"
            "• _My child's attendance_\n"
            "• _Show me my child's class and section_\n"
            "• _Guardian details for my child_\n\n"
            "General school stats are also available."
        )
    else:
        help_text = (
            "Please share your phone number to access student information.\n"
            "Type /start to begin."
        )

    await update.message.reply_text(help_text, parse_mode="Markdown")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Telegram error: {context.error}", exc_info=context.error)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env")
    if not AGENT_API_KEY:
        raise RuntimeError("AGENT_API_KEY is not set in .env")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    logger.info("Bot started — open to all users, phone verification required.")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
