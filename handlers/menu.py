from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from .utils import main_menu_keyboard
from .report import REPORT
from .solve import SOLVE, COMMON_ISSUES

MENU = 1

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "What issue you want to send to Henua?\n"
        "1) Report Issue\n"
        "2) Solve Problem\n"
        "3) See Manual\n"
        "4) See Video Manual",
        reply_markup=main_menu_keyboard()
    )
    return MENU

async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == '1':
        await update.message.reply_text(
            "Please describe the issue you want to report:"
        )
        return REPORT

    if text == '2':
        # Show the keyboard of common issues and go to SOLVE
        kb = ReplyKeyboardMarkup(
            [[issue] for issue in COMMON_ISSUES],
            one_time_keyboard=True
        )
        await update.message.reply_text(
            "Choose your problem:", reply_markup=kb
        )
        return SOLVE

    if text == '3':
        await update.message.reply_text(
            "User manual: https://example.com/manual"
        )
        return ConversationHandler.END

    if text == '4':
        await update.message.reply_text(
            "Video manual: https://example.com/video"
        )
        return ConversationHandler.END

    # Invalid choice
    await update.message.reply_text("Please choose 1–4.")
    return MENU
