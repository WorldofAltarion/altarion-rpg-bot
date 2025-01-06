import sqlite3

# Функция для создания таблиц в базе данных
def create_tables():
    connection = sqlite3.connect('altarion_bot.db')
    cursor = connection.cursor()

    # Создание таблицы пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        side TEXT,
        hero TEXT,
        energy INTEGER DEFAULT 3,
        last_energy_update TEXT
    )
    ''')

    connection.commit()
    connection.close()

# Функция для добавления или обновления пользователя в базе данных
def add_user(user_id, username, side=None, hero=None):
    connection = sqlite3.connect('altarion_bot.db')
    cursor = connection.cursor()

    # Проверка, существует ли пользователь в базе данных
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        # Обновляем данные пользователя
        cursor.execute('''
        UPDATE users
        SET username = ?, side = ?, hero = ?
        WHERE user_id = ?
        ''', (username, side, hero, user_id))
    else:
        # Добавляем нового пользователя
        cursor.execute('''
        INSERT INTO users (user_id, username, side, hero)
        VALUES (?, ?, ?, ?)
        ''', (user_id, username, side, hero))

    connection.commit()
    connection.close()

# Функция для получения информации о пользователе
def get_user(user_id):
    connection = sqlite3.connect('altarion_bot.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    connection.close()
    return user

# Функция для обновления энергии
from datetime import datetime, timedelta

def update_energy(user_id):
    connection = sqlite3.connect('altarion_bot.db')
    cursor = connection.cursor()

    # Получаем данные пользователя
    cursor.execute('SELECT energy, last_energy_update FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        current_energy, last_update = user
        max_energy = 3
        recovery_time = 2  # Время восстановления одной энергии (в часах)

        # Если last_energy_update пуст, устанавливаем текущее время
        if not last_update:
            last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                'UPDATE users SET last_energy_update = ? WHERE user_id = ?',
                (last_update, user_id)
            )
            connection.commit()
            connection.close()
            return current_energy

        # Вычисляем восстановленную энергию
        last_update_time = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        time_diff = now - last_update_time
        recovered_energy = time_diff.total_seconds() // (recovery_time * 3600)

        if recovered_energy > 0:
            new_energy = min(current_energy + int(recovered_energy), max_energy)
            new_last_update = (last_update_time + timedelta(hours=recovered_energy * recovery_time)).strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute(
                'UPDATE users SET energy = ?, last_energy_update = ? WHERE user_id = ?',
                (new_energy, new_last_update, user_id)
            )
            connection.commit()

    connection.close()
    return current_energy
