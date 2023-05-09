import logging
import random
import telegram
import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from detect_intent import detect_intent
from telegram_logs_handler import TelegramLogsHandler

logger = logging.getLogger(__name__)
adm_logger = logging.getLogger(__file__)


def reply(event, vk_api, project_id):
    dialogflow_response = detect_intent(
        project_id,
        event.user_id,
        event.text,
        'ru'
    )
    if not dialogflow_response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

    env = Env()
    env.read_env()

    tg_admin_bot_token = env('TG_ADMIN_BOT_TOKEN')
    chat_id = env('ADMIN_CHAT_ID')
    admin_bot = telegram.Bot(token=tg_admin_bot_token)
    adm_logger.setLevel(logging.WARNING)
    adm_logger.addHandler(TelegramLogsHandler(admin_bot, chat_id))

    try:
        vk_group_token = env('VK_GROUP_TOKEN')
        google_cloud_project = env('GOOGLE_CLOUD_PROJECT')
        vk_session = vk.VkApi(token=vk_group_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        adm_logger.info("Бот запущен")
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply(event, vk_api, google_cloud_project)
    except Exception as err:
        adm_logger.error(err, exc_info=True)
