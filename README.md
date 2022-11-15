## Чат-бот VKinder

### Для начала работы необходимо установить настроить БД:
* Необходимо установить создать БД PostgreSQL
* Обязательно создать схему под наименованием "public", если ее нет
* Внести название БД, имя пользователя и пароль в файл [postgres_db.py](postgres_db.py)
* После чего запускаем скрипт [postgres_db.py](postgres_db.py)
* Не забываем проверить, что таблицы создались и таблица "Mark" заполнилась двумя строками

### После установки схемы таблиц
* Вставить токен группы (token_vk_group_bot) и токен сообщества (token_vk_app) в файл [token_file.py](Modul/token_file.py)
* После чего запускаем основной скрипт [main.py](main.py)
