import logging
import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
# We use .get() without raising an immediate error to allow the process 
# to stay alive long enough for logs to show on Render.
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# The bot to promote
POLYSSIGHTS_BOT = "@polyssightsbot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command - ONLY show the link"""
    try:
        user = update.effective_user
        logger.info(f"User {user.id} started the bot")
        
        welcome_message = f"""
🌟 **MAIN BOT** 🌟

━━━━━━━━━━━━━━━━━━━━━━━━

🔥 **Click below to visit our main bot:**

👉 **{POLYSSIGHTS_BOT}** 👈

━━━━━━━━━━━━━━━━━━━━━━━━

*This bot only redirects to our main analytics bot.*
        """
        
        keyboard = [
            [InlineKeyboardButton("🔥 CLICK HERE FOR MAIN BOT 🔥", url=f"https://t.me/{POLYSSIGHTS_BOT.replace('@', '')}")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error in start_command: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    help_message = f"ℹ️ **HELP**\n\nRedirecting to: {POLYSSIGHTS_BOT}"
    keyboard = [[InlineKeyboardButton("🔥 GO TO MAIN BOT 🔥", url=f"https://t.me/{POLYSSIGHTS_BOT.replace('@', '')}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(help_message, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Always redirect to main bot"""
    redirect_message = f"💡 **Looking for our main bot?**\n\n👉 **{POLYSSIGHTS_BOT}** 👈"
    keyboard = [[InlineKeyboardButton("🔥 GO TO MAIN BOT 🔥", url=f"https://t.me/{POLYSSIGHTS_BOT.replace('@', '')}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(redirect_message, reply_markup=reply_markup, parse_mode='Markdown')

def main():
    """Start the bot"""
    if not BOT_TOKEN:
        logger.critical("FATAL: BOT_TOKEN is missing! Update it in Render Dashboard -> Environment.")
        sys.exit(1)

    try:
        logger.info(f"Starting Redirect Bot for {POLYSSIGHTS_BOT}...")
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_any_message))
        
        logger.info("Bot is now polling...")
        application.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == '__main__':
    main()
