import sqlite3
import random
import datetime as dt

# Словарь кафедр и базирующихся на них
# направлениями подготовки с набором ЕГЭ
departments = {
    'Кафедра общей физики': ['Ф М РЯ',
                             ['Радиотехника',
                              'Прикладная механика',
                              'Фотоника', 'Молекулярная физика']],
    'Кафедра перспективных материалов': ['Ф М РЯ',
                                         ['Материаловедение',
                                          'Технологии нанолитографии']],
    'Кафедра высшей математики': ['ИКТ М Ф РЯ',
                                  ['Прикладная математика',
                                   'Математическое моделирование',
                                   'Науки о данных']],
    'Кафедра системной и программной инженерии': ['ИКТ М РЯ',
                                                  ['Программная инженерия',
                                                   'Прикладная информатика',
                                                   'Фундаментальная информатика',
                                                   'Инфокуммуникационные системы',
                                                   'Вычислительная механика и кибернетика']],
    'Кафедра органической химии': ['Х М РЯ',
                                   ['Медицинская химимя',
                                    'Органические и гибридные материалы',
                                    'Химическая кинетика']],
    'Кафедра биомедицинских систем': ['Ф Б М РЯ',
                                      ['Консруирование биомедицинских систем']],
    'Кафедра электроники и микросистем': ['Ф М РЯ',
                                          ['Электроника и наноэлектроника',
                                           'Проектирование интегральных микросхем']],
    'Кафедра графики и дизайна': ['Творческий конкурс',
                                  ['Промышленный дизайн', 'Графический дизайн',
                                   'Дизайн ландшафтов']],
    'Кафедра маркетинга и управления проектами': ['О РЯ',
                                                  ['Реклама', 'Менеджмент',
                                                   'Управление процессами']],
    'Кафедра гуманитарных наук': ['РЯ ИЯ О', ['Филология', 'Лигвистика',
                                  'Социология', 'Политология']],
}

# Словарь должностей
positions = {
    'Профессор': [100000, 40],
    'Доцент': [60000, 32],
    'Лаборант': [40000, 36],
}

connection = sqlite3.connect('departments.db')
db_cursor = connection.cursor()
db_cursor.execute("""CREATE TABLE IF NOT EXIST departments(
         dep_ID INTEGER PRIMARY KEY AUTOINCREMENT,
         Dep_name TEXT NOT NULL,
         Num_of_fac INTEGER,
         Dec TEXT NOT NULL,
         Rating REAL NOT NULL,
         Num_of_emp INTEGER NOT NULL);
""")
connection.commit()
db_cursor.execute("""CREATE TABLE IF NOT EXIST faculties(
         fac_ID INTEGER PRIMARY KEY AUTOINCREMENT,
         Fac_name TEXT NOT NULL,
         USE TEXT NOT NULL,
         Min_score INTEGER NOT NULL,
         dep_ID INTEGER,
         FOREIGN KEY(dep_ID) REFERENCES departments(dep_ID)); 
""")
connection.commit()
db_cursor.execute("""CREATE TABLE IF NOT EXIST employees(
         Pos_name TEXT PRIMARY KEY,
         Salary INTEGER NOT NULL,
         Work_h INTEGER NOT NULL);
""")
connection.commit()
db_cursor.execute("""CREATE TABLE IF NOT EXIST employees(
         ID_emp INTEGER PRIMARY KEY AUTOINCREMENT,
         dep_ID INTEGER,
         Name TEXT NOT NULL,
         Position TEXT,
         Rate REAL NOT NULL,
         Birth_date DATE NOT NULL,
         Salary INTEGER NOT NULL,
         FOREIGN KEY(dep_ID) REFERENCES departments(dep_ID),
         FOREIGN KEY(Position) REFERENCES positions(Pos_name));
""")
connection.commit()
db_cursor.execute("""CREATE TABLE IF NOT EXIST kids(
         Name TEXT NOT NULL,
         ID_emp INTEGER,
         Age INTEGER NOT NULL
         FOREIGN KEY(ID_emp) REFERENCES employees(ID_emp));
""")
connection.commit()