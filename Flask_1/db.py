import sqlite3
from datetime import datetime


def create_tables():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS temperatures (
                                date DATETIME,
                                value REAL)''')
    db.commit()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS levels (
                                    id INTEGER PRIMARY KEY,
                                    min REAL, 
                                    max REAL,
                                    heaterState INTEGER)''')
    db.commit()

    cursor.execute(f'''INSERT INTO levels(min, max, heaterState) VALUES(?, ?, ?)''', (1, 2, 0))

    db.commit()
    db.close()


def get_heater_state():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(f'''SELECT heaterState FROM levels WHERE id = 1''')
    result = cursor.fetchone()
    return result[0]


def set_heater_state(state):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(f'''UPDATE levels
                            SET heaterState = "{state}" WHERE id = 1''')
    db.commit()
    db.close()


def update_levels(*levels):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(f'''UPDATE levels
                        SET min = "{levels[0]}", max = "{levels[1]}" WHERE id = 1''')
    db.commit()
    db.close()


def insert_temperatures(value):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(f'''INSERT INTO temperatures(date, value) VALUES(?, ?)''', (datetime.now(), value))
    db.commit()
    db.close()


def get_limits():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(f'''SELECT min, max FROM levels WHERE id = 1''')
    result = cursor.fetchone()
    print(result)
    return result


def get_temperatures(number):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(f'''SELECT date, value FROM temperatures 
                       LIMIT "{number}" OFFSET (SELECT MAX(rowid) FROM temperatures) - "{number}"''')
    result = cursor.fetchall()
    return result


def clear_database():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(f'''DELETE FROM temperatures''')
    db.commit()
    db.close()


def delete_tables():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute(f'''DROP TABLE temperatures''')
    db.commit()
    cursor.execute(f'''DROP TABLE levels''')
    db.commit()
    db.close()


if __name__ == "__main__":
    delete_tables()
    create_tables()
    update_levels(24.2, 25.1)

