import os
# from dotenv import load_dotenv
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

# 1) Load environment variables from Render's dashboard
# load_dotenv() # <-- This line should be removed or commented out
TOKEN      = os.getenv("BOT_TOKEN")
OP_CHAT    = os.getenv("OPERATOR_CHAT_ID")

if not (TOKEN and OP_CHAT):
    raise RuntimeError("BOT_TOKEN and OPERATOR_CHAT_ID must be set in Render's environment variables")

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

# 4) Run polling
if __name__ == "__main__":
    print("Starting bot polling...")
    app.run_polling()
