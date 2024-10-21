import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Replace with your actual User ID
YOUR_USER_ID = 2011056922  # Your User ID from the previous step

# Bot token from BotFather
TOKEN = '7741750918:AAF2NKPXR4WI_gQztdZ64Xo8sYLKW6un3LU'

# Configure logging to monitor bot activity
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext):
    """Handler for the /start command."""
    await update.message.reply_text("Bot is running! All incoming messages will be forwarded to you.")

async def forward_message(update: Update, context: CallbackContext):
    """Forward all incoming messages to your chat."""
    if update.message:
        user_id = update.message.from_user.id
        first_name = update.message.from_user.first_name
        text = update.message.text

        # Log and forward the message to your Telegram chat
        logging.info(f"From {first_name} (ID: {user_id}): {text}")
        await context.bot.send_message(
            chat_id=YOUR_USER_ID,
            text=f"From {first_name} (ID: {user_id}): {text}"
        )

async def reply(update: Update, context: CallbackContext):
    """Reply to a user with the given user ID."""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reply <user_id> <message>")
        return

    user_id = int(context.args[0])
    reply_message = ' '.join(context.args[1:])

    # Send the reply to the specified user
    await context.bot.send_message(chat_id=user_id, text=reply_message)
    await update.message.reply_text("Reply sent!")

def main():
    """Main function to start the bot."""
    application = ApplicationBuilder().token(TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reply", reply))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
