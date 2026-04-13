TOKEN = '8467075810:AAFn-tDbHMAZ8GhhmdpIK64D3SpawEXT9Ho'
ADMIN_ID = 7274312890
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from config import ADMIN_ID  

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Admin bilan bog'lanish", url='https://t.me/alpomishmamanazarov')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Salom {update.effective_user.first_name}! Link yuboring:",
        reply_markup=reply_markup
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("Admin panelga xush kelibsiz!")
    else:
        await update.message.reply_text("Kechirasiz, ruxsat yo'q.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "instagram.com" in text:
        await update.message.reply_text("Instagram linki qabul qilindi...")
    else:
        await update.message.reply_text("Iltimos, link yuboring.")
        from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import TOKEN
from handlers import start, admin, handle_message

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlerlarni qo'shish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot ishlamoqda...")
    app.run_polling()
