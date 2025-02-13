### Получение токена (ключ доступа сообщества)
* Создаем группу в Вконтакте.
* Управление => Работа с API. Создать ключ.
* "Показать". Копируем токен и готово.

### Получение токена (ключ доступа пользователя)
* Переходим по [ссылке](https://id.vk.com/auth?app_id=51649761&device_id=&response_type=code&redirect_uri=https%3A%2F%2Fid.vk.com%2Fabout%2Fbusiness%2Fgo&scope=email&lang_id=0&scheme=bright_light&oauth_version=2&redirect_state=6a96610f-67dc-4ca7-bba3-b8069e3c9230&code_challenge=R05vsT88YnRv6S6YYGUXcIXPU1dEd8X4QUgr9QgbHo4&code_challenge_method=sha256)
 => «Добавить приложение». 
* Вводим название приложения и выберите тип платформы — Web => «Далее»
* В поле «Базовый домен» и «Доверенный Redirect URL» вставляем [ссылку](https://example.com/callback)
* В [ссылке](https://oauth.vk.com/authorize?client_id=1&display=page&redirect_uri=http://example.com/callback&scope=friends&response_type=token&v=5.131&state=123456) 
 в значение "client_id" изменяем параметр на «ID приложения» (только цифры без букв) 
 из поля «Информация о приложении» и добавляем к "http" "s"
  (результат "https") => «Enter»
* В окне «Вход с помощью VK ID» нажимаем «Продолжить как ***»
* Из ссылки копируем "access_token"(от "access_token=" до "&expires_in").
* #### Важно понимать,что этот токен не живет больше суток.