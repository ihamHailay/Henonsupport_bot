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

# 1) Load .env
load_dotenv()
TOKEN   = os.getenv("BOT_TOKEN")
OP_CHAT = os.getenv("OPERATOR_CHAT_ID")
print("Loaded operator ID:", OP_CHAT)  # Add this line after loading .env

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in .env")

# 2) Build the Application once
app = ApplicationBuilder().token(TOKEN).build()

# 3) Make OPERATOR_CHAT_ID available to handlers
app.bot_data["OPERATOR_CHAT_ID"] = OP_CHAT

# 4) Create your ConversationHandler
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

# 5) Register the handler
app.add_handler(conv)

# 6) Run polling (sync)
if __name__ == "__main__":
    print("Bot is up and running—send /start in Telegram to test.")
    app.run_polling()
