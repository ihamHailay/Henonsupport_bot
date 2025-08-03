from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from .utils import forward_to_operator, nav_back_to_menu

# State constant for ConversationHandler
REPORT = 2

async def handle_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles user input for reporting an issue.
    Forwards the message to the operator and acknowledges the user with a
    “Back to Main Menu” navigation button.
    """
    # Forward the message to operator(s)
    await forward_to_operator(update, context)

    # Confirm to the user with a nav button
    await update.message.reply_text(
        "✅ Your issue has been sent to the support team.",
        reply_markup=nav_back_to_menu()
    )

    return ConversationHandler.END
