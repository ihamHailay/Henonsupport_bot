from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from .utils import forward_to_operator

# State constant
SOLVE = 3

# Predefined problems and solutions
COMMON_ISSUES = [
    "Login failure",
    "Payment error",
    "Sync problem",
]
SOLUTIONS = {
    "Login failure": "Please reset your password here: https://example.com/reset",
    "Payment error":  "Check your card details and try again.",
    "Sync problem":   "Ensure you have an active internet connection and restart the app.",
}

async def handle_solve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Processes the user's selection from the common-issues keyboard.
    Sends a canned solution or forwards unknown issues.
    """
    choice = update.message.text
    solution = SOLUTIONS.get(choice)

    if solution:
        # Send the canned solution directly
        await update.message.reply_text(solution)
    else:
        # Forward any unknown choice to the operator
        await forward_to_operator(update, context)
       await update.message.reply_text("✅ Your issue has been sent to the support team.")
+ from .utils import nav_back_to_menu
+ await update.message.reply_text(
+     "✅ Your issue has been sent to the support team.",
+     reply_markup=nav_back_to_menu()
+ )


    return ConversationHandler.END
