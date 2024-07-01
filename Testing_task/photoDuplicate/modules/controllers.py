from concurrent.futures import ProcessPoolExecutor
import os
from multiprocessing import Process, RLock, Queue
from modules.utils import clear_or_create_dir, get_chunked_list, merge_dicts
from modules.hashing import get_hashes
from modules.visualization import save_images_with_duplicates


def parallel_controller(filelist):
    """
    Контроллер для обработки списка файлов параллельно.

    Очищает или создает директории вывода, разбивает список файлов на части,
    вычисляет хеши файлов и ищет дубликаты в параллельном режиме, а затем сохраняет изображения с дубликатами.

    Args:
        filelist (list): Список путей к файлам для обработки.

    """
    clear_or_create_dir()
    num_processes = os.cpu_count()

    data = get_chunked_list(filelist, num_processes)

    with ProcessPoolExecutor(num_processes) as executor:
        hashes = executor.map(get_hashes, data)

    merged_dict = merge_dicts(list(hashes))
    data = get_chunked_list([v for v in merged_dict.values() if len(v) > 1], num_processes)

    processes = []
    lock = RLock()
    q = Queue()
    q.put(1)

    for i in range(0, len(data)):
        processes.append(Process(target=save_images_with_duplicates, args=(data[i], q, lock)))

    for process in processes:
        process.start()

    for process in processes:
        process.join()


def linear_controller(filelist):
    """
    Контроллер для обработки списка файлов линейно.

    Очищает или создает директории вывода, вычисляет хеши файлов и 
    ищет дубликаты, а затем сохраняет изображения с дубликатами.

    Args:
        filelist (list): Список путей к файлам для обработки.

    """
    clear_or_create_dir()

    duplicate_dict, group_counter = get_hashes(filelist), 1

    save_images_with_duplicates([v for v in duplicate_dict.values() if len(v) > 1], counter=group_counter)
