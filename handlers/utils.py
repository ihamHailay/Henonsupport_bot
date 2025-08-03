from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def language_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard for selecting language."""
    return ReplyKeyboardMarkup(
        [['EN', 'AMH']],
        one_time_keyboard=True
    )

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Main menu keyboard with five options."""
    return ReplyKeyboardMarkup(
        [['1', '2', '3'], ['4', '5']],
        one_time_keyboard=True
    )
def nav_back_to_menu():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🔙 Back to Main Menu", callback_data="nav_main")
    ]])

async def forward_to_operator(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str = None
) -> None:
    """
    Forwards an incoming message or a custom summary text to one or more operators.
    
    If `text` is provided, sends that text as a new message (with operator action buttons).
    Otherwise, forwards the original incoming message (preserving media/type).
    """
    user = update.effective_user
    operator_ids = context.bot_data.get('OPERATOR_CHAT_ID', '').split(',')

    # Optional inline buttons for operator actions
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Mark as Solved", callback_data="solved")],
        [InlineKeyboardButton(
            "↩️ Reply to User",
            url=f"https://t.me/{user.username}" if user.username else ""
        )]
    ])

    for op_id in operator_ids:
        chat_id = int(op_id.strip())
        if text:
            # Send the custom summary text
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup
            )
        else:
            # Forward the original incoming message (any type)
            await update.message.forward(chat_id=chat_id)
