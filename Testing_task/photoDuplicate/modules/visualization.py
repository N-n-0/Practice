from PIL import Image, ImageDraw, ImageFont
from queue import Empty


def get_image_with_duplicates(photo_paths):
    """
    Создает коллажное изображение с миниатюрами дубликатов фотографий.

    Параметры:
    photo_paths (list): Список путей к файлам фотографий

    Возвращает:
    Image: Коллажное изображение с миниатюрами дубликатов фотографий
    """
    n = len(photo_paths)

    photo = Image.open(photo_paths[0])
    photo.thumbnail((200, 200))

    max_width, max_height, max_char_width = min(200, photo.width), min(200, photo.height), 6

    total_width = max(n*(max_width+20), max(len(path) * max_char_width for path in photo_paths)+4)
    total_height = 15 + max_height + 17*(n+1)

    collage = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    font = ImageFont.truetype('arial.ttf', 12)
    draw = ImageDraw.Draw(collage)

    text_x, text_y, x, y = 10, max_height + 32, 10, 10

    for i, photo_path in enumerate(photo_paths):
        photo = Image.open(photo_path)
        photo.thumbnail((max_width, max_height))

        collage.paste(photo, (x, y))
        draw.text((x+photo.width/2, y+photo.height+5), str(i+1), font=font, fill=(0, 0, 0))
        draw.text((text_x, text_y), f'{i+1} : {photo_paths[i]}', font=font, fill=(0, 0, 0))

        x += photo.width + 20
        text_y += 17

    return collage


def save_images_with_duplicates(photo_paths, q=None, lock=None, counter=None):
    """
    Сохраняет коллажное изображение с миниатюрами дубликатов фотографий в файл.

    Параметры:
    photo_paths (list): Список списков путей к файлам фотографий
    q (Queue): Очередь для получения следующего номера группы
    lock (Lock): Опциональный блокировщик для доступа к очереди
    counter (int): Счетчик группы дубликатов
    """
    for path in photo_paths:
        collage = get_image_with_duplicates(path)
        if lock is None:
            collage.save(f'output/Group{counter}.bmp')
            counter += 1
        else:
            with lock:
                try:
                    key = q.get(timeout=1)
                    collage.save(f'output/Group{key}.bmp')
                    q.put(key + 1)
                except Empty as err:
                    print("Empty", err)
