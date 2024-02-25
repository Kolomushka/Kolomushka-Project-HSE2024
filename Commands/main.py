import telebot
import sys
import os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from Commands.StartCommand import StartCommand
from Commands.HelpCommand import HelpCommand
from Commands.InfoCommand import InfoCommand
from Commands.StartDialogCommand import StartDialogCommand

bot = telebot.TeleBot('6705246337:AAGhgopMsf80iVJLYTuYX5oVSOxs6UFbpyc')

# Создаем объекты для каждой команды
start_command = StartCommand(bot)
help_command = HelpCommand(bot)
info_command = InfoCommand(bot)
start_dialog_command = StartDialogCommand(bot)

try:
    # Регистрируем обработчики команд
    bot.message_handler(commands=start_command.get_command_names())(start_command.handle)
    bot.message_handler(commands=help_command.get_command_names())(help_command.handle)
    bot.message_handler(commands=info_command.get_command_names())(info_command.handle)
    bot.message_handler(commands=start_dialog_command.get_command_names())(start_dialog_command.handle)
except Exception as e:
    print("Произошла ошибка при регистрации обработчика команды: {e}")

try:
    # Запускаем бота
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Произошла ошибка при запуске бота: {e}")