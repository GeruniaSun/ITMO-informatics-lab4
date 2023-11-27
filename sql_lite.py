import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"create_connection: The error '{e}' occurred")
    return connection


def execute_queries(connection, *queries):
    cursor = connection.cursor()
    try:
        for query in queries:
            cursor.execute(query)
            connection.commit()
        print("success!")
    except Error as e:
        print(f"execute_queries: The error '{e}' occurred")


def clearing(connection, tables):
    queries = ['DROP TABLE ' + table_name + ';' for table_name in tables]
    execute_queries(connection, *queries)


def execute_read_queries(connection, *queries):
    cursor = connection.cursor()
    result = []
    for query in queries:
        try:
            cursor.execute(query)
            result += cursor.fetchall()
        except Error as e:
            print(f"The error '{e}' occurred")
            return 'ERROR!'
    return result


def print_read_queries(connection, *queries):
    queries = execute_read_queries(connection, *queries)
    if queries == 'ERROR!':
        pass
    else:
        print('-' * 100)
        for query in queries:
            print(*query, sep=', ')
        print('-' * 100 + '\n')


# подключаемся к БД
my_connection = create_connection(r"C:\Users\brain\PycharmProjects\lab4\CROD_DB_sqlite")
my_tables = ['rooms', 'mentors', 'teachers', 'children']  # сделаем список названий будущих таблиц

# сотрем прошлую версию БД
print('Starts clearing...')
clearing(my_connection, my_tables)

# создаем таблицы
create_rooms_table = """
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campus TEXT NOT NULL,
    floor INTEGER,
    sign TEXT
);
"""
create_mentors_table = """
CREATE TABLE IF NOT EXISTS mentors (
    name TEXT PRIMARY KEY,
    squad INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms (id)
);
"""
create_teachers_table = """
CREATE TABLE IF NOT EXISTS teachers (
    name TEXT NOT NULL PRIMARY KEY,
    lesson TEXT NOT NULL,
    room_id INTEGER NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms (id)
);
"""
create_children_table = """
CREATE TABLE IF NOT EXISTS children (
    name TEXT NOT NULL PRIMARY KEY,
    squad INTEGER,
    age INTEGER,
    lesson_1 TEXT NOT NULL,
    lesson_2 TEXT NOT NULL,
    room_id INTEGER NOT NULL,
    FOREIGN KEY (squad) REFERENCES mentors (squad),
    FOREIGN KEY (lesson_1) REFERENCES teachers (lesson)
    FOREIGN KEY (lesson_2) REFERENCES teachers (lesson)
    FOREIGN KEY (room_id) REFERENCES rooms (id)
);
"""

print('Trying to create tables...')
execute_queries(my_connection, create_rooms_table, create_mentors_table,
                create_teachers_table, create_children_table)

# запишем данные в таблицы
create_rooms = """
INSERT INTO
    rooms (campus, floor, sign)
VALUES
    ('garnet', 1, '№2'),
    ('garnet', 1, '№4'),
    ('garnet', 1, 'laboratory'),
    ('garnet', 2, '№1'),
    ('garnet', 2, '№3'),
    ('garnet', 2, 'computer class'),
    ('azure', 1, "mentor's room"),
    ('azure', 1, '№1'),
    ('azure', 1, '№2'),
    ('pistachio', 2, "mentor's room"),
    ('pistachio', 2, '№1'),
    ('pistachio', 2, '№2'),
    ('administration', 2, "mentor's room"),
    ('administration', 2, '№1'),
    ('administration', 2, '№2');
"""
create_mentors = """
INSERT INTO
    mentors (name, squad, room_id)
VALUES
    ('Nikita Sergeevich', 1, 10),
    ('Polina Andreevna', 2, 10),
    ('Anastasia Genadievna', 3, 13),
    ('Arina Ruslanovna', 4, 7),
    ('Gerard Gerardovich', 5, 7);
"""
create_teachers = """
INSERT INTO
    teachers (name, lesson, room_id)
VALUES
    ('Sergey Alekseevich', 'handiwork', 1),
    ('Daniil Evgenievich', 'beading', 2),
    ('Roman Antonovich', 'chemical experiments', 3),
    ('Anna Alekseevna', 'art', 4),
    ('Gleb Sergeevich', 'physics with cats', 5),
    ('Anastasia Genadievna', 'english', 6);
"""
create_children = """
INSERT INTO
    children (name, squad, age, lesson_1, lesson_2, room_id)
VALUES
    ('Prohorov Nikita', 1, 11, 'english', 'chemical experiments', 11),
    ('Belousova Varvara', 2, 11, 'art', 'beading', 12),
    ('Puankare Savelii', 3, 10, 'chemical experiments', 'english', 15),
    ('Lapshin Kirill', 4, 9, 'handiwork', 'beading', 8),
    ('Mogilev Yan', 5, 7, 'chemical experiments', 'physics with cats', 9);
"""

print('Trying to insert data in tables...')
execute_queries(my_connection, create_rooms, create_mentors,
                create_teachers, create_children)

