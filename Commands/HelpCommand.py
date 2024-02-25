from CommandTg import CommandTg

class HelpCommand(CommandTg):
    def handle(self, message):
        self.bot.send_message(message.chat.id, 'Перечень того, что я могу:\n/start - здесь мы начинаем)🙃\n/help - список команд (мы здесь)😱\n/info - подробное описание функционала бота✅\n/start_dialog - то, зачем вы здесь. Проверьте свои навыки прямо сейчас👍')

    def get_command_names(self):
        return ['help']