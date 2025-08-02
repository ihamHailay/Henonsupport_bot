import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

# Import your handlers
from handlers.language import start, chosen, LANG
from handlers.menu     import main_menu, choice, MENU
from handlers.report   import REPORT, handle_report
from handlers.solve    import SOLVE, handle_solve

# 1) Load environment
load_dotenv()
TOKEN    = os.getenv("BOT_TOKEN")
OP_CHAT  = os.getenv("OPERATOR_CHAT_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-service.onrender.com

if not TOKEN or not WEBHOOK_URL:
    raise RuntimeError("BOT_TOKEN and WEBHOOK_URL must be set in .env")

# 2) Build the Telegram application
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Make OPERATOR_CHAT_ID available to handlers
telegram_app.bot_data["OPERATOR_CHAT_ID"] = OP_CHAT

# 3) Set up your ConversationHandler
conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LANG:   [MessageHandler(filters.Regex("^(EN|AR)$"), chosen)],
        MENU:   [MessageHandler(filters.Regex("^[1-4]$"), choice)],
        REPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_report)],
        SOLVE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_solve)],
    },
    fallbacks=[CommandHandler("cancel", lambda upd, ctx: ctx.bot.send_message(
        chat_id=upd.effective_chat.id,
        text="Operation cancelled."
    ))],
)
telegram_app.add_handler(conv)

# 4) Create a minimal Flask app to receive webhooks
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook_handler():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    telegram_app.process_update(update)
    return "OK"

if __name__ == "__main__":
    # 5) Start webhook listener and register with Telegram
    #    Listen on 0.0.0.0:8443 and tell Telegram to post updates here:
    webhook_path = f"/{TOKEN}"
    print("Starting Flask server and setting webhook to", WEBHOOK_URL + webhook_path)
    # Set the webhook with Telegram
    telegram_app.bot.set_webhook(url=WEBHOOK_URL + webhook_path)
    # Run Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8443)))
