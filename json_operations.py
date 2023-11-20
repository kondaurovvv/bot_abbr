import json
import os


"""
Module : json_operations
"""


def load_json(name_file: str, name_dir: str) -> dict:
    """
    Читает данные из файла JSON.

    :param name_file: Имя файла JSON.
    :type name_file: `str`

    :param name_dir: Имя каталога где хранится JSON.
    :type name_dir: `str`

    :return: Словарь с данными или пустой словарь.
    :rtype: `dict`
    """

    if not os.path.exists(path=name_dir):
        os.makedirs(name_dir)
    file_name: str = os.path.join(name_dir, name_file)
    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="utf-8") as file_json:
            json.dump(dict(), file_json, ensure_ascii=False, indent=4)
    with open(file_name, "r", encoding="utf-8") as file_json:
        return json.load(file_json)


def dump_json(json_dct: dict, name_file: str, name_dir: str) -> None:
    """
    Записывает данные в файл JSON.

    :param path_file: Путь до файла JSON.
    :type path_file: `str`

    :param json_dct: Данные для перевода в JSON формат.
    :type json_dct: `dict`

    :return: Записывает данные в формате JSON в файл.
    :rtype: None
    """

    if not os.path.exists(path=name_dir):
        os.makedirs(name_dir)
    file_name: str = os.path.join(name_dir, name_file)
    with open(file_name, "w", encoding="utf-8") as file_json:
        json.dump(json_dct, file_json, ensure_ascii=False, indent=4)


"""
Этот модуль может загружать и записывать данные из/в файла JSON.
python3 json_operations.py
"""


if __name__ == "__main__":
    pass
    # Test load_json №1
    # json_dct = load_json()

    # Test load_json №2
    # Перед тестирование не забудь создать каталог test и файл test.json
    # name_file = "test.json"
    # name_dir = "test"
    # json_dct = load_json(name_file=name_file, name_dir=name_dir)
    # print(json_dct)

    # Test load_json №3
    # name_file = 'abbreviations.json'
    # json_dct = load_json(name_file=name_file, name_dir='.')
    # print(json_dct)

    # Test load_json №4
    # name_dir = "test"
    # json_dct = load_json(name_dir=name_dir)
    # print(json_dct)

    # Test dump_json №1
    # dump_json()

    # Test dump_json №2 (каталог и файл созданы)
    # name_file = "test.json"
    # name_dir = "test1/21/4"
    # dump_json(json_dct=json_dct, name_dir=name_dir, name_file=name_file)

    # Test dump_json №3 (каталог и файл отсутствуют)
    # name_file = "test.json"
    # name_dir = "test"
    # dump_json(json_dct=json_dct, name_dir=name_dir, name_file=name_file)

    # Test №4
    # name_file = "test.json"
    # dump_json(json_dct=json_dct, name_file=name_file)
