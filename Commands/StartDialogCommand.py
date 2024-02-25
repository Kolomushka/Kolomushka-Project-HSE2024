import sys
import os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from DataBase.UserBase import UserDB
from Commands.CommandTg import CommandTg
from Commands.GlobalData import GlobalData
from Dialog.WordAction import WordAction
from telebot import types
import random

class StartDialogCommand(CommandTg):

    gd = GlobalData()
    wd = WordAction()

    def handle(self, message):
        self.bot.send_message(message.chat.id, 'Отлично! Присутупим.')
        self.user_db = UserDB(message.chat.id) # Делаем запись в бд с chat_id
        self.theme_query(message)

    # Запрос тем
    def theme_query(self, message): 
        self.keyboard_setup(message, GlobalData.theme_dict)

    def handle_button(self, message, theme):
        try:
            self.bot.send_message(message.chat.id, f"Вы выбрали тему: {theme}")
            self.user_db.set_theme(theme, message.chat.id)
            self.user_dialog(message, 1)
        except Exception as e:
            print(f"Произошла ошибка, при theme = {theme}: {e}")

    def keyboard_setup(self, message, theme_dict):
        
        # Создаем объект клавиатуры
        markup = types.InlineKeyboardMarkup()
        for el in theme_dict.values():
            button = types.InlineKeyboardButton(el, callback_data=el)
            markup.add(button)

        self.bot.send_message(message.chat.id, text="Выберите тему:", reply_markup=markup)     

        @self.bot.callback_query_handler(func=lambda callback: True)
        def callback_message(callback): 
            for theme in GlobalData.theme_dict.values():
                if theme == callback.data:                
                    self.handle_button(message, callback.data) 
                
            for i in range(50):
                if callback.data == f'True{i+1}':
                    self.bot.send_message(message.chat.id, 'Correctly! ✅')
                    self.user_dialog(message, i+3)
                elif callback.data == f'False{i+1}':
                    self.bot.send_message(message.chat.id, 'Please try again 😭')
                    self.user_dialog(message, i+1)

    def set_theme(self, theme, message):
        self.user_db.set_theme(theme, message.chat.id)

    def set_iter(self, iter, message):
        self.user_db.set_iter(iter, message.chat.id)

    def set_line(self, line, message):
        self.user_db.set_line(line, message.chat.id)

    def get_theme(self, message):
        return self.user_db.get_theme(message.chat.id)
    
    def get_iter(self, message):
        return self.user_db.get_iter(message.chat.id)

    def get_line(self, message):
        return self.user_db.get_line(message.chat.id)

    def get_command_names(self):
        return ['start_dialog']
    
    def user_dialog(self, message, iter):
        try:
            if iter == 1:
                number_line = self.wd.find_random_line_number_by_value(self.gd.theme_to_num(self.get_theme(message)))
                self.set_line(number_line, message)
                self.set_iter(100, message)

            self.dialog_keyboard(message, iter)
            print("question", iter)

        except Exception as e:
            print(f"Произошла ошибка в user_dialog: {e}")

    def dialog_keyboard(self, message, iter):
        if iter <= self.get_iter(message):
            try:
                text_line = self.get_line(message)
                line = self.wd.read_data_by_line_number(text_line)
                replies = line.split("__eou__")

                if iter == 1:
                    self.set_iter(len(replies), message)
                END = True

                try:
                    correct = replies[iter].strip()
                    wrong_repl1 = self.wd.replace_with_synonyms(correct)
                except Exception as e:
                    END = False
                    print(f"Произошла ошибка в установке correct: {e}")
                    self.end_dialog(message)

                if END:

                    if 1 <= iter <= len(replies):
                        bot_repl = replies[iter - 1].strip()
                        if bot_repl: 
                            self.bot.send_message(message.chat.id, bot_repl)
                        else:
                            END = False
                            print("Ошибка: Попытка отправить пустое сообщение.")

                    if END:
                        messages = [correct, wrong_repl1]
                        random.shuffle(messages)
                        for i, msg in enumerate(messages):
                            if msg is not None and msg != '': 
                                self.bot.send_message(message.chat.id, f'{i+1}. ' + msg)
                            else:
                                self.bot.send_message(message.chat.id, "Wow!I have nothing to say.")

                        markup = types.InlineKeyboardMarkup()
                        buttons = []
                        for i in range(2):
                            is_correct = messages[i] == correct
                            callback_data = f'True{iter}' if is_correct else f'False{iter}'
                            button = types.InlineKeyboardButton(f'{i+1}️⃣', callback_data=callback_data)
                            buttons.append(button)

                        markup.add(*buttons)
                        self.bot.send_message(message.chat.id, 'Choose the correct answer:', reply_markup=markup)

                    else:
                        self.end_dialog(message)

            except Exception as e:
                print(f"Произошла ошибка в dialog_keyboard: {e}")
        else:
           self.end_dialog(message)

    def end_dialog(self, message):
        self.user_db.clear_line(message.chat.id)
        self.bot.send_message(message.chat.id, "Dialog complite!\nВы хорошо постарались😘,\nЧтобы начать новый,\nPress /start_dialog")
