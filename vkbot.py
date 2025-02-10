from pprint import pprint

import requests
import json
from datetime import date, datetime
from dateutil import relativedelta

from private.private import token, my_token


# token = ""
# my_token - токен которые я получила для себя через приложение(используется не для сообщества)


class VkBot:
    def __init__(self, vk_token, user_id, version="5.131"):
        self.user_id = user_id
        self.base_url = 'https://api.vk.com/method/'
        self.token = vk_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.user_first_name = None
        self.user_last_name = None
        self.user_sex = None
        self.user_bdate = None
        self.user_city = None

        self.test_commands = ["ГОРОД", "ПОЛ", "ВОЗРАСТ", "ИМЯ", "ФАМИЛИЯ", "ФОТО"]
        self.commands = ["ПРИВЕТ", "ПОКА", "НАЙТИ ПАРУ", "ДОБАВИТЬ ПРЕДПОЧТЕНИЯ", "СЛЕДУЮЩИЙ", "ПОДХОДИТ",
                         "НЕ ПОДХОДИТ", "ПОКАЗАТЬ АНКЕТУ"]

    # методы для получения информации пользователя
    def get_user_data(self):
        url = self.base_url + 'users.get?'
        param = {
            **self.params,
            'user_ids': self.user_id,
            'fields': 'city, sex, bdate, about'
        }
        response = requests.get(url, params=param)
        assert response.status_code == 200
        data = response.json()['response'][0]
        self.user_first_name = data.get('first_name')
        self.user_last_name = data.get('last_name')
        if data.get('sex') == 1:
            self.user_sex = 'Женский'
        elif data.get('sex') == 2:
            self.user_sex = 'Мужской'
        else:
            self.user_sex = 'Не указан'

        day1, month1, year1 = data.get('bdate').split('.')
        date1 = datetime(int(year1), int(month1), int(day1))
        day2, month2, year2 = date.today().strftime('%d.%m.%Y').split('.')
        date2 = datetime(int(year2), int(month2), int(day2))
        diff = relativedelta.relativedelta(date2, date1)
        years = diff.years

        self.user_bdate = '{} лет(года)'.format(years)
        self.user_city = data['city'].get('title')

    def get_photo_id(self, my_token):
        url = f"{self.base_url}photos.get"
        param = {
            'access_token': my_token,
            'v': self.version,
            "owner_id": self.user_id,
            "album_id": "profile",
            "extended": 1
        }
        response = requests.get(url, params=param)
        photos_dict = {}
        # вводим словарь, где ключок будет количество лайков, а зачением - ссылка
        # в цикле перебираем всю информацию о фотографиях и составляем словарь
        for photo in response.json()['response']['items']:
            likes_count = photo['likes']['count']
            photo_id = photo['id']
            photos_dict[likes_count] = photo_id

        photos_id = []
        # Получаем 1 фото
        inverse = [key for key in photos_dict.keys()]
        max_key = max(inverse)
        photos_id.append(photos_dict.pop(max_key))
        # Получаем 2 фото
        inverse = [key for key in photos_dict.keys()]
        max_key = max(inverse)
        photos_id.append(photos_dict.pop(max_key))
        # Получаем 3 фото
        inverse = [key for key in photos_dict.keys()]
        max_key = max(inverse)
        photos_id.append(photos_dict.pop(max_key))

        return photos_id

    def send_photo(self, owner_id):
        url = f"{self.base_url}messages.send"

        all_photo = []
        photo_ids = self.get_photo_id(my_token)
        for photo_id in photo_ids:
            param = {
                **self.params,
                'user_id': self.user_id,
                'random_id': 0,
                'attachment': f'photo{owner_id}_{photo_id}'
            }

            response = requests.get(url, params=param)
            all_photo.append(response.json())
        return all_photo

    #метод, позволяющий боту найти подходящих кандидатов после указания предпочтений
    def find_lover(self):
        pass

    # метод получения предпочтений пользователя
    def get_preferences(self):
        pass

    # метод добавления в избранные кандидаты
    def add_favorite(self):
        pass

    # метод для добавления пользователя в черный список
    def add_blacklist(self):
        pass

    # метод перехода к следующему пользователю
    def next_user(self):
        pass

    # метод, выводящий список фаворитов для каждого пользователя
    def show_favorite(self):
        pass

    # метод по обработке тех или иных сообщений
    def new_message(self, message):
        self.get_user_data()
        self.get_photo_id(my_token) #тут будет немного исправлено, когда мы уже будет работать с анкетами других пользвателей
        if message.upper() == self.commands[0]:
            # нужны ли нам в этой переменной, помимо приветствия, правила использования и возмжности?
            if self.user_city is None:
                # в будущем перенесем это сообщение, когда пользователь напишет что-то вроде "найти пару"
                send_message = f"Привет, {self.user_first_name}! Тебе нужно указать город в котором ты живешь, иначе я не смогу подобрать тебе пару"
            else:
                send_message = f"Привет, {self.user_first_name}!"
            return send_message

        elif message.upper() == self.commands[1]:
            return f"До встречи, {self.user_first_name}!"

        #test
        elif message.upper() == self.test_commands[0]:
            send_message = f"Твой город - {self.user_city}"
            return send_message
        elif message.upper() == self.test_commands[1]:
            send_message = f"Твой пол - {self.user_sex}"
            return send_message
        elif message.upper() == self.test_commands[2]:
            send_message = f"Твой возраст - {self.user_bdate}"
            return send_message
        elif message.upper() == self.test_commands[3]:
            send_message = f"Твое имя - {self.user_first_name}"
            return send_message
        elif message.upper() == self.test_commands[4]:
            send_message = f"Твоя фамилия - {self.user_last_name}"
            return send_message
        elif message.upper() == self.test_commands[5]:
            self.send_photo(self.user_id)
            send_message = f"Вот твое фото"
            return send_message

        else:
            return "Я пока не знаю такой команды. 😞"


if __name__ == '__main__':
    user_id = '136220003'
    vk_token = token

    VK = VkBot(vk_token, user_id)
    # send = VK.send_photo(user_id)
    # print(send)
    # photo = VK.get_photo(my_token)
    # pprint(photo)
    get_user = VK.get_user_data()
    print(
        f'Информация о пользователе:\nИмя: {VK.user_first_name}\nФамилия: {VK.user_last_name}\nПол: {VK.user_sex}\nДата рождения: {VK.user_bdate}\nГород: {VK.user_city}')
