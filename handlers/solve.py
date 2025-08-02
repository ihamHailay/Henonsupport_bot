from telegram import Update, ReplyKeyboardMarkup
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
    "Payment error": "Check your card details and try again.",
    "Sync problem": "Ensure you have an active internet connection and restart the app.",
}

async def handle_solve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # First time we ask the user to pick one
    if "asked_solve" not in context.user_data:
        kb = ReplyKeyboardMarkup(
            [[issue] for issue in COMMON_ISSUES],
            one_time_keyboard=True,
        )
        await update.message.reply_text(
            "Choose your problem:", reply_markup=kb
        )
        context.user_data["asked_solve"] = True
        return SOLVE

    # Second invocation: process their selection
    choice = update.message.text
    solution = SOLUTIONS.get(choice)

    if solution:
        # Send the canned solution
        await update.message.reply_text(solution)
    else:
        # Forward the original message to the operator
        await forward_to_operator(update, context)
        # Notify the user
        await update.message.reply_text(
            "I don’t see that issue—you’re being connected to a human operator."
        )

    return ConversationHandler.END
