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
        "Great! Now please attach your **Excel file** (as a document)."
    )
    return GETSTART_FILE

async def gs_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Collect the document
    doc = update.message.document
    file_id = doc.file_id

    # Build a summary text
    summary = (
        f"🆕 New system setup request:\n"
        f"• Bank: {context.user_data['bank']}\n"
        f"• School: {context.user_data['school']}\n"
        f"• Account: {context.user_data['account']}\n"
        f"• Level: {context.user_data['level']}\n"
        f"• Address: {context.user_data['address']}\n"
    )

    # Forward summary as text
    await forward_to_operator(update, context, text=summary)

    # Forward the Excel document itself
    await context.bot.send_document(
        chat_id=int(context.bot_data['OPERATOR_CHAT_ID']),
        document=file_id,
        filename=doc.file_name
    )

    # Acknowledge user
    await update.message.reply_text("✅ Your setup request has been sent!")
    return ConversationHandler.END
