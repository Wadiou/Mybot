import logging
import os
from telegram import Update, User
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = os.getenv('TOKEN')
YOUR_USER_ID = 2011056922  # Your Telegram ID

user_profiles = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


async def start(update: Update, context: CallbackContext):
    menu_message = (
        "Welcome to the bot!\n\n"
        "I will forward your messages to the admin. "
        "Feel free to send your message anytime.\n\n"
        "You'll receive a confirmation when your message is sent successfully."
    )
    await update.message.reply_text(menu_message)


async def store_user_profile(user: User):
    user_profiles[user.id] = {
        'full_name': user.full_name,
        'username': user.username,
        'id': user.id
    }


async def forward_message(update: Update, context: CallbackContext):
    if update.message:
        user = update.message.from_user
        await store_user_profile(user)

        message = (f"From: {user.full_name} (@{user.username})\n"
                   f"ID: {user.id}\n"
                   f"Message: {update.message.text}")

        await context.bot.send_message(chat_id=YOUR_USER_ID, text=message)
        await update.message.reply_text("Your message was sent successfully!")


async def reply(update: Update, context: CallbackContext):
    if update.message.from_user.id != YOUR_USER_ID:
        await update.message.reply_text(
            "Unauthorized! Only the bot admin can use this command.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reply <user_id> <message>")
        return

    user_id = int(context.args[0])
    reply_message = ' '.join(context.args[1:])

    await context.bot.send_message(chat_id=user_id, text=reply_message)
    await update.message.reply_text(
        f"Reply sent to {user_profiles[user_id]['full_name']} (@{user_profiles[user_id]['username']})."
    )


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reply", reply))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))
    application.run_polling()


if __name__ == '__main__':
    main()
