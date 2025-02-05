#pip install vk_api
#pip install requests
from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from private.private import token

from vkbot import VkBot

# token = input('Token: ')
token = token

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)


def write_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


print("Бот запущен")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print(f'Новое сообщение от пользователя с id {event.user_id}: ', end='')

            bot = VkBot(token, event.user_id)
            write_msg(event.user_id, bot.new_message(event.text))

            print(f'"{event.text}"')