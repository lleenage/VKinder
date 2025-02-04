# python -m pip install vk_api
# python -m pip install bs4
from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from private.private import token

from vkbot import VkBot

# token = input('Token: ')
token = token

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


print("Бот запущен")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print(f'Новое сообщение от пользователя с id {event.user_id}: ', end='')

            bot = VkBot(event.user_id, token)
            write_msg(event.user_id, bot.new_message(event.text))

            print(f'"{event.text}"')