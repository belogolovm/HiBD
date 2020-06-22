import datetime
import random
import time

__names_male = [
    "Александр",
    "Алексей",
    "Андрей",
    "Артем",
    "Виктор",
    "Даниил",
    "Дмитрий",
    "Егор",
    "Илья",
    "Кирилл",
    "Максим",
    "Марк",
    "Михаил",
    "Роман",
    "Степан",
    "Тимофей",
    "Ярослав"
]

__names_female = [
    "Александра",
    "Алиса",
    "Анастасия",
    "Анна",
    "Арина",
    "Валерия",
    "Варвара",
    "Вероника",
    "Виктория",
    "Дарья",
    "Ева",
    "Екатерина",
    "Елизавета",
    "Кира",
    "Маргарита",
    "Мария",
    "Полина",
    "София",
    "Таисия",
    "Ульяна"
]

__surnames = [
    "Смирнов",
    "Иванов",
    "Кузнецов",
    "Соколов",
    "Попов",
    "Лебедев",
    "Козлов",
    "Новиков",
    "Морозов",
    "Петров",
    "Волков",
    "Соловьёв",
    "Васильев",
    "Зайцев",
    "Павлов",
    "Семёнов",
    "Голубев",
    "Виноградов",
    "Богданов",
    "Воробьёв",
    "Фёдоров",
    "Михайлов",
    "Беляев",
    "Тарасов",
    "Белов"
]

def generate_name():
    sex = random.randrange(2)
    if sex == 1:
        return random.choice(__surnames) + " " + random.choice(__names_male)
    else:
        return random.choice(__surnames) + "а " + random.choice(__names_female)


def generate_term():
    return random.randrange(8)


__universities = [
    'Университет ИТМО'
]


def generate_university():
    return random.choice(__universities)


def generate_hours():
    return random.randrange(100, 200)


__disciplines = [
    "Компьютерная графика (2018449043-И)",
    "Технологии веб-сервисов",
    "Системное и прикладное ПО",
    "Языки системного программирования",
    "Программирование",
    "Системы управления базами данных"
]


def generate_discipline():
    return random.choice(__disciplines)


__standards = [
    "новый",
    "старый"
]


def generate_standard():
    return random.choice(__standards)


__facultes = [
    "ФПИиКТ",
    "ФИТИП"
]


def generate_faculty():
    return random.choice(__facultes)


__specialty = [
    "09.01.02 – Магия вне Хогвартса",
    "01.02.03 – Тёмные искусства Дурмстранга"
]


def generate_specialty():
    return random.choice(__specialty)


def generate_position():
    return random.choice([
        "студент бакалавриата", "студент магистратуры", "доцент"
    ])


def generate_conference():
    return random.choice([
        "КМУ", "Майоровские чтения"
    ])


def generate_publication_type():
    return random.choice([
        "статья", "тезисы"
    ])


def generate_language():
    return random.choice([
        "русский", "Английский"
    ])


def generate_city():
    data = [
        "Москва", "Тверь", "Санкт-Петербург", "Челябинск"
    ]
    i = random.randrange(len(data))
    return i + 1, data[i]


def generate_country():
    data = [
        "Российская федерация"
    ]
    i = random.randrange(len(data))
    return i + 1, data[i]


def generate_street():
    data = [
        "Ленина ул.",
        "Советская ул.",
        "Революции пл.",
        "Энтузиастов ул.",
        "Сони Кривой ул.",
    ]
    i = random.randrange(len(data))
    return i + 1, data[i]


def generate_office():
    data = [
        "Пятёрочка",
        "Зингер",
        "Рога и Ко",
    ]
    i = random.randrange(len(data))
    return i + 1, data[i]


def generate_source_type():
    return random.choice([
        "ВАК", "РИНЦ"
    ])


def generate_group():
    return random.choice([
        "P3110",
        "P3210",
        "P3310",
        "P3410",
        "P4114",
        "P3111",
        "P3211",
        "P3311",
        "P3411",
        "P4116",
        "P41142",
    ])


def generate_qualification():
    return random.choice([
        "бакалавр", "магистр"
    ])


def generate_dormitory():
    street = random.choice([
        "Вяземский пер.",
        "Белорусская ул.",
        "Ленсовета ул.",
        "Альпийский п-к",
    ])
    building = random.randrange(200)
    return f'{street}, д.{building}'


def generate_is_exam():
    return random.randrange(2)


def generate_rating():
    letter = random.choice([
        'A', 'B', 'C', 'D', 'E', 'FX', 'F'
    ])
    if letter == 'A':
        number = 5
    elif letter == 'B' or letter == 'C':
        number = 4
    elif letter == 'D' or letter == 'E':
        number = 3
    else:
        number = 2
    return number, letter


def generate_person_id():
    return random.randrange(100000, 400000)


def generate_place():
    return random.choice([
        "Москва", "Санкт-Петербург", "Новосибирск", "Хабаровск", "Южно-Сахалинск", "Сочи"
    ])


def generate_study_type():
    return random.choice([
        "бюджет", "контракт"
    ])


def generate_school():
    return random.choice([
        "очная", "заочная", "вечерняя"
    ])


def generate_weekday():
    return random.randrange(14)


def generate_hour():
    return random.randrange(8, 19)


def generate_minute():
    return random.randrange(60)


def generate_room():
    return random.randrange(100, 4999)


def generate_publication_name():
    first = [
        "Солнечный",
        "Траурный",
        "Плюшевый",
        "Бешеный",
        "Памятный",
        "Базовый",
        "Ласковый",
        "Радужный",
        "Огненный",
        "Ламповый",
        "Пепельный",
        "Жареный",
        "Загнанный",
    ]
    second = [
        "зайчик",
        "глобус",
        "ветер",
        "пёсик",
        "щавель",
        "копчик",
        "егерь",
        "Игорь",
        "невод",
        "лобстер",
        "жемчуг",
        "кольщик",
        "йогурт",
    ]
    third = [
        "стеклянного",
        "ванильного",
        "резонного",
        "широкого",
        "дешевого",
        "горбатого",
        "собачьего",
        "волшебного",
        "исконного",
        "лохматого",
        "огромного",
        "едрённого",
    ]
    fourth = [
        "глаза",
        "плова",
        "дела",
        "жира",
        "мема",
        "сала",
        "фена",
        "зала",
        "рака",
        "бура",
    ]
    return "{} {} {} {}".format(
        random.choice(first),
        random.choice(second),
        random.choice(third),
        random.choice(fourth),
    )


def generate_pages():
    return random.randrange(50)


def generate_quote_index():
    return random.uniform(0, 100)


def generate_project_name():
    return "Проект #" + str(random.randrange(5000))


def generate_book_name():
    return "Книга #" + str(random.randrange(5000))


def generate_bool():
    return True if random.randrange(2) == 1 else False


def generate_warnings():
    return random.randrange(10)


def generate_max_person():
    return random.randrange(4)


def random_time(start, size):
    return start + random.randrange(size)


def generate_date():
    return datetime.datetime.fromtimestamp(random_time(1567296000, 23673600))

def generate_birthdate():
    return datetime.datetime.fromtimestamp(random_time(631152000, 915148800-631152000))