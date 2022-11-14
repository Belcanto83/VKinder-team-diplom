from Modul.vk_api_func import ApiFunction
from postgres_db import VKinderPostgresqlDB
from database_pg.models import User, UserMark, Mark
from sqlalchemy.exc import OperationalError, IntegrityError
# from main import marked_user_id

"""Работа с пользовательской частью бота, непосредственно с интерфейсом и механикой бота. 
В классе BotFunction прописаны функции обрабатывающие входные данные от пользователя"""


class BotFunction:
    def __init__(self, vk_user_id=None, city=None, sex=None, age_from=None, age_to=None, uid_db=None):
        self.dataset = None
        self.datas = None
        self.city = city
        self.sex = sex
        self.age_from = age_from
        self.age_to = age_to
        # self.favorite_list = []
        # self.black_list = []
        self.vk_user_id = vk_user_id
        self.insert_user()

    def insert_user(self):
        try:
            VKinder_DB = VKinderPostgresqlDB()
            session = VKinder_DB.new_session()
            with session:
                try:
                    VKinder_DB.add_row(session=session, model=User, data={'user_id': self.vk_user_id})
                    session.commit()
                except IntegrityError:
                    session.rollback()
        except OperationalError as err:
            print('Ошибка подключения к БД:', err)

    def user_search_data(self):
        """Обработка запроса на поиск профилей по соответсвующим критериям пользователя.
        Результат: 1. ИО профиля, ссылка на профиль,
        2. фотографии через запятую в формате: <photo><owner_id>_<id>(для удобного просмотра в интерфейсе пользователя)
        Перед этим переопределяет 'data' и 'dataset' для последующей обработки.
        Объект data является последним запрошенный пользователь
        Объект dataset весь запрошенный список """

        sex_key = {"мужской": 2, "женский": 1, "любой": 0}
        vk_search_user = ApiFunction(city=self.city, sex=sex_key[self.sex], age_from=self.age_from,
                                     age_to=self.age_to)
        self.datas = iter(vk_search_user.users_search())
        self.dataset = next(self.datas)
        vk_upload_photo = ApiFunction(users_id=f"{self.dataset['user_id']}")
        users_photo = vk_upload_photo.get_photos()
        photos = ''
        for photo in users_photo:
            photos += photo["attachment"] + ','
        user_name_and_link = f"{self.dataset['profile_name']}\n {self.dataset['link']}"
        return user_name_and_link, photos

    def next_profile(self):
        """Выводит следующего по списку dataset пользователя.
        Формат вывода равноценен 'user_search_data()'.
         Переопределяет пользователя в переменной data"""
        self.dataset = next(self.datas)

        vk_upload_photo = ApiFunction(users_id=f"{self.dataset['user_id']}")
        users_photo = vk_upload_photo.get_photos()
        photos = ''
        for photo in users_photo:
            photos += photo["attachment"] + ','
        user_name_and_link = f"{self.dataset['user_id']}\n{self.dataset['profile_name']}\n {self.dataset['link']}"
        return user_name_and_link, photos, self.dataset['user_id']

    def add_to_favorites_lists(self, marked_user):
        """Добавляет в 'список избранных' профиль из переменной data
        (Последний профиль, который был выведен для пользователя в интерфейсе).
        Корректно обрабатывает выходные данные если пользователь уже добавлял профиль в список"""
        try:
            VKinder_DB = VKinderPostgresqlDB()
            session = VKinder_DB.new_session()
            with session:
                try:
                    value = session.query(UserMark).filter(UserMark.user_id == self.vk_user_id, UserMark.marked_user_id == marked_user, UserMark.mark_id == 1).all()
                    if len(value) == 0:
                            session.add(UserMark(
                                user_id = self.vk_user_id, 
                                marked_user_id = marked_user, 
                                mark_id = 1
                            ))
                            session.commit()
                            text = f"Профиль '{self.dataset['profile_name']}' добавлен в избранное"
                    else:
                        text = f"Профиль '{self.dataset['profile_name']}' уже находится в избранном" 
                except IntegrityError:
                    session.rollback()
        except OperationalError as err:
            print('Ошибка подключения к БД:', err)
        return text

        # if self.dataset not in self.favorite_list:
        #     self.favorite_list.append(self.dataset)
        #     text = f"Профиль '{self.dataset['profile_name']}' добавлен в избранное"
        # else:
        #     text = f"Профиль '{self.dataset['profile_name']}' уже был в избранном"
        # return text

    def show_favorites_list(self):
        """Выводит информацию о добавленных в 'избранный список' профилях
        Формат: <ИО><ссылка на профиль>"""
        list_favorite = []
        try:
            VKinder_DB = VKinderPostgresqlDB()
            session = VKinder_DB.new_session()
            with session:
                try:
                    value = session.query(UserMark).filter(UserMark.user_id == self.vk_user_id, UserMark.mark_id == 1).all()
                    for id in value:
                        list_favorite.append(f'https://vk.com/id{id.marked_user_id}')
                    # text = ''.join(f'https://vk.com/id{id.marked_user_id}')
                    text = '\n'.join(list_favorite)
                    print(text)
                except IntegrityError:
                    session.rollback()
        except OperationalError as err:
            print('Ошибка подключения к БД:', err)
        return text


        # count = 0
        # text = ""
        # if len(self.favorite_list)>0:
        #     for user in self.favorite_list:
        #         count += 1
        #         text += f"{count}: {user['profile_name']} ссылка: {user['link']}\n"
        # else:
        #     text = "Список избранных пока пуст"
        # return text

    def add_to_black_list(self, marked_user):
        """добавляет последний профиль в 'черный список'
        в дальнейшем этот профиль будет отсортирован и не попадаться для пользователя в поиске профилей"""
        try:
            VKinder_DB = VKinderPostgresqlDB()
            session = VKinder_DB.new_session()
            with session:
                try:
                    value = session.query(UserMark).filter(UserMark.user_id == self.vk_user_id, UserMark.marked_user_id == marked_user, UserMark.mark_id == 0).all()
                    if len(value) == 0:
                            session.add(UserMark(
                                user_id = self.vk_user_id, 
                                marked_user_id = marked_user, 
                                mark_id = 1
                            ))
                            session.commit()
                            text = f"Профиль '{self.dataset['profile_name']}' добавлен в черный список"
                    else:
                        text = f"Профиль '{self.dataset['profile_name']}' уже находится в черном писке" 
                except IntegrityError:
                    session.rollback()
        except OperationalError as err:
            print('Ошибка подключения к БД:', err)
        return text
        # self.black_list.append(self.dataset)
        # text = f"Профиль {self.dataset['profile_name']} больше не отобразится"
        # return text
