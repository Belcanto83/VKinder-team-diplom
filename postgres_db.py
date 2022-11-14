import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from database_pg.models import Base, Mark

"""" В этом модуле описан класс созданию таблиц и подключение к БД
    Внимание! Для создание БД необходимо запустить этот скрипт 
    Для успеха при создании БД нужно создать схему 'public' """


class VKinderPostgresqlDB:
    """Wrapper class for VKinder postgres database"""

    def __init__(self):
        self.db_name = 'postgres' #db_name
        self.db_user = 'postgres' #credentials.get('user')
        self.db_pass = 'postgres' #credentials.get('pass')
        self._engine = self.create_db_engine()
        self.create_tables()
        self.class_session = sessionmaker(bind=self._engine)

    def create_db_engine(self, host='localhost', port=5432):
        DSN = f'postgresql://{self.db_user}:{self.db_pass}@{host}:{port}/{self.db_name}'
        engine = sa.create_engine(DSN)
        return engine

    def create_tables(self):
        Base.metadata.create_all(self._engine)

    def drop_database(self):
        Base.metadata.drop_all(self._engine)

    # def new_session(self):
    #     session = self.class_session()
    #     return session

    def new_session(self):
        session = self.class_session()
        return session

    @staticmethod
    def add_row(session, model, data):
        row = model(**data)
        session.add(row)
        return session


def insert_mark():
    num_0 = Mark(
        mark_id = 0,
        name = 'black list'
    )
    num_1 = Mark(
        mark_id = 1,
        name = 'favorite list'
    )
    session = tab.new_session() # Создаем ссесию
    session.add_all([num_0, num_1]) # Добавляем флаги
    session.commit()




if __name__ == "__main__":
    tab = VKinderPostgresqlDB() # Создать БД
    insert_mark() # Создадим флаги black и favorite листа для таблицы UserMark

    # VKinderPostgresqlDB.drop_database(tab) # Если надо - дропнуть