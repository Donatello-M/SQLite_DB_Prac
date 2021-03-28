import sqlite3
import random
import datetime as dt
import names

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
    'Профессор': 100000,
    'Доцент': 60000,
    'Лаборант': 40000,
}

# Запросы на создание таблиц
connection = sqlite3.connect('departments.db')
db_cursor = connection.cursor()
db_cursor.execute("""CREATE TABLE IF NOT EXISTS departments(
         dep_ID INTEGER PRIMARY KEY AUTOINCREMENT,
         Dep_name TEXT NOT NULL,
         Num_of_fac INTEGER,
         Dec TEXT NOT NULL,
         Rating REAL NOT NULL,
         Num_of_emp INTEGER NOT NULL DEFAULT 0);
""")
connection.commit()

db_cursor.execute("""CREATE TABLE IF NOT EXISTS faculties(
         fac_ID INTEGER PRIMARY KEY AUTOINCREMENT,
         Fac_name TEXT NOT NULL,
         USE TEXT NOT NULL,
         Min_score INTEGER NOT NULL,
         dep_ID INTEGER,
         FOREIGN KEY (dep_ID) REFERENCES departments(dep_ID)); 
""")
connection.commit()

db_cursor.execute("""CREATE TABLE IF NOT EXISTS employees(
         ID_emp INTEGER PRIMARY KEY AUTOINCREMENT,
         dep_ID INTEGER,
         Name TEXT NOT NULL,
         Position TEXT,
         Rate REAL NOT NULL,
         Birth_date DATE NOT NULL,
         Salary REAL,
         FOREIGN KEY (dep_ID) REFERENCES departments(dep_ID),
         FOREIGN KEY (Position) REFERENCES positions(Pos_name));
""")
connection.commit()

db_cursor.execute("""CREATE TABLE IF NOT EXISTS kids(
         Name TEXT NOT NULL,
         ID_emp INTEGER,
         Age INTEGER NOT NULL,
         FOREIGN KEY (ID_emp) REFERENCES employees(ID_emp));
""")
connection.commit()

print('таблицы созданы')

dep_list = []
fac_list = []
id_dep = 1
for rec in list(departments.keys()):
    print(rec)
    dec_name = names.get_full_name()
    num_fac = len(departments[rec][1])
    print(id_dep)
    rating = round(random.uniform(1, 5), 2)
    id_dep += 1
    for i in range(len(departments[rec][1])):
        fac_name = departments[rec][1][i]
        use = departments[rec][0]
        min_score = random.randint(150, 300)
        tup_fac = (fac_name, use, min_score, id_dep)
        fac_list.append(tup_fac)
    tup_dep = (rec, num_fac, dec_name, rating)
    dep_list.append(tup_dep)

db_cursor.executemany("INSERT INTO departments(Dep_name, "
                      "Num_of_fac, Dec, Rating) VALUES(?, ?, ?, ?)", dep_list)
connection.commit()
db_cursor.executemany("INSERT INTO faculties(Fac_name, "
                      "USE, Min_score, dep_ID) VALUES(?, ?, ?, ?)", fac_list)
connection.commit()

print('dep and fac is ready')

emp_list = []
start_date = dt.date(year=1955, month=1, day=1).toordinal()
end_date = dt.date(year=1981, month=12, day=31).toordinal()
for i in range(100):
    dep_id = random.randint(1, 10)
    name = names.get_full_name()
    position = random.choice(list(positions.keys()))
    rate = round(random.uniform(0.5, 3), 2)
    birth_date = dt.date.fromordinal(random.randint(start_date, end_date))
    salary = round(positions[position] * rate, 2)
    tup = (dep_id, name, position, rate, birth_date, salary)
    emp_list.append(tup)

db_cursor.executemany("INSERT INTO employees(dep_ID, "
                      "Name, Position, Rate, Birth_date, Salary) VALUES(?, ?, ?, ?, ?, ?)", emp_list)
connection.commit()
print('emp is ready')

kids_list = []
for i in range(150):
    name = names.get_full_name()
    id_emp = random.randint(1, 100)
    age = random.randint(5, 23)
    tup = (name, id_emp, age)
    kids_list.append(tup)

db_cursor.executemany("INSERT INTO kids(Name, "
                      "ID_emp, Age) VALUES(?, ?, ?)", kids_list)
connection.commit()
print('kids are ready')

db_cursor.execute("""UPDATE departments 
        SET Num_of_emp = (SELECT COUNT(Name) FROM employees
        WHERE departments.dep_ID=employees.dep_ID)
        WHERE EXISTS (SELECT * FROM employees
        WHERE departments.dep_ID=employees.dep_ID)
""")
connection.commit()

db_cursor.execute("SELECT * FROM departments")
print(db_cursor.fetchall())
db_cursor.execute("SELECT * FROM faculties")
print(db_cursor.fetchall())
db_cursor.execute("SELECT * FROM employees")
print(db_cursor.fetchall())
db_cursor.execute("SELECT * FROM kids")
print(db_cursor.fetchall())

db_cursor.execute("DROP TABLE IF EXISTS departments;")
connection.commit()
db_cursor.execute("DROP TABLE IF EXISTS faculties;")
connection.commit()
db_cursor.execute("DROP TABLE IF EXISTS employees;")
connection.commit()
db_cursor.execute("DROP TABLE IF EXISTS kids;")
connection.commit()
