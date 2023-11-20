from datetime import datetime
from datetime import timedelta
import csv_operations as co


"""
Module : log_operations
"""


ten_most_recently_added_transcripts: list = []
ten_most_popular_transcripts: dict = dict()
ten_most_recent_first_time_users: list = []
all_users: dict = dict()


def save_text_log(message) -> None:
    """
    Записывает даные о пользователе:
        1) Дату обращения пользователя;
        2) Время обращения пользователя:
        3) Чат ID пользователя;
        4) Первое имя пользователя;
        5) Второе имя пользователя;
        6) Текст отправленый пользователем.

    :param log_lst: Данные о пользователе.
    :type log_lst: `list`

    :return: Записывает данные в формате CSV в файл log.csv.
    :rtype: None
    """

    date_time: datetime = datetime.now()
    current_date: str = date_time.strftime("%d-%m-%Y")
    current_time: str = date_time.strftime("%H:%M:%S")
    log_lst: list = [
        message.chat.id,
        message.from_user.first_name,
        message.from_user.last_name,
        message.text,
    ]
    def save_log(log_lst):
        with open("log/log.csv", "a", encoding="utf8") as file_log:
            user_text: str = (
                log_lst[3]
                .replace("\n", " ")
                .replace("'", "*")
                .replace('"', "**")
                .replace(";", "|")
            )  # Сделать отдельнгой функций
            csv_str: str = f'"{current_date}";"{current_time }";"{log_lst[0]}";"{log_lst[1]}";"{log_lst[2]}";"{user_text}"\n'
            file_log.write(csv_str)


def adding_transcripts(text):
    if len(ten_most_recently_added_transcripts) == 10:
        ten_most_recently_added_transcripts.pop(0)
    ten_most_recently_added_transcripts.append(text)


def count_popular_transcripts(text):
    if text in ten_most_popular_transcripts:
        ten_most_popular_transcripts[text] += 1
    else:
        ten_most_popular_transcripts[text] = 1


def assembly_of_new_users(message):
    if str(message.from_user.id) not in ten_most_recent_first_time_users:
        ten_most_recent_first_time_users.append(str(message.from_user.id))
    if len(ten_most_recent_first_time_users) > 10:
        ten_most_recent_first_time_users.pop(0)


def assembly_all_users(message):
    if message.from_user.id in all_users:
        all_users[message.from_user.id] += 1
    else:
        all_users[message.from_user.id] = 1


def collection_of_the_number_of_hits():
    date_lst = []
    for i in range(10):
        date = datetime.today() - timedelta(days=i)
        date = date.strftime("%d-%m-%Y")
        date_lst.append(date)
    co.read_csv('log/log.csv')



"""
Этот модуль может записывать данные в файла CSV.
python3 log_operations.py
"""


if __name__ == "__main__":
    # pass
    # Test save_text_log №1
    log_lst: list = ["5676564257", "Владимир", "Кондауров", "КГБ"]
    save_text_log(log_lst)

    # Test save_text_log №2
    log_lst: list = ["5676564257", "Владимир", "Кондауров", "йцу😡"]
    save_text_log(log_lst)

    # Test save_text_log №3
    log_lst: list = ["5676564257", "Владимир", "Кондауров", "чсмчв\nывачясм\nячсмяс"]
    save_text_log(log_lst)

    # Test save_text_log №4
    log_lst: list = [
        "5676564257",
        "Владимир",
        "Кондауров",
        "ячсячс \"zxcczxc\", qweqw 'vbfxvx',:dasd;qweq;",
    ]
    save_text_log(log_lst)

    # with open("log.csv", "r", encoding="utf8") as file_log:
    #     print(file_log.read())

    collection_of_the_number_of_hits()
