import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from deep_translator import GoogleTranslator

user_languages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Вітання! Надішліть /translate у відповідь на повідомлення, щоб перекласти.\n"
        "Або /setlang [код_мови], щоб змінити мову перекладу."
    )

async def setlang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Використання: /setlang <код_мови> (наприклад, /setlang uk)")
        return

    lang = context.args[0].lower()
    user_languages[update.effective_user.id] = lang
    await update.message.reply_text(f"✅ Мова перекладу встановлена: {lang}")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    target_lang = user_languages.get(user_id, 'uk')

    # Визначаємо текст для перекладу
    if update.message.reply_to_message and update.message.reply_to_message.text:
        text_to_translate = update.message.reply_to_message.text
    else:
        text_to_translate = " ".join(context.args)

    if not text_to_translate:
        await update.message.reply_text("❗ Напишіть /translate у відповідь на повідомлення або додайте текст для перекладу.")
        return

    try:
        # Deep-translator не робить автоматичне визначення мови, тому для прикладу використаємо GoogleTranslator з source='auto'
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text_to_translate)
        await update.message.reply_text(
            f"🔁 Переклад (→ {target_lang}):\n{translated_text}"
        )
    except Exception as e:
        await update.message.reply_text(f"❗ Помилка перекладу: {e}")

def main():
    app = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setlang", setlang))
    app.add_handler(CommandHandler("translate", translate))
    app.run_polling()

if __name__ == "__main__":
    main()
