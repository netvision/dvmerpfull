"""
bot.py — Telegram bot entry point.
Handles incoming messages, enforces the allowlist, and delegates to the agent.
"""

import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

import agent  # noqa — imports after dotenv so GEMINI_API_KEY is set

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
_raw_ids = os.getenv("ALLOWED_TELEGRAM_IDS", "")
ALLOWED_IDS: set[int] = set(
    int(x.strip()) for x in _raw_ids.split(",") if x.strip().isdigit()
)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_allowed(update: Update) -> bool:
    """Check if the user is on the allowlist. If allowlist is empty, deny all."""
    if not ALLOWED_IDS:
        return False
    return update.effective_user.id in ALLOWED_IDS

# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    if not _is_allowed(update):
        await update.message.reply_text(
            "⛔ Access denied. Please contact the school administrator to get access."
        )
        logger.warning(f"Unauthorized /start from user {update.effective_user.id}")
        return

    name = update.effective_user.first_name or "there"
    await update.message.reply_text(
        f"👋 Hello {name}! I'm the *DVM School ERP Assistant*.\n\n"
        "You can ask me questions like:\n"
        "• _How many students are in Class 5?_\n"
        "• _Find student Arjun Sharma_\n"
        "• _What is admission no 2024/101's attendance?_\n"
        "• _Show me the Maths department staff_\n"
        "• _School statistics_\n\n"
        "I support both English and Hindi. Go ahead and ask!",
        parse_mode="Markdown",
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    if not _is_allowed(update):
        await update.message.reply_text("⛔ Access denied.")
        return

    await update.message.reply_text(
        "*What can I help you with?*\n\n"
        "🎓 *Students*\n"
        "  • Search by name or admission number\n"
        "  • Get full profile (guardian, class, DOB)\n"
        "  • Check attendance\n\n"
        "👨‍🏫 *Staff*\n"
        "  • Search by name or department\n\n"
        "📊 *Statistics*\n"
        "  • Total students, class-wise breakdown\n"
        "  • Gender distribution\n\n"
        "Just type your question naturally!",
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all incoming text messages."""
    if not _is_allowed(update):
        await update.message.reply_text(
            "⛔ You are not authorized to use this bot.\n"
            "Please contact the school administrator."
        )
        logger.warning(
            f"Unauthorized message from user {update.effective_user.id} "
            f"(@{update.effective_user.username}): {update.message.text!r}"
        )
        return

    user_text = update.message.text.strip()
    if not user_text:
        return

    logger.info(
        f"Message from {update.effective_user.id} "
        f"(@{update.effective_user.username}): {user_text!r}"
    )

    # Show typing indicator while the agent thinks
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    try:
        reply = agent.ask(user_text)
    except Exception as e:
        err_str = str(e)
        if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
            reply = "⏳ The AI is a bit busy right now. Please try again in a few seconds."
        elif "403" in err_str or "API_KEY" in err_str.upper():
            reply = "⚠️ AI service configuration issue. Please contact the administrator."
        else:
            logger.error(f"Agent error: {e}", exc_info=True)
            reply = "⚠️ Something went wrong. Please try again."

    await update.message.reply_text(reply, parse_mode="Markdown")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors from the Telegram library."""
    logger.error(f"Telegram error: {context.error}", exc_info=context.error)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env")
    if not ALLOWED_IDS:
        raise RuntimeError(
            "ALLOWED_TELEGRAM_IDS is empty. Add at least one Telegram user ID to .env"
        )

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    logger.info(f"Bot starting. Allowed user IDs: {ALLOWED_IDS}")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
