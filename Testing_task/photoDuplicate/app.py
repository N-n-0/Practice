from modules.loading_images import get_filelist
from modules.controllers import parallel_controller, linear_controller


def find_duplicate_app():
    """
    Находит дубликаты изображений в директории.

    Эта функция получает список файлов из функции `get_filelist` и затем
    решает, использовать параллельный или линейный контроллер на основе длины
    списка файлов. Если список имеет 5000 или более файлов, она использует
    параллельный контроллер, в противном случае она использует линейный контроллер.
    """
    filelist = get_filelist()
    parallel_controller(filelist) if len(filelist) >= 5000 else linear_controller(filelist)


if __name__ == '__main__':
    find_duplicate_app()
