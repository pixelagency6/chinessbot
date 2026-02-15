import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable not set!")
    raise ValueError("BOT_TOKEN environment variable not set!")

# The bot to promote
POLYSSIGHTS_BOT = "@polyssightsbot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command - ONLY show the link"""
    try:
        user = update.effective_user
        logger.info(f"User {user.id} started the bot")
        
        # Simple message ONLY showing the link
        welcome_message = f"""
🌟 **MAIN BOT** 🌟

━━━━━━━━━━━━━━━━━━━━━━━━

🔥 **Click below to visit our main bot:**

👉 **{POLYSSIGHTS_BOT}** 👈

━━━━━━━━━━━━━━━━━━━━━━━━

*This bot only redirects to our main analytics bot.*
        """
        
        # Create a single, prominent button
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
        await update.message.reply_text(f"Error. Please visit: {POLYSSIGHTS_BOT}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message - also only shows the link"""
    help_message = f"""
ℹ️ **HELP**

This bot redirects you to our main analytics bot:

👉 **{POLYSSIGHTS_BOT}** 👈

Click the button below or use /start
"""
    
    keyboard = [
        [InlineKeyboardButton("🔥 GO TO MAIN BOT 🔥", url=f"https://t.me/{POLYSSIGHTS_BOT.replace('@', '')}")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        help_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle ANY message - always redirect to main bot"""
    if update.message and update.message.text and not update.message.text.startswith('/'):
        # For any text message, show the link
        redirect_message = f"""
💡 **Looking for our main bot?**

👉 **{POLYSSIGHTS_BOT}** 👈

Click below or use /start
"""
        
        keyboard = [
            [InlineKeyboardButton("🔥 GO TO MAIN BOT 🔥", url=f"https://t.me/{POLYSSIGHTS_BOT.replace('@', '')}")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            redirect_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks - just acknowledge"""
    query = update.callback_query
    await query.answer("Redirecting to main bot...")

def main():
    """Start the bot"""
    try:
        logger.info("Starting Redirect Bot for @polyssightsbot...")
        logger.info(f"Bot will ONLY show link to: {POLYSSIGHTS_BOT}")
        
        # Create Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        
        # Add callback query handler for buttons
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Handle ALL other messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message))
        application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_any_message))
        
        # Start the bot
        logger.info("Redirect bot is now polling for updates...")
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == '__main__':
    main()
