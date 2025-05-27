
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os

# Set your token here directly (or load via env if you deploy securely)
TOKEN: Final = "7635971252:AAGsdhATslkGq95ep4yI6i7pSsydS6_jKQk"
BOT_USERNAME: Final = "@sssaample_bot"

# --- Command Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}, I am a sample bot. "
        f"Thanks for starting me! "
        f"You can call me {BOT_USERNAME}. "
        f"How can I assist you today?"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I can help you with the following commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "Feel free to ask me anything!"
    )

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command response.")

# --- Response Logic ---

def handle_response(text: str) -> str:
    text = text.lower()
    if "hello" in text:
        return "Hello! How can I help you today?"
    elif "how are you" in text:
        return "I'm just a bot, but thanks for asking! How can I assist you?"
    elif "bye" in text:
        return "Goodbye! Have a great day!"
    else:
        return "I'm not sure how to respond to that. Can you please rephrase your question?"

# --- Message Handler ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f"User {update.message.chat.id} in {message_type} sent: {text}")

    response: str = ""

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return  # bot not mentioned, do nothing
    else:
        response = handle_response(text)

    print(f"Response: {response}")
    await update.message.reply_text(response)

# --- Error Handler ---

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("An error occurred. Please try again later.")

# --- Main Execution ---

if __name__ == "__main__":
    print("Starting bot...")
    app = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    print("Polling updates...")
    app.run_polling(poll_interval=3)
    print("Bot started successfully!")
# Note: Make sure to replace the TOKEN with your actual bot token.
