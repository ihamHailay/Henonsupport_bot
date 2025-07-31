from telegram import Update
from telegram.ext import ContextTypes
from .utils import language_keyboard

LANG = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Choose language / Amharic:",
        reply_markup=language_keyboard()
    )
    return LANG

async def chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ctx = context.user_data
    ctx['lang'] = update.message.text
    # proceed to main menu
    from .menu import main_menu
    return await main_menu(update, context)