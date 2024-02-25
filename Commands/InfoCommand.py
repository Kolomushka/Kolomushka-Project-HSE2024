from CommandTg import CommandTg

class InfoCommand(CommandTg):
    def handle(self, message):
        self.bot.send_message(message.chat.id, 'Вы можете поддерживать свой уровень английского,\nнаучиться чувстовать логику языку.\nОсновная функция /start_dialog - формирует для вас диалог\nпо теме и сложности на выбор.\nЭто происходит в формате теста,\nесть всего 1 правильная реплика,\nи одна неверная, корректность определяется с нормами устной речи.\nПомним, что собеседники уважают друг-другу\nи оба культруные люди.🤭')

    def get_command_names(self):
        return ['info']
