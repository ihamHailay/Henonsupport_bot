from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def language_keyboard():
    return ReplyKeyboardMarkup([['EN', 'AR']], one_time_keyboard=True)

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [['1', '2'], ['3', '4']], one_time_keyboard=True
    )

async def forward_to_operator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    operator_ids = context.bot_data.get('OPERATOR_CHAT_ID', "").split(',')

    # Build optional reply markup for operator
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Mark as Solved", callback_data="solved")],
        [InlineKeyboardButton("↩️ Reply to User", url=f"https://t.me/{user.username}" if user.username else "")]
    ])

    for op_id in operator_ids:
        chat_id = int(op_id.strip())

        # Handle different message types
        if update.message.text:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"🆕 Message from @{user.username or user.id}:\n\n{update.message.text}",
                reply_markup=reply_markup
            )

        elif update.message.voice:
            await update.message.forward(chat_id=chat_id)
        elif update.message.photo:
            await update.message.forward(chat_id=chat_id)
        elif update.message.document:
            await update.message.forward(chat_id=chat_id)
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"Message type not supported from @{user.username or user.id}."
            )
