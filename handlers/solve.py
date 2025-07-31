from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from .utils import forward_to_operator
from telegram.ext import ConversationHandler

SOLVE = 3
COMMON_ISSUES = [
    "Login failure",
    "Payment error",
    "Sync problem"
]
SOLUTIONS = {
    "Login failure": "Please reset your password here: https://...",
    "Payment error": "Check your card details and try again.",
    "Sync problem": "Ensure you have an active internet connection and try restarting the app."
}

async def handle_solve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # First invocation: show the issues keyboard
    if 'asked_solve' not in context.user_data:
        kb = ReplyKeyboardMarkup(
            [[issue] for issue in COMMON_ISSUES],
            one_time_keyboard=True
        )
        await update.message.reply_text(
            "Choose your problem:", reply_markup=kb
        )
        context.user_data['asked_solve'] = True
        return SOLVE

    # Second invocation: process the chosen issue
    choice = update.message.text
    solution = SOLUTIONS.get(choice)
    if solution:
        await update.message.reply_text(solution)
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "I don’t see that issue—you’re being connected to a human operator."
        )
        forward_to_operator(
            bot=context.bot,
            chat_id=int(context.bot_data['OPERATOR_CHAT_ID']),
            user=update.effective_user,
            message_text=f"Help needed with: {choice}"
        )
        return ConversationHandler.END