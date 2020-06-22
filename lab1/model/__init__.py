from mongoengine import get_db
from sqlalchemy import create_engine
from configparser import ConfigParser
import mongoengine
from sqlalchemy.ext.declarative import declarative_base

databases = {}
Base = declarative_base()


def init_sql_engines():
    config = ConfigParser()
    config.read('db.cfg')

    for s in config.sections():
        try:
            proto = config[s]['proto']
            url = config[s]['url']
            username = config[s]['username']
            password = config[s]['password']
        except KeyError:
            continue

        databases[s] = {
            'engine': create_engine(
                f'{proto}://{username}:{password}@{url}',
                encoding='UTF-8'
            )
        }

        # print(f'Подключение к {s} инициализировано')


def init_mongo_engine():
    config = ConfigParser()
    config.read('db.cfg')

    section = 'mongo'

    if not section in config.sections():
        return
    try:
        url = config[section]['url']
        username = config[section]['username']
        password = config[section]['password']
    except KeyError:
        return

    mongoengine.connect(
        host=f'mongodb://{username}:{password}@{url}'
    )


    # print(f'Подключение к {section} инициалзировано')


def __check_sql_helloworld(engine, statement):
    data = databases[engine]['engine'].execute(statement).scalar()
    if data == "Hello, World!":
        return f'{engine}: OK'
    return f'{engine}: FAIL'


def check_connection():
    print(__check_sql_helloworld('oracle', "select 'Hello, World!' from dual"))
    print(__check_sql_helloworld('postgres', "select 'Hello, World!'"))
    print(__check_sql_helloworld('mysql', "select 'Hello, World!'"))

    try:
        class test(mongoengine.Document):
            id = mongoengine.StringField()

        test.objects()
        print('mongo: OK')
    except:
        print('mongo: FAIL')