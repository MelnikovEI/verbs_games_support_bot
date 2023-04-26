import logging
import random
import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType
from detect_intent import detect_intent_text

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)


def reply(event, vk_api, google_cloud_project):
    answer = detect_intent_text(
        google_cloud_project,
        event.user_id,
        event.text,
        'ru'
    )
    if answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )


def main() -> None:
    env = Env()
    env.read_env()
    vk_group_token = env('VK_GROUP_TOKEN')
    google_cloud_project = env('GOOGLE_CLOUD_PROJECT')

    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply(event, vk_api, google_cloud_project)


if __name__ == "__main__":
    main()
