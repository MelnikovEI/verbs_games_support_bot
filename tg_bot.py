import logging
import telegram
from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from detect_intent import detect_intent_text
from telegram_logs_handler import TelegramLogsHandler

logger = logging.getLogger(__name__)
adm_logger = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Это помощник компании «Игра глаголов», спросите меня и я постараюсь помочь.')


def reply(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    answer = detect_intent_text(
        google_cloud_project,
        update.effective_user.id,
        update.message.text,
        'ru'
    )
    if answer:
        update.message.reply_text(answer)
    logger.info(f"effective_user: {update.effective_user}")


def main() -> None:
    tg_bot_token = env('TG_BOT_TOKEN')
    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
    adm_logger.info("Бот запущен")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
    env = Env()
    env.read_env()
    google_cloud_project = env('GOOGLE_CLOUD_PROJECT')

    tg_admin_bot_token = env('TG_ADMIN_BOT_TOKEN')
    chat_id = env('ADMIN_CHAT_ID')
    admin_bot = telegram.Bot(token=tg_admin_bot_token)
    adm_logger.setLevel(logging.WARNING)
    adm_logger.addHandler(TelegramLogsHandler(admin_bot, chat_id))

    try:
        main()
    except Exception as err:
        adm_logger.error(err, exc_info=True)
