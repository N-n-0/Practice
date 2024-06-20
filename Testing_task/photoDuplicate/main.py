import os
import imghdr
import shutil

from PIL import Image, ImageDraw, ImageFont
from imagehash import average_hash


def input_dir(hash_dict=None):
    path_pic = input('Enter directory path: ')

    if not os.path.exists(path_pic):
        print('Directory doesn\'t exist')
        return input_dir(hash_dict)

    if hash_dict is None:
        hash_dict = {}
    for root, dirs, files in os.walk(path_pic):
        for file in files:
            if is_valid_image(f'{root}/{file}'):
                pic = Image.open(f'{root}/{file}')
                pic_hash = average_hash(pic)
                if pic_hash in hash_dict.keys():
                    hash_dict[pic_hash].append(f'{root}/{file}')
                else:
                    hash_dict[pic_hash] = [f'{root}/{file}']
            else:
                print(f'{root}/{file} is broke')

    if input('Compare images from other directory? Y/N\t').lower() == 'y':
        hash_dict = input_dir(hash_dict)

    for key, value in hash_dict.items():
        hash_dict[key] = list(set(value))

    return hash_dict


def is_valid_image(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(32)
        return imghdr.what(None, header) is not None


def photo_visualisation(key, photo_paths):
    n = len(photo_paths)

    photo = Image.open(photo_paths[0])

    photo.thumbnail((200, 200))

    max_width, max_height = min(200, photo.width), min(200, photo.height)

    total_width = 700
    total_height = n * (max_height + 30)
    collage = Image.new('RGB', (total_width, total_height), (255, 255, 255))

    font = ImageFont.truetype('arial.ttf', 12)

    draw = ImageDraw.Draw(collage)

    x, y = 10, 10
    for i, photo_path in enumerate(photo_paths):
        photo = Image.open(photo_path)

        photo.thumbnail((max_width, max_height))

        collage.paste(photo, (x, y))

        caption = photo_path
        text_x, text_y = x, y + photo.height + 5
        draw.text((text_x, text_y), caption, font=font, fill=(0, 0, 0))

        y += photo.height + 30

    collage.save(f'output/Group{key}.jpg')


def clear_output():
    for filename in os.listdir('output'):
        file_path = os.path.join('output', filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Ошибка при удалении файла {file_path}: {e}")


def main():
    hash_dict = input_dir()
    group_counter = 1
    clear_output()
    for value in hash_dict.values():
        if len(value) > 1:
            photo_visualisation(group_counter, value)
            group_counter += 1


if __name__ == "__main__":
    main()
