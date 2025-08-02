import os
# from dotenv import load_dotenv # <-- Comment this line out
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

if not (TOKEN and OP_CHAT):
    raise RuntimeError("BOT_TOKEN and OPERATOR_CHAT_ID must be set in .env")

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

# 4) Run polling (sync) so Render sees the port open
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8443))
    print(f"Starting polling. (Render health-check will see this process bound.)")
    app.run_polling()
