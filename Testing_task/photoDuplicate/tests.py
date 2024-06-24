import os
import shutil
from PIL import Image
from imagehash import average_hash
import pytest

from main import (
    input_paths,
    make_hash_dict,
    is_valid_image,
)


@pytest.fixture
def get_dir_name():
    os.makedirs('test_images', exist_ok=True)
    yield os.path.dirname(__file__) + '/test_images'
    shutil.rmtree('test_images')


@pytest.fixture
def test_image(get_dir_name):
    test_image = Image.new('RGB', (100, 100))
    test_image.save(get_dir_name + '/test_image.jpg')
    yield
    os.remove(get_dir_name + '/test_image.jpg')


@pytest.fixture
def broke_image(get_dir_name):
    with open(get_dir_name + '/broke_image.txt', 'w') as f:
        f.write('This is not an image')
    yield
    os.remove(get_dir_name + '/broke_image.txt')


@pytest.fixture
def test_image1_and_test_image2(get_dir_name):
    test_image1 = Image.new('RGB', (100, 100))
    test_image1.save(get_dir_name + '/test_image1.jpg')
    test_image2 = Image.new('RGB', (100, 100))
    test_image2.save(get_dir_name + '/test_image2.jpg')
    yield
    os.remove(get_dir_name + '/test_image1.jpg')
    os.remove(get_dir_name + '/test_image2.jpg')


def test_input_paths_single_directory(monkeypatch, get_dir_name):
    input_values = [get_dir_name, 'n']

    def mock_input(_prompt):
        return input_values.pop(0)

    monkeypatch.setattr('builtins.input', mock_input)
    path1, path2 = input_paths()
    assert path1 == get_dir_name
    assert path2 is None


def test_input_paths_two_directories(monkeypatch, get_dir_name):
    input_values = [get_dir_name, 'y', get_dir_name]

    def mock_input(_prompt):
        return input_values.pop(0)

    monkeypatch.setattr('builtins.input', mock_input)
    path1, path2 = input_paths()
    assert path1 == get_dir_name
    assert path2 == get_dir_name


def test_make_hash_dict_empty():
    hash_dict = make_hash_dict([None, None])
    assert hash_dict == {}


def test_make_hash_dict_single_file(test_image, get_dir_name):
    hash_dict = make_hash_dict([get_dir_name])
    assert len(hash_dict) == 1
    assert hash_dict[average_hash(Image.open(get_dir_name + '/test_image.jpg'))] == [get_dir_name + '/test_image.jpg']


def test_make_hash_dict_duplicates(test_image1_and_test_image2, get_dir_name):
    hash_dict = make_hash_dict([get_dir_name])
    assert len(hash_dict) == 1
    assert sorted(hash_dict[average_hash(Image.open(get_dir_name + '/test_image1.jpg'))]) == [
        get_dir_name + '/test_image1.jpg',
        get_dir_name + '/test_image2.jpg']
    assert sorted(hash_dict[average_hash(Image.open(get_dir_name + '/test_image2.jpg'))]) == [
        get_dir_name + '/test_image1.jpg',
        get_dir_name + '/test_image2.jpg']


def test_is_valid_image_valid(test_image, get_dir_name):
    assert is_valid_image(get_dir_name + '/test_image.jpg')


def test_is_valid_image_invalid(broke_image, get_dir_name):
    assert not is_valid_image(get_dir_name + '/broke_image.txt')
