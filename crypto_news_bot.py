import logging
import os
import sys
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
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

async def run_bot():
    """Start the bot asynchronously"""
    if not BOT_TOKEN:
        logger.critical("FATAL: BOT_TOKEN is missing! Update it in Render Dashboard -> Environment.")
        return

    try:
        logger.info(f"Starting Redirect Bot for {POLYSSIGHTS_BOT}...")
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_any_message))
        
        # Initialize and start polling
        # We use run_polling within the managed loop
        logger.info("Bot is now polling...")
        
        # Using a more robust entry point for PTB v20+
        await application.initialize()
        await application.start()
        await application.updater.start_polling(drop_pending_updates=True)
        
        # Keep the bot running
        # This is the async equivalent of idle()
        stop_event = asyncio.Event()
        await stop_event.wait()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
    finally:
        if 'application' in locals():
            await application.stop()
            await application.shutdown()

def main():
    """Main entry point to handle the event loop"""
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Main loop error: {e}")

if __name__ == '__main__':
    main()
