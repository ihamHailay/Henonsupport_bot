from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from .utils import forward_to_operator

# State constant for ConversationHandler
REPORT = 2

async def handle_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles user input for reporting an issue.
    Forwards the message to the operator and acknowledges the user.
    """
    # Forward the message to operator(s)
    await forward_to_operator(update, context)

    # Confirm to the user
    await update.message.reply_text("✅ Your issue has been sent to the support team.")
    return ConversationHandler.END
