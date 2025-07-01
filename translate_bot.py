import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters
from googletrans import Translator

translator = Translator()
user_languages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Надішліть /translate у відповідь на повідомлення.\n/setlang [код] — змінити мову.")

async def setlang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Використання: /setlang uk")
        return
    lang = context.args[0].lower()
    user_languages[update.effective_user.id] = lang
    await update.message.reply_text(f"✅ Мову перекладу встановлено: {lang}")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and update.message.reply_to_message.text:
        original = update.message.reply_to_message.text
    else:
        original = " ".join(context.args)

    if not original:
        await update.message.reply_text("❗ Напишіть /translate у відповідь на повідомлення або додайте текст.")
        return

    user_id = update.effective_user.id
    target_lang = user_languages.get(user_id, 'uk')
    translated = translator.translate(original, dest=target_lang)
    await update.message.reply_text(f"🔁 Переклад ({translated.src} → {target_lang}):\n{translated.text}")

app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setlang", setlang))
app.add_handler(CommandHandler("translate", translate))
app.run_polling()
