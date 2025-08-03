import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from handlers.language    import start, chosen, LANG
from handlers.menu        import main_menu, choice, MENU
from handlers.report      import REPORT, handle_report
from handlers.solve       import SOLVE, handle_solve
# ────────────────────────────────────────────────────────────────
# Added imports for the “Get Started with System” flow
from handlers.get_started import (
    GETSTART_BANK, GETSTART_SCHOOL, GETSTART_ACCOUNT,
    GETSTART_LEVEL, GETSTART_ADDRESS, GETSTART_FILE,
    gs_bank, gs_school, gs_account, gs_level, gs_address, gs_file
)

# … inside states:…
    GETSTART_BANK:    [MessageHandler(filters.TEXT & ~filters.COMMAND, gs_bank)],
    GETSTART_SCHOOL:  [MessageHandler(filters.TEXT & ~filters.COMMAND, gs_school)],
    GETSTART_ACCOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, gs_account)],
    GETSTART_LEVEL:   [MessageHandler(filters.TEXT & ~filters.COMMAND, gs_level)],
    GETSTART_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, gs_address)],
    GETSTART_FILE:    [MessageHandler(filters.Document.ALL,        gs_file)],
# ────────────────────────────────────────────────────────────────

# Load environment variables as you already do
TOKEN       = os.getenv("BOT_TOKEN")
OP_CHAT     = os.getenv("OPERATOR_CHAT_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not (TOKEN and OP_CHAT and WEBHOOK_URL):
    raise RuntimeError("BOT_TOKEN, OPERATOR_CHAT_ID, and WEBHOOK_URL must be set")

# Build the bot application
app = ApplicationBuilder().token(TOKEN).build()
app.bot_data["OPERATOR_CHAT_ID"] = OP_CHAT

# Register your ConversationHandler, now including states 4–9
conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LANG:   [MessageHandler(filters.Regex("^(EN|AR)$"), chosen)],
        # Allow options 1–5 in the main menu
        MENU:   [MessageHandler(filters.Regex("^[1-5]$"), choice)],
        REPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_report)],
        SOLVE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_solve)],

        # Get Started with System flow
        GETSTART_BANK:    [MessageHandler(filters.TEXT & ~filters.COMMAND, gs_bank)],
        GETSTART_SCHOOL:  [MessageHandler(filters.TEXT & ~filters.COMMAND, gs_school)],
        GETSTART_ACCOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, gs_account)],
        GETSTART_LEVEL:   [MessageHandler(filters.TEXT & ~filters.COMMAND, gs_level)],
        GETSTART_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, gs_address)],
        GETSTART_FILE:    [MessageHandler(filters.Document.ALL,           gs_file)],
    },
    fallbacks=[CommandHandler("cancel", lambda u, c: c.bot.send_message(
        chat_id=u.effective_chat.id,
        text="Operation cancelled."
    ))],
)
app.add_handler(conv)

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
