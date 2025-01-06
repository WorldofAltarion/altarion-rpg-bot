import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from db_handler import create_tables, add_user, get_user, update_energy

# Создаем таблицы при старте
create_tables()

# Получаем токен из переменной окружения
API_TOKEN = os.environ['MY_BOT_TOKEN']
bot = telebot.TeleBot(API_TOKEN)

# Описания героев
hero_descriptions = {
    "Talorn the Swordsman": "A brave swordsman with basic combat skills.\nStrength: 6\nDefense: 5\nSpeed: 4",
    "Ellina the Mage": "An apprentice mage with basic magical abilities.\nMagic: 7\nIntelligence: 6\nDefense: 3",
    "Garron the Archer": "A skilled hunter and tracker from the forests.\nDexterity: 5\nAccuracy: 4\nStealth: 4",
    "Bone Titan": "A massive creature made of bones, slow but powerful.\nStrength: 6\nDefense: 5\nSpeed: 2",
    "Phantom Witch": "A novice in the dark arts, master of illusions.\nMagic: 5\nStealth: 5\nSpeed: 3",
    "Dark Destroyer": "A creature of darkness with deadly claws.\nStrength: 5\nDefense: 4\nSpeed: 3",
}

# Описания монстров
monster_descriptions = {
    "Grogg the Slug Beast": "A massive, slimy creature with toxic slime attacks.\nHealth: 40\nAttack: 5\nDefense: 3\nSpeed: 2",
    "Glimmer the Fire Wisp": "A small, fiery creature that's hard to hit.\nHealth: 30\nAttack: 4\nDefense: 2\nSpeed: 6",
    "Shadow Claw": "A beast made of dark smoke and claws.\nHealth: 35\nAttack: 4\nDefense: 3\nSpeed: 4",
    "Rotten Wraith": "A decaying specter that weakens enemies' resolve.\nHealth: 40\nAttack: 4\nDefense: 3\nSpeed: 5",
    "Cinder Beast": "A creature of ash and embers with fire-based attacks.\nHealth: 30\nAttack: 6\nDefense: 5\nSpeed: 4",
    "Corrupt Guardian": "A stone golem twisted by dark magic.\nHealth: 35\nAttack: 7\nDefense: 8\nSpeed: 3",
}

# Главное меню /start
@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.chat.id
    current_energy = update_energy(user_id)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Enter Game"), KeyboardButton("Help"))

    bot.send_message(
        message.chat.id,
        f"Welcome to the RPG game Altarion!\nYour current energy: {current_energy}/3\nUse the buttons below to start:",
        reply_markup=markup
    )

# Кнопка "Help"
@bot.message_handler(func=lambda message: message.text == "Help")
def show_help(message):
    bot.send_message(
        message.chat.id,
        "Instructions:\n- Click 'Enter Game' to start your journey.\n- Choose a side (Light or Darkness).\n- Select a hero and confirm your choice.\n- Face powerful monsters and defeat them!"
    )

# Кнопка "Enter Game"
@bot.message_handler(func=lambda message: message.text == "Enter Game")
def enter_game(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Light"), KeyboardButton("Darkness"))

    bot.send_message(
        message.chat.id,
        "Choose your path: Light or Darkness.",
        reply_markup=markup
    )

# Остальной код (выбор стороны, героев, монстров) аналогичен предыдущему примеру.
