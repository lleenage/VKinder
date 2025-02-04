import requests
import json

class VkBot:
    def __init__(self, user_id, token, version="5.131"):
        self.user_id = user_id
        self.username = self.get_user_name(user_id)
        self.token = token
        self.version = version
        self.base_url = "https://api.vk.com/method/"
        self.params = {"access_token": self.token, "v": self.version}
        self.commands = ["ПРИВЕТ", "ПОКА"]

    #метод для получения возраста, пола, города пользователя
    def get_info(self):
        pass

    #метод получения имени пользователя
    def get_user_name(self, user_id):
        pass

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
            return f"Привет, {self.username}!"

        elif message.upper() == self.commands[3]:
            return f"До встречи, {self.username}!"

        else:
            return "Я пока не знаю такой команды. 😞"