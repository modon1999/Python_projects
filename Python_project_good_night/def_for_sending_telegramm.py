from telethon.sync import TelegramClient

api_hash = '7XXXXXXXXXXXXXXXXXXXXXX8'
api_id = 1XXXXXX7

phone = '+79XXXXXXX4'
username = 'mXXXXXXn'

# (2) Create the client and connect
client = TelegramClient(username, api_id, api_hash)
client.connect()

# Ensure you're authorized
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))
    client.sign_in(password=input('Password: '))


def sending_congratulation_message(username):
    """
    Функция отправляет сообщение с пожеланием спокойной ночи от имени аккаунта, на вход принимает пользователя,
    которому необходимо отправить сообщение
    """
    client.send_message(username, 'Спокойной ночи!❤️❤️❤️')
