import imghdr
import os
import shutil
from collections import defaultdict


def is_valid_image(file_path):
    """
    Проверяет, является ли файл валидным изображением.

    Args:
        file_path (str): Путь к файлу для проверки.

    Returns:
        bool: True, если файл является валидным изображением, False — во всех других случаях.
    """
    with open(file_path, 'rb') as f:
        header = f.read(32)
        return imghdr.what(None, header) is not None


def clear_or_create_dir():
    """
    Очищает директорию output, если она существует, или создает ее, если она не существует.

    """
    if os.path.exists('output'):
        for filename in os.listdir('output'):
            file_path = os.path.join('output', filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error with deleting {file_path}: {e}")
    else:
        os.makedirs('output', exist_ok=True)


def get_chunked_list(filelist, num_processes):
    """
    Разбивает список файлов на чанки для параллельной обработки.

    Args:
        filelist (list): Список файлов.
        num_processes (int): Количество процессов для параллельной обработки.

    Returns:
        list: Список чанков, где каждый чанк - это список файлов.
    """
    chunk = len(filelist) // num_processes
    data = []

    for i in range(0, len(filelist) - 2 * chunk, chunk):
        data.append((filelist[i:i + chunk]))

    data.append((filelist[i + chunk:]))

    return data


def merge_dicts(dicts):
    """
    Объединяет несколько словарей в один.

    Args:
        dicts (list): Список словарей для объединения.

    Returns:
        dict: Объединенный словарь.
    """
    merged_dict = defaultdict(list)

    for d in dicts:
        for key, value in d.items():
            merged_dict[key].extend(value)
            merged_dict[key] = list(set(merged_dict[key]))

    return dict(merged_dict)