from PIL import Image
from imagehash import average_hash


def get_hashes(filelist):
    """
    Вычисляет средние хеши для списка файлов изображений и группирует их по значению хеша.

    Args:
    filelist (list): Список путей к файлам изображений.

    Returns:
    dict: Словарь, где каждый ключ - это значение среднего хеша,
    а каждый значение - это список путей к файлам, имеющим это значение хеша.
    """
    hash_dict = {}
    for file in filelist:
        pic = Image.open(file)
        pic_hash = average_hash(pic)
        hash_dict.setdefault(pic_hash, []).append(file)
    return hash_dict
