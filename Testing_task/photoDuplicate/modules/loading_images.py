import os
from modules.utils import is_valid_image

answers_dict = {
    True: ['yes', 'y'],
    False: ['no', 'n', 'not']
}


def get_dir_paths():
    """
    Получает пути к директориям от пользователя.

    Returns:
        list: Список путей к директориям, предоставленных пользователем.
    """
    dirs = []
    while True:
        path = input("Enter directory path: ")
        if os.path.exists(path):
            dirs.append(path)
            break
        else:
            print("Wrong path. Try again.")

    while True:
        choice = input("Compare images from other directory? (Y/N) ").strip().lower()
        if choice in answers_dict[True]:
            while True:
                path = input("Enter directory path: ")
                if os.path.exists(path):
                    dirs.append(path)
                    break
                else:
                    print("Wrong path. Try again.")
        elif choice in answers_dict[False]:
            break
        else:
            print("Incorrect answer.")

    return dirs


def get_filelist():
    """
    Получает список валидных файлов изображений из заданных путей к директориям.

    Returns:
        list: Список путей к валидным файлам изображений.
    """
    dir_paths, filelist = get_dir_paths(), []
    for path in dir_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if is_valid_image(f'{root}/{file}'):
                    filelist.append(f'{root}/{file}')
                else:
                    print(f'{root}/{file} is broke or not supported')

    return filelist
