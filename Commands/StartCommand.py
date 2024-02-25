from CommandTg import CommandTg

class StartCommand(CommandTg):
    def handle(self, message):
        self.bot.send_message(message.chat.id, f"""
            Доброго времени, {message.from_user.first_name} {message.from_user.last_name}!🤝
        Я помогу вам стать лучше в английском.
        Чтобы начать диалог: /start_dialog
        Посмотреть все команды: /help""")

    def get_command_names(self):
        return ['start']
