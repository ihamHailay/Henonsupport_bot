from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, filters
from .utils import forward_to_operator

# State constants
GETSTART_BANK    = 4
GETSTART_SCHOOL  = 5
GETSTART_ACCOUNT = 6
GETSTART_LEVEL   = 7
GETSTART_ADDRESS = 8
GETSTART_FILE    = 9

async def gs_bank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['bank'] = update.message.text
    await update.message.reply_text("Enter your **school name**:")
    return GETSTART_SCHOOL

async def gs_school(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['school'] = update.message.text
    await update.message.reply_text("Enter your **account number**:")
    return GETSTART_ACCOUNT

async def gs_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['account'] = update.message.text
    await update.message.reply_text("Enter your **school level**:")
    return GETSTART_LEVEL

async def gs_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['level'] = update.message.text
    await update.message.reply_text("Enter your **address**:")
    return GETSTART_ADDRESS

async def gs_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['address'] = update.message.text
    await update.message.reply_text(
        "Almost done—please attach your **Excel file** (as a document)."
    )
    return GETSTART_FILE

async def gs_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Build summary text from collected fields
    data = context.user_data
    summary = (
        f"🆕 New system setup request:\n"
        f"• Bank: {data['bank']}\n"
        f"• School: {data['school']}\n"
        f"• Account: {data['account']}\n"
        f"• Level: {data['level']}\n"
        f"• Address: {data['address']}\n"
    )

    # 1) Send the summary text to operators
    await forward_to_operator(update, context, text=summary)

    # 2) Forward the attached Excel document itself
    doc = update.message.document
    await context.bot.send_document(
        chat_id=int(context.bot_data['OPERATOR_CHAT_ID']),
        document=doc.file_id,
        filename=doc.file_name
    )

    # 3) Acknowledge the user
    await update.message.reply_text("✅ Your setup request has been sent to support!")
    return ConversationHandler.END
