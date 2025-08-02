import os
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

# Load .env

TOKEN         = os.getenv("BOT_TOKEN")
OP_CHAT       = os.getenv("OPERATOR_CHAT_ID")
WEBHOOK_URL   = os.getenv("WEBHOOK_URL")  # e.g. https://your-render-url.com

if not (TOKEN and OP_CHAT and WEBHOOK_URL):
    raise RuntimeError("BOT_TOKEN, OPERATOR_CHAT_ID, WEBHOOK_URL must be set")

# Build the bot application
app = ApplicationBuilder().token(TOKEN).build()
app.bot_data["OPERATOR_CHAT_ID"] = OP_CHAT

# Register your ConversationHandler, as before
conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LANG:   [MessageHandler(filters.Regex("^(EN|AR)$"), chosen)],
        MENU:   [MessageHandler(filters.Regex("^[1-4]$"), choice)],
        REPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_report)],
        SOLVE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_solve)],
    },
    fallbacks=[CommandHandler("cancel", lambda u,c: c.bot.send_message(
        chat_id=u.effective_chat.id,
        text="Operation cancelled."
    ))],
)
app.add_handler(conv)

if __name__ == "__main__":
    # Use the PORT Render assigns (default 10000 or $PORT)
    port = int(os.environ.get("PORT", "10000"))
    # The path Telegram will post to must exactly match TOKEN
    path = f"/{TOKEN}"
    # Start webhook (this sets Telegram’s webhook under the hood)
    print(f"Starting webhook on port {port}, URL {WEBHOOK_URL}{path}")
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}{path}"
    )
