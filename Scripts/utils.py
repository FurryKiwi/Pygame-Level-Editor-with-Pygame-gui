import os
import json
import pygame
import time
import functools
from Scripts.settings import *

# For testing purposes
def timefunc(func):
    """timefunc's doc"""

    @functools.wraps(func)
    def time_closure(*args, **kwargs):
        """time_wrapper's doc string"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        time_elapsed = time.perf_counter() - start
        print(f"Function: {func.__name__}, Time: {time_elapsed}")
        return result

    return time_closure


def load_autotile_rules(path):
    """Load in the calculations from Tile-Setter text file."""
    data = read_bitmask(BASE_IMG_PATH + path)
    id_lists = data['blob_sets'][0]['members']
    rules = {}
    for dic in id_lists:
        i, role = dic.values()
        rules.update({role: i})
    return rules


def read_bitmask(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def clip(surf, x, y, x_size, y_size):
    """Helper function for loading tile-sets."""
    handle_surf = surf.copy()
    snip = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(snip)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


def load_tileset(path):
    """Loads in and clips each tile from the image Tile-Setter exports."""
    tileset_img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    tileset_img.set_colorkey((0, 0, 0))
    tile_size = 16
    tile_count_width = int(tileset_img.get_width() / tile_size)
    tile_count_height = int(tileset_img.get_height() / tile_size)
    images = []
    for h in range(tile_count_height):
        for w in range(tile_count_width):
            if h == 5 and w == 7:
                return images
            new_image = clip(tileset_img, w * tile_size, h * tile_size, tile_size, tile_size)
            images.append(new_image)


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images