# серия SELECT запросов
# все записи всех таблиц
print('-' * 100 + '\nвсе записи всех таблиц:')
selecting_all = ['SELECT * FROM ' + table_name + ';' for table_name in my_tables]
print_read_queries(my_connection, *selecting_all)
# запрос с использованием JOIN
print('выведем для каждого ребенка его воспитателя:')
selecting_with_join = '''
SELECT
    children.name,
    children.age,
    mentors.name
FROM
    mentors
    INNER JOIN children ON children.squad = mentors.squad
'''
print_read_queries(my_connection, selecting_with_join)
# запрос с использованием WHERE и GROUP
print('посмотрим сколько воспитателей живет в каждой воспитательской')
selecting_with_group = '''
SELECT
    campus,
    sign,
    COUNT(mentors.room_id) as Rooms
FROM
    mentors,
    rooms
WHERE
    rooms.id = mentors.room_id
GROUP BY
    mentors.room_id
'''
print_read_queries(my_connection, selecting_with_group)
# запрос с вложенным SELECT запросом №1
print('выведем самых взрослых детей')
selecting_with_inner_select_first = '''
SELECT name
FROM children
WHERE age = (
    SELECT MAX(age) FROM children
);
'''
print_read_queries(my_connection, selecting_with_inner_select_first)
# запрос с вложенным SELECT запросом №2
print('предположим мы не знаем сколько у нас групп, выведем воспитателя группы со средним номером')
selecting_with_inner_select_second = '''
SELECT name, squad
FROM mentors
WHERE squad = (
    SELECT AVG(squad) FROM mentors
);
'''
print_read_queries(my_connection, selecting_with_inner_select_second)
# запрос с использованием UNION №1
print('выведем весь педсостав')
selecting_with_union_first = '''
SELECT name
FROM mentors
UNION
SELECT name
FROM teachers
'''
print_read_queries(my_connection, selecting_with_union_first)
# запрос с использованием UNION №2
print('узнаем кто где живет')
selecting_with_union_second = '''
SELECT name, room_id
FROM mentors
UNION
SELECT name, room_id
FROM teachers
UNION
SELECT name, room_id
FROM children
'''
print_read_queries(my_connection, selecting_with_union_second)
# запрос с использованием DISTINCT
print('посмотрим какие занятия посещают дети первыми')
selecting_with_distinct = '''
SELECT DISTINCT lesson_1
FROM children
'''
print_read_queries(my_connection, selecting_with_distinct)

# обновление записей
# №1
print('после нескольких дней смены\nзоркий глаз Герардаса Герардовича\n'
      'заметил опечатку на собственном бэйджике\nнадо изменить имя в базе\n')
print('текущее: ')
selecting_gergerich_name = '''
SELECT name
FROM mentors
WHERE name LIKE '%Gerardovich'
'''
print_read_queries(my_connection, selecting_gergerich_name)

updating_gergerich_name = '''
UPDATE mentors
SET name = 'Gerardas Gerardovich'
WHERE name = 'Gerard Gerardovich'
'''
print('отправляем запрос на изменение...')
execute_queries(my_connection, updating_gergerich_name)

print('\nубедимся что сработало:')
print_read_queries(my_connection, selecting_gergerich_name)
# №2
print('поздравляем Варю Белоусову с днём рождения!\n'
      'время изменить возраст в базе\n')
print('текущий: ')
selecting_varvara_age = '''
SELECT age
FROM children
WHERE name = 'Belousova Varvara'
'''
print_read_queries(my_connection, selecting_varvara_age)

updating_varvara_age = '''
UPDATE children
SET age = age + 1
WHERE name = 'Belousova Varvara'
'''
print('отправляем запрос на изменение...')
execute_queries(my_connection, updating_varvara_age)

print('\nубедимся что сработало:')
print_read_queries(my_connection, selecting_varvara_age)

# удаление записей
# №1
print('Яну не понравилось в центре\nи родители его забрали\nуберём его и из базы:\n')
print('отправляем запрос...')
execute_queries(my_connection, '''DELETE FROM children WHERE name = "Mogilev Yan"''')
print('\nубедимся что сработало:')
print_read_queries(my_connection, '''SELECT * FROM children''')
# №2
print('Арина Руслановна приболела\nей придётся покинуть центр\nа нам придётся убрать её из базы:')
print('отправляем запрос...')
execute_queries(my_connection, '''DELETE FROM mentors WHERE squad = 4''')
print('\nубедимся что сработало:')
print_read_queries(my_connection, '''SELECT * FROM mentors''')
# №3
print('Роман Антонович украл дорогое оборудование\nудаляем негодника:\n')
print('отправляем запрос...')
execute_queries(my_connection, '''DELETE FROM teachers WHERE lesson = "chemical experiments"''')
print('\nубедимся что сработало:')
print_read_queries(my_connection, '''SELECT * FROM teachers''')
# №4
print('лабораторию закрывают на ремонт после грабежа\nпридётся убрать её из списка:\n')
print('отправляем запрос...')
execute_queries(my_connection, '''DELETE FROM rooms WHERE sign = "laboratory"''')
print('\nубедимся что сработало:')
print_read_queries(my_connection, '''SELECT * FROM rooms''')

# удаление таблицы
print('7-ая смена объявляется закрытой!!!\nдети разъехались по домам\nпора очистить таблицу\n')
print('отправляем запрос...')
execute_queries(my_connection, '''DELETE FROM children''')
print('\nубедимся что сработало:')
print_read_queries(my_connection, '''SELECT * FROM children''')
