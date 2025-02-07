from pprint import pprint

import requests
import json
from datetime import date

from private.private import token, my_token
#my_token - токен которые я получила для себя через приложение(используется не для сообщества)


class VkBot:
    def __init__(self, vk_token, user_id, version="5.131"):
        self.user_id = user_id
        self.base_url = 'https://api.vk.com/method/'
        self.token = vk_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

        self.commands = ["ПРИВЕТ", "ПОКА", "НАЙТИ ПАРУ", "ДОБАВИТЬ ПРЕДПОЧТЕНИЯ", "СЛЕДУЮЩИЙ", "ПОДХОДИТ", "НЕ ПОДХОДИТ"]

    #методы для получения города пользователя
    def get_city(self):
        url = self.base_url + 'users.get?'
        param = {
            **self.params,
            'user_ids': self.user_id,
            'fields': 'city'
        }
        response = requests.get(url, params=param)
        try:
            try:
                users_city = response.json()['response'][0]['title']
                return users_city
            except:
                users_town = response.json()['response'][0]['home_town']
                return users_town
        except:
            return 'Город не указан'

    #метод для получения пола
    def get_sex(self):
        url = self.base_url + 'users.get?'
        param = {
            **self.params,
            'user_ids': self.user_id,
            'fields': 'sex'
        }
        response = requests.get(url, params=param)
        sex = response.json()['response'][0]['sex']
        if sex == 1:
            user_gender = 'Женский пол'
        elif sex == 2:
            user_gender = 'Мужской пол'
        else:
            user_gender = 'Пол не указан'
        return user_gender

    #метод для получения имени и фамилии(
    def get_name(self):
        url = self.base_url + 'users.get?'
        param = {
            **self.params,
            'user_ids': self.user_id,
            'fields': 'about'

        }
        response = requests.get(url, params=param)
        user_first_name = response.json()['response'][0]['first_name']
        user_last_name = response.json()['response'][0]['last_name']

        return user_first_name, user_last_name

    #метод получения возраста(нужно доделать, либо я плохо искала и не нашла нужный метод для получения возраста)
    def get_age(self):
        url = self.base_url + 'users.get?'
        param = {
            **self.params,
            'user_ids': self.user_id,
            'fields': 'bdate'
        }
        response = requests.get(url, params=param)
        try:
            birth_date = response.json()['response'][0]['bdate']
            time_now = date.today().strftime('%d.%m.%Y')

            #тут будет код для вычесления возраста

            return birth_date, time_now
        except:
            return 'Год или дата рождения не указана'

    #метод получения списка из 3 фотографий с наибольшим количеством лайков
    def get_photo(self, my_token):
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
        #вводим словарь, где ключок будет количество лайков, а зачением - ссылка
        #в цикле перебираем всю информацию о фотографиях и составляем словарь
        for photo in response.json()['response']['items']:
            likes_count = photo['likes']['count']
            url = photo['orig_photo']['url']
            photos_dict[likes_count] = url

        photos_url = []
        #Получаем 1 фото
        inverse = [key for key in photos_dict.keys()]
        max_key = max(inverse)
        photos_url.append(photos_dict.pop(max_key))
        #Получаем 2 фото
        inverse = [key for key in photos_dict.keys()]
        max_key = max(inverse)
        photos_url.append(photos_dict.pop(max_key))
        #Получаем 3 фото
        inverse = [key for key in photos_dict.keys()]
        max_key = max(inverse)
        photos_url.append(photos_dict.pop(max_key))
        return photos_url

    def get_group_id(self):
        url = f"{self.base_url}photos.getMessagesUploadServer"
        param = {
            **self.params,
            'peer_id': user_id
        }
        response = requests.get(url, params=param).json()
        return response

    def upload_photo(self):
        url = f"{self.base_url}photos.saveMessagesPhoto"

    #метод, позволяющий боту найти подходящих кандидатов после указания предпочтений
    def find_lover(self):
        pass

    #метод получения предпочтений пользователя
    def get_preferences(self):
        pass

    # метод добавления в избранные кандидаты
    def add_favorite(self):
        pass

    #метод для добавления пользователя в черный список
    def add_blacklist(self):
        pass

    #метод перехода к следующему пользователю
    def next_user(self):
        pass

    #метод, выводящий список фаворитов для каждого пользователя
    def show_favorite(self):
        pass

    #метод по обработке тех или иных сообщений
    def new_message(self, message):
        if message.upper() == self.commands[0]:
            self.get_name()
            self.get_age()
            self.get_sex()
            self.get_city()
            self.get_photo(my_token)
            #нужны ли нам в этой переменной, помимо приветствия, правила использования и возмжности?
            if self.get_city() == 'Город не указан':
                #в будущем перенесем это сообщение, когда пользователь напишет что-то вроде "найти пару"
                send_message = f"Привет, {self.get_name()[0]}! Тебе нужно указать город в котором ты живешь, иначе я не смогу подобрать тебе пару"
            else:
                send_message = f"Привет, {self.get_name()[0]}!"
            return send_message

        elif message.upper() == self.commands[1]:
            return f"До встречи, {self.get_name()[0]}!"

        else:
            return "Я пока не знаю такой команды. 😞"

if __name__ == '__main__':
    user_id = '821271818'
    vk_token = token
    my_token = my_token

    VK = VkBot(vk_token, user_id)
    photo = VK.get_photo(my_token)
    pprint(photo)