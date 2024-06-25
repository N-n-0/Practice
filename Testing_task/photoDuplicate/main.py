import os
import imghdr
import shutil
from itertools import chain

from PIL import Image, ImageDraw, ImageFont
from imagehash import average_hash
import keras
import numpy as np
from scipy.spatial.distance import cosine


model = keras.applications.vgg16.VGG16(weights='imagenet', include_top=True)
feat_extractor = keras.models.Model(inputs=model.input, outputs=model.get_layer("fc2").output)


def input_paths():
    while True:
        path1 = input("Enter directory path: ")
        if os.path.exists(path1):
            break
        else:
            print("Wrong path. Try again.")

    while True:
        choice = input("Compare images from other directory? (Y/N) ")
        if choice.lower().rstrip().lstrip() == 'y' or choice.lower().rstrip().lstrip() == 'yes':
            while True:
                path2 = input("Enter second directory path: ")
                if os.path.exists(path2):
                    return path1, path2
                else:
                    print("Wrong path. Try again.")
        elif choice.lower().rstrip().lstrip() == 'n' or choice.lower().rstrip().lstrip() == 'no':
            return path1, None
        else:
            print("Enter 'y' or 'n'.")


def clear_dirs():
    if os.path.exists('features'):
        for filename in os.listdir('features'):
            file_path = os.path.join('features', filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error with deleting {file_path}: {e}")
    else:
        os.makedirs('features', exist_ok=True)

    if os.path.exists('hash'):
        for filename in os.listdir('hash'):
            file_path = os.path.join('hash', filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error with deleting {file_path}: {e}")
    else:
        os.makedirs('hash', exist_ok=True)

def is_valid_image(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(32)
        return imghdr.what(None, header) is not None


def make_filelist(paths):
    filelist = []
    for path in paths:
        if path is not None:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if is_valid_image(f'{root}/{file}'):
                        filelist.append(f'{root}/{file}')
                    else:
                        print(f'{root}/{file} is broke')

    return list(set(filelist))


def make_hash_dict(filelist):
    hash_dict = {}
    for file in filelist:
        pic = Image.open(file)
        pic_hash = average_hash(pic)
        if pic_hash in hash_dict.keys():
            hash_dict[pic_hash].append(file)
        else:
            hash_dict[pic_hash] = [file]

    return hash_dict


def duplicates_by_hash(filelist):
    duplicate_dict, group_counter = make_hash_dict(filelist), 1

    for value in duplicate_dict.values():
        if len(value) > 1:
            photo_visualisation(group_counter, value)
            group_counter += 1


def make_features_dict(filelist):
    feature_dict = {}
    for image_path in filelist:
        image = keras.preprocessing.image.load_img(image_path, target_size=model.input_shape[1:3])
        image_data = keras.preprocessing.image.img_to_array(image)
        image_data = np.expand_dims(image_data, axis=0)
        image_data = keras.applications.imagenet_utils.preprocess_input(image_data)
        features = feat_extractor.predict(image_data).flatten()
        feature_dict[image_path] = features

    duplicate_dict = {}
    feature_dict_keys = list(feature_dict.keys())

    for i in range(0, len(feature_dict_keys)):
        feature = feature_dict[feature_dict_keys[i]]
        if feature_dict_keys[i] not in list(chain(*duplicate_dict.values())):
            duplicate_dict[i + 1] = [feature_dict_keys[i]]
            for j in range(i + 1, len(feature_dict_keys)):
                if 1 - cosine(feature, feature_dict[feature_dict_keys[j]]) >= 0.9:
                    duplicate_dict[i + 1].append(feature_dict_keys[j])

    return duplicate_dict


def duplicates_by_features(filelist):
    duplicate_dict, group_counter = make_features_dict(filelist), 1

    for value in duplicate_dict.values():
        if len(value) > 1:
            photo_visualisation(group_counter, value, output='features')
            group_counter += 1


def photo_visualisation(key, photo_paths, output='hash'):
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
        draw.text((text_x, text_y), f'{i+1} : {photo_path}', font=font, fill=(0, 0, 0))

        x += photo.width + 20
        text_y += 17

    collage.save(f'{output}/Group{key}.bmp')


def main():
    dirs = input_paths()
    clear_dirs()
    filelist = make_filelist(dirs)
    duplicates_by_hash(filelist)
    duplicates_by_features(filelist)


if __name__ == "__main__":
    main()
