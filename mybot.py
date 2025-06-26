from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, ConversationHandler
)

# Вставь сюда токен от BotFather
TOKEN = '7979092246:AAF5W93CR2QYHlxCApLGN9v5RL1sGgzlp3g'

# Этапы диалога
CATEGORY, MESSAGE = range(2)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        ['🛰 Телекоммуникация', '🏛 Рақамли ҳукумат'],
        ['🎓 Рақамли таълим', '💻 IT Park'],
        ['📬 Почта']
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Ассалому алайкум!!! \nDigital Namangan ботига Хуш келибсиз!\nИлтимос, мурожаат турини танланг:", reply_markup=keyboard)
    return CATEGORY

# Обработка категории
async def choose_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["category"] = update.message.text
    await update.message.reply_text("Илтимос, мурожаат матнини ёзинг:")
    return MESSAGE

# Обработка текста жалобы
async def receive_complaint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = context.user_data["category"]
    message = update.message.text
    username = update.message.from_user.username or "username not found"
    name = update.message.from_user.full_name
    complaint = (
        f"📣 ЯНГИ МУРОЖААТ\n"
        f"👤 Фойдаланувчи: {name} (@{username})\n"
        f"📂 Бўлим: {category}\n"
        f"📝 Матн: {message}"
    )

    # Отправка админу (сюда вставь свой Telegram ID)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Раҳмат! Мурожаатингиз қабул қилинди.")
    await context.bot.send_message(chat_id=469942406, text=complaint)

    return ConversationHandler.END

# Команда /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Мурожаат бекор қилинди.")
    return ConversationHandler.END

# Запуск
app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CATEGORY: [MessageHandler(filters.TEXT, choose_category)],
        MESSAGE: [MessageHandler(filters.TEXT, receive_complaint)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)
app.run_polling()