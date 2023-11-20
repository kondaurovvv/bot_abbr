import telebot

import json_operations as jo
import log_operations as lo
from config import API_TOKEN, file_name, data_path
import csv_operations as co


bot = telebot.TeleBot(token=API_TOKEN)


@bot.message_handler(commands=["help"])
def help_user(message: telebot.types.Message) -> None:
    """
    Приветствует пользователя и рассказывает о возможностях бота.

    :param message: Данные в JSON формате.
    :type message: :class:`telebot.types.Message`

    :return: Отправляет сообщения в чат.
    :rtype: None
    """
    lo.assembly_of_new_users(message)
    lo.assembly_all_users(message)
    first_name: str = message.from_user.first_name
    last_name: str = message.from_user.last_name
    msg_lst: list = [
        f"Привет {first_name} {last_name}!",
        f"Рад Вас видеть!.",
        f"Напишите аббревиатуру на русском языке и бот выдаст расшифровку.",
        f'Вы можете добавить свою расшифровку аббревиатуры в формате "аббревиатура=расшифровка".',
        f"Пример: КГБ=Комитет Государственной Безопасности",
        f"Если Вы увидели ошибку в рассшифровке аббрревеатуры то можете исправить её.",
    ]
    msg: str = "\n".join(msg_lst)
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message) -> None:
    """
    Приветствует пользователя.

    :param message: Данные в JSON формате.
    :type message: :class:`telebot.types.Message`

    :return: Отправляет сообщения в чат.
    :rtype: None
    """
    lo.assembly_of_new_users(message)
    lo.assembly_all_users(message)
    first_name: str = message.from_user.first_name
    last_name: str = message.from_user.last_name
    msg_lst: list = [
        f"Здравствуйте {first_name} {last_name}!",
        f"Рад Вас видеть! Какая аббревиатура Вас интерисует?",
    ]
    msg: str = "\n".join(msg_lst)
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["statistics"])
def producing_statistics(message: telebot.types.Message) -> None:
    lo.assembly_of_new_users(message)
    lo.assembly_all_users(message)
    count = co.read_csv('log/log.csv')
    abbreviations: dict = jo.load_json(name_file=file_name, name_dir=data_path)
    number_letters_words: int = len(
        ("".join((abbreviations.keys())) + "".join((abbreviations.values()))).replace(
            " ", ""
        )
    )
    sum_all_keys: int = len("".join(abbreviations.keys()))
    sum_all_transcripts: int = len("".join(abbreviations.values()))
    sorted_transcripts = sorted(
        lo.ten_most_popular_transcripts.items(), key=lambda item: item[1], reverse=True
    )
    if len(sorted_transcripts) > 10:
        sorted_transcripts = [sorted_transcripts[i] for i in range(10)]
    sorted_all_users = sorted(lo.all_users.items(),key=lambda item: item[1], reverse=True )
    if len(sorted_all_users) > 10:

        sorted_all_users = [sorted_all_users[i] for i in range(10)]
    msg_lst: list = [
        f"Количество ключевых слов: {len(abbreviations.keys())}",
        f"Количество букв в словаре - сумма всех ключей + сумма всех расшифровок: {number_letters_words - sum_all_keys + sum_all_transcripts}",
        f"10 последних добавленных расшифровок: {', '.join(lo.ten_most_recently_added_transcripts)}",
        f"10 самых популярных расшифровок: {sorted_transcripts}",
        f"10 самых последних впервые встретившихся пользователей: {lo.ten_most_recent_first_time_users}",
        f"10 самых активных пользователей: {lo.all_users}",
        f"10 недавних дней и количество обращений к боту: {count}"
    ]
    msg: str = "\n".join(msg_lst)
    bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=["text"])
def decipher_abbreviations(message: telebot.types.Message) -> None:
    """
    Возращает аббревеаттуру запрошеную пользователем или
    добавляет аббреввеатуру запрошеную пользователем.

    :param message: Данные в JSON формате.
    :type message: :class:`telebot.types.Message`

    :return: Возращает рассшифровку аббревеатуры.
    :rtype: None
    """
    lo.assembly_of_new_users(message)
    lo.assembly_all_users(message)
    message_from_user: str = message.text
    log_lst: list = [
        message.chat.id,
        message.from_user.first_name,
        message.from_user.last_name,
        message.text,
    ]
    lo.save_text_log(log_lst)
    abbreviations: dict = jo.load_json(name_file=file_name, name_dir=data_path)
    if "=" in message_from_user:
        lo.adding_transcripts(message_from_user)
        new_abbreviation: str = message_from_user.split("=")
        text: str = f'{abbreviations.get(new_abbreviation[0].strip().upper()) if abbreviations.get(new_abbreviation[0].strip().upper()) else ""}{new_abbreviation[1].strip()}, '
        abbreviations[new_abbreviation[0].strip().upper()] = text
        jo.dump_json(name_file=file_name, name_dir=data_path, json_dct=abbreviations)
        msg: str = "Мы запомнили аббревиатуру!"
        bot.send_message(message.chat.id, msg)
    elif message_from_user.upper() in abbreviations:
        lo.count_popular_transcripts(message_from_user.upper())
        if len(abbreviations[message_from_user.upper()]) > 4095:
            for i in range(0, len(abbreviations[message_from_user.upper()]), 4095):
                bot.reply_to(
                    message, text=abbreviations[message_from_user.upper()][i : i + 4095]
                )
        else:
            msg: str = (
                f"{message_from_user} = {abbreviations[message_from_user.upper()]}"
            )
            bot.send_message(message.chat.id, msg)
    else:
        msg_lst: list = [
            f"На сегодняшний день я не знаю расшифровку {message_from_user}, но Вы можете предложить свою =)",
            f'В формате "аббревеатура=расшифровка"',
        ]
        msg: str = "\n".join(msg_lst)
        bot.send_message(message.chat.id, msg)


"""
start - Старт
help - Помощь
Основной функционал bot_abbr.
Приветствие пользователя.
Рассшифровка аббревеатур.
Запись новых аббревеатур.
python3 bot.py
"""


if __name__ == "__main__":
    bot.infinity_polling()
