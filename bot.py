import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from handlers.language import start, chosen, LANG
from handlers.menu     import main_menu, choice, MENU
from handlers.report   import REPORT, handle_report
from handlers.solve    import SOLVE, handle_solve

# 1) Load environment
load_dotenv()
TOKEN      = os.getenv("BOT_TOKEN")
OP_CHAT    = os.getenv("OPERATOR_CHAT_ID")
WEBHOOK_URL= os.getenv("WEBHOOK_URL")  # e.g. https://your-service.onrender.com

if not (TOKEN and OP_CHAT and WEBHOOK_URL):
    raise RuntimeError("BOT_TOKEN, OPERATOR_CHAT_ID, and WEBHOOK_URL must be set in .env")

# 2) Build the bot application
app = ApplicationBuilder().token(TOKEN).build()
app.bot_data["OPERATOR_CHAT_ID"] = OP_CHAT

# 3) ConversationHandler setup
conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LANG:   [MessageHandler(filters.Regex("^(EN|AR)$"), chosen)],
        MENU:   [MessageHandler(filters.Regex("^[1-4]$"), choice)],
        REPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_report)],
        SOLVE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_solve)],
    },
    fallbacks=[CommandHandler("cancel", lambda u, c: c.bot.send_message(
        chat_id=u.effective_chat.id, text="Operation cancelled."
    ))],
)
app.add_handler(conv)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8443))
    # This method does:
    # 1) initialize the internal bot
    # 2) call set_webhook under the hood
    # 3) start an HTTPS server on 0.0.0.0:port
    # 4) begin listening for Telegram POSTs
    print("Starting webhook on port", port)
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}",
    )
