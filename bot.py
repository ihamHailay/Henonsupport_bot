import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
)
from handlers.language import start, chosen, LANG
from handlers.menu import main_menu, choice, MENU, main_menu_keyboard
from handlers.report import REPORT, handle_report
from handlers.solve import SOLVE, handle_solve
from handlers.utils import nav_back_to_menu

# “Get Started with System” flow
from handlers.get_started import (
    GETSTART_BANK, GETSTART_SCHOOL, GETSTART_ACCOUNT,
    GETSTART_LEVEL, GETSTART_ADDRESS, GETSTART_FILE,
    gs_bank, gs_school, gs_account, gs_level, gs_address, gs_file
)

# Load environment variables
TOKEN       = os.getenv("BOT_TOKEN")
OP_CHAT     = os.getenv("OPERATOR_CHAT_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not (TOKEN and OP_CHAT and WEBHOOK_URL):
    raise RuntimeError("BOT_TOKEN, OPERATOR_CHAT_ID, and WEBHOOK_URL must be set")

# Build the bot
app = ApplicationBuilder().token(TOKEN).build()
app.bot_data["OPERATOR_CHAT_ID"] = OP_CHAT

# Navigation: back to main menu (returns to MENU state)
async def nav_handler(update, context):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "What issue you want to send to Henua?\n"
        "1) Report Issue\n"
        "2) Solve Problem\n"
        "3) See Manual\n"
        "4) See Video Manual\n"
        "5) Get Started with System",
        reply_markup=main_menu_keyboard()
    )
    return MENU

# Define the conversation handler with nav_handler included in all states
conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LANG: [
            MessageHandler(filters.Regex("^(EN|AR)$"), chosen),
            CallbackQueryHandler(nav_handler, pattern="^nav_main$")
        ],
        MENU: [
            MessageHandler(filters.Regex("^[1-5]$"), choice),
            CallbackQueryHandler(nav_handler, pattern="^nav_main$")
        ],
        REPORT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_report),
            CallbackQueryHandler(nav_handler, pattern="^nav_main$")
        ],
        SOLVE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_solve),
            CallbackQueryHandler(nav_handler, pattern="^nav_main$")
        ],
        GETSTART_BANK: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, gs_bank),
            CallbackQueryHandler(nav_handler, pattern="^nav_main$")
        ],
        GETSTART_SCHOOL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, gs_school),
            CallbackQueryHandler(nav_handler, pattern="^nav_main$")
        ],
        GETSTART_ACCOUNT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, gs_account),
            CallbackQueryHandler(nav_handler, pattern="^nav_main$")
        ],
        GETSTART_LEVEL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, gs_level),
            CallbackQueryHandler(nav_handler, pattern="^nav_main$")
        ],
        GETSTART_ADDRESS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, gs_address),
            CallbackQueryHandler(nav_handler, pattern="^nav_main$")
        ],
        GETSTART_FILE: [
            MessageHandler(filters.Document.ALL, gs_file),
            CallbackQueryHandler(nav_handler, pattern="^nav_main$")
        ],
    },
    fallbacks=[
        CommandHandler("cancel", lambda update, context: update.message.reply_text(
            "Operation cancelled."
        ))
    ],
)

# Register the conversation handler
app.add_handler(conv)

# Start webhook
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    path = f"/{TOKEN}"
    print(f"Starting webhook on port {port}, URL {WEBHOOK_URL}{path}")
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}{path}",
    )
