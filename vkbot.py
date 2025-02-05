import requests
import json
from datetime import date


class VkBot:
    def __init__(self, vk_token, user_id, version="5.131"):
        self.user_id = user_id
        self.base_url = 'https://api.vk.com/method/'
        self.token = vk_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

        self.commands = ["ПРИВЕТ", "ПОКА", "МОЙ ГОРОД", "МОЙ ПОЛ"]

    #методы для получения родного города пользователя и города, в котором живет пользователь
    def get_home_town(self):
        url = self.base_url + 'users.get?'
        param = {
            **self.params,
            'user_ids': self.user_id,
            'fields': 'home_town'
        }
        response = requests.get(url, params=param)
        try:
            users_town = response.json()['response'][0]['home_town']
            return users_town
        except:
            return 'Родной город не указан'

    def get_city(self):
        url = self.base_url + 'users.get?'
        param = {
            **self.params,
            'user_ids': self.user_id,
            'fields': 'city'
        }
        response = requests.get(url, params=param)
        try:
            users_city = response.json()['response'][0]['title']
            return users_city
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
    # get_name()[0] - имя
    # get_name()[1] - фамилия
    # )
    def get_name(self):
        url = self.base_url + 'users.get?'
        param = {
            **self.params,
            'user_ids': self.user_id,
            'fields': 'about'

        }
        response = requests.get(url, params=param)
        self.user_first_name = response.json()['response'][0]['first_name']
        self.user_last_name = response.json()['response'][0]['last_name']

        return self.user_first_name, self.user_last_name

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

    #метод получения 3 фотографий с наибольшим количеством лайков
    def get_photo(self, user_id, count=3):
        pass

    #метод получения предпочтений пользователя и добавление фаворита в бд
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
            return f"Привет, {self.get_name()[0]}!"

        elif message.upper() == self.commands[1]:
            return f"До встречи, {self.get_name()[0]}!"
        #проверяю на работоспособность получение города пользователя
        elif message.upper() == self.commands[2]:
            town = [self.get_home_town(),  self.get_city()]
            return town
        #проверка медотода получения гендера
        elif message.upper() == self.commands[3]:
            return self.get_sex()
        else:
            return "Я пока не знаю такой команды. 😞"