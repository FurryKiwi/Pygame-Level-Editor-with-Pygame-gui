import json
import pygame
from Scripts.utils import load_autotile_rules
from Scripts.settings import *


class EditorTileMap:

    def __init__(self, app):
        self.app = app
        self.tilemap = {}
        self.offgrid_tiles = {}

        self.tile_bitmask = {}
        self.rules = {}

        self.current_layer = 0
        self.player_layer = 0
        self.tile_size = 16
        self.current_map = ""

        self.brush_size = 1
        self.show_count = False

        self.recent_tiles = []

        self.load_rules(RULE_PATHS)

    def change_layer(self, layer):
        self.current_layer = int(layer)

    def change_player_layer(self, layer):
        self.player_layer = int(layer)

    def add_layer(self, layer):
        self.tilemap.update({str(layer): {}})
        self.offgrid_tiles.update({str(layer): {}})

    def delete_layer(self, layer):
        if str(layer) in self.tilemap:
            del self.tilemap[str(layer)]
        if str(layer) in self.offgrid_tiles:
            del self.offgrid_tiles[str(layer)]

    def get_layers(self):
        offgrid_layers = [layer for layer in self.offgrid_tiles.keys()]
        grid_layer = [layer for layer in self.tilemap.keys()]
        total = set(offgrid_layers + grid_layer)
        new_list = []
        for i in sorted(total, key=int):
            new_list.append(i)
        return new_list

    def add_tile(self, tile_group, tile_variant, tile_pos, tile_settings):
        pos = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if pos not in self.recent_tiles and self.app.auto_tile:
            self.recent_tiles.append(pos)
        try:
            if tile_group in OBJECT_TYPES:
                self.tilemap[str(self.current_layer)].update({str(tile_pos[0]) + ';' + str(tile_pos[1]):
                                                                  {'type': tile_group,
                                                                   'variant': tile_variant,
                                                                   'pos': tile_pos,
                                                                   'tags': tile_settings}})
            else:
                self.tilemap[str(self.current_layer)].update({str(tile_pos[0]) + ';' + str(tile_pos[1]):
                                                                  {'type': tile_group,
                                                                   'variant': tile_variant,
                                                                   'pos': tile_pos}})
        except KeyError:
            if tile_group in OBJECT_TYPES:
                self.tilemap.update({str(self.current_layer): {str(tile_pos[0]) + ';' + str(tile_pos[1]):
                                                                   {'type': tile_group,
                                                                    'variant': tile_variant,
                                                                    'pos': tile_pos,
                                                                    'tags': tile_settings}}})
            else:
                self.tilemap.update({str(self.current_layer): {str(tile_pos[0]) + ';' + str(tile_pos[1]):
                                                                   {'type': tile_group,
                                                                    'variant': tile_variant,
                                                                    'pos': tile_pos}}})

        if self.brush_size == 5:
            for shift in [N, S, E, W]:
                tile_shift = str(tile_pos[0] + shift[0]) + ';' + str(tile_pos[1] + shift[1])
                if tile_shift not in self.recent_tiles and self.app.auto_tile:
                    self.recent_tiles.append(tile_shift)
                new_tile_pos = ((tile_pos[0] + shift[0]), (tile_pos[1] + shift[1]))
                try:
                    if tile_group in OBJECT_TYPES:
                        self.tilemap[str(self.current_layer)].update({tile_shift: {
                            'type': tile_group, 'variant': tile_variant, 'pos': new_tile_pos,
                            'tags': tile_settings}})
                    else:
                        self.tilemap[str(self.current_layer)].update({tile_shift: {
                            'type': tile_group, 'variant': tile_variant, 'pos': new_tile_pos}})
                except KeyError:
                    if tile_group in OBJECT_TYPES:
                        self.tilemap.update({str(self.current_layer): {tile_shift: {
                            'type': tile_group, 'variant': tile_variant, 'pos': new_tile_pos,
                            'tags': tile_settings}}})
                    else:
                        self.tilemap.update({str(self.current_layer): {tile_shift: {
                            'type': tile_group, 'variant': tile_variant, 'pos': new_tile_pos}}})
        if self.brush_size == 9:
            for shift in [N, S, E, W, NW, NE, SW, SE]:
                tile_shift = str(tile_pos[0] + shift[0]) + ';' + str(tile_pos[1] + shift[1])
                if tile_shift not in self.recent_tiles and self.app.auto_tile:
                    self.recent_tiles.append(tile_shift)
                new_tile_pos = ((tile_pos[0] + shift[0]), (tile_pos[1] + shift[1]))
                try:
                    if tile_group in OBJECT_TYPES:
                        self.tilemap[str(self.current_layer)].update({tile_shift: {
                            'type': tile_group, 'variant': tile_variant, 'pos': new_tile_pos,
                            'tags': tile_settings}})
                    else:
                        self.tilemap[str(self.current_layer)].update({tile_shift: {
                            'type': tile_group, 'variant': tile_variant, 'pos': new_tile_pos}})
                except KeyError:
                    if tile_group in OBJECT_TYPES:
                        self.tilemap.update({str(self.current_layer): {tile_shift: {
                            'type': tile_group, 'variant': tile_variant, 'pos': new_tile_pos,
                            'tags': tile_settings}}})
                    else:
                        self.tilemap.update({str(self.current_layer): {tile_shift: {
                            'type': tile_group, 'variant': tile_variant, 'pos': new_tile_pos}}})

    def remove_tile(self, tile_pos):
        # On Grid Tiles
        tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
        try:
            if tile_loc in self.tilemap[str(self.current_layer)]:
                if self.app.auto_tile:
                    self.recent_tiles.append(tile_loc)
                else:
                    del self.tilemap[str(self.current_layer)][tile_loc]
            if self.brush_size == 5:
                for shift in [N, S, E, W]:
                    tile_shift = str(tile_pos[0] + shift[0]) + ';' + str(tile_pos[1] + shift[1])
                    if tile_shift in self.tilemap[str(self.current_layer)]:
                        if self.app.auto_tile:
                            self.recent_tiles.append(tile_shift)
                        else:
                            del self.tilemap[str(self.current_layer)][tile_shift]
            if self.brush_size == 9:
                for shift in [N, S, E, W, NW, NE, SW, SE]:
                    tile_shift = str(tile_pos[0] + shift[0]) + ';' + str(tile_pos[1] + shift[1])
                    if tile_shift in self.tilemap[str(self.current_layer)]:
                        if self.app.auto_tile:
                            self.recent_tiles.append(tile_shift)
                        else:
                            del self.tilemap[str(self.current_layer)][tile_shift]
        except KeyError:
            pass

    def add_tile_offgrid(self, tile_group, tile_variant, position, tile_settings):
        try:
            if tile_group in OBJECT_TYPES:
                self.offgrid_tiles[str(self.current_layer)].update({str(position[0]) + ';' + str(position[1]):
                                                                        {'type': tile_group,
                                                                         'variant': tile_variant,
                                                                         'pos': position,
                                                                         'tags': tile_settings}})
            else:
                self.offgrid_tiles[str(self.current_layer)].update({str(position[0]) + ';' + str(position[1]):
                                                                        {'type': tile_group,
                                                                         'variant': tile_variant,
                                                                         'pos': position}})
        except KeyError:
            if tile_group in OBJECT_TYPES:
                self.offgrid_tiles.update({str(self.current_layer): {str(position[0]) + ';' + str(position[1]):
                                                                         {'type': tile_group,
                                                                          'variant': tile_variant,
                                                                          'pos': position,
                                                                          'tags': tile_settings}}})
            else:
                self.offgrid_tiles.update({str(self.current_layer): {str(position[0]) + ';' + str(position[1]):
                                                                         {'type': tile_group,
                                                                          'variant': tile_variant,
                                                                          'pos': position}}})

    def remove_tile_offgrid(self, scroll, mpos):
        # TODO: Figure out a better way of doing this
        try:
            for pos in self.offgrid_tiles[str(self.current_layer)].copy():
                tile = self.offgrid_tiles[str(self.current_layer)][pos]
                tile_img = self.app.assets[tile['type']][tile['variant']]
                tile_r = pygame.Rect(tile['pos'][0] - scroll[0], tile['pos'][1] - scroll[1],
                                     tile_img.get_width(), tile_img.get_height())
                if tile_r.collidepoint(mpos):
                    del self.offgrid_tiles[str(self.current_layer)][pos]
        except KeyError:
            pass

    def increase_brush(self):
        self.brush_size += 4
        if self.brush_size >= 9:
            self.brush_size = 9

    def decrease_brush(self):
        self.brush_size -= 4
        if self.brush_size <= 1:
            self.brush_size = 1

    def save(self, path):
        for layer in self.tilemap.copy():
            if self.tilemap[layer] == {}:
                del self.tilemap[layer]
        for layer in self.offgrid_tiles.copy():
            if self.offgrid_tiles[layer] == {}:
                del self.offgrid_tiles[layer]
        with open(path, 'w') as f:
            json.dump({'tilemap': self.tilemap, 'offgrid': self.offgrid_tiles,
                       'tile_size': self.tile_size, 'player_layer': self.player_layer,
                       'current_layer': self.current_layer}, f, indent=4)
        r = path.split('\\')
        self.current_map = r[-1]

    def load(self, path):
        with open(path, 'r') as f:
            map_data = json.load(f)

        self.tilemap = map_data['tilemap']
        self.offgrid_tiles = map_data['offgrid']
        self.tile_size = map_data['tile_size']
        self.player_layer = map_data['player_layer']
        self.current_layer = map_data['current_layer']

        r = path.split('\\')
        self.current_map = r[-1]
        self.brush_size = 1

    def create_new(self):
        """Create a new map."""
        self.tilemap = {}
        self.offgrid_tiles = {}
        self.current_map = "TO_BE_SAVED"
        self.current_layer = 0
        self.player_layer = 0
        self.brush_size = 1
        self.add_layer(0)

    def load_rules(self, id_paths: list):
        """Loads the txt file generated by Tilesetter that has all the calculated values for each variant tile."""
        try:
            for type, path in id_paths:
                self.rules.update({type: load_autotile_rules(path)})
        except FileNotFoundError as err:
            print(err, " Load Rules method couldn't run.")

    def bitwise_method(self, location, direction):
        """Updates the bitwise calculation in the dict."""
        direction_value = BITMASK_LOOKUP[direction]
        try:
            old_value = self.tile_bitmask[str(self.current_layer)][location]["index"]
            new_value = old_value + direction_value
            self.tile_bitmask[str(self.current_layer)][location].update({"index": new_value})
        except KeyError:
            try:
                self.tile_bitmask[str(self.current_layer)].update({location: {"index": direction_value}})
            except KeyError:
                self.tile_bitmask = {str(self.current_layer): {location: {"index": direction_value}}}

    def check_cardinal(self, tile, loc):
        """Check the cardinal directions of the tile were calculating and update the dict."""
        check_type = tile['type']
        count = 0
        for direction in [N, S, E, W]:
            check_loc = str(tile['pos'][0] + direction[0]) + ';' + str(tile['pos'][1] + direction[1])
            if check_loc in self.tilemap[str(self.current_layer)]:
                if check_type == self.tilemap[str(self.current_layer)][check_loc]['type']:
                    self.bitwise_method(loc, (direction[0], direction[1]))
                    count += 1
        if count == 0:
            try:
                self.tile_bitmask[str(self.current_layer)].update({loc: {"index": 0}})
            except KeyError:
                self.tile_bitmask = {str(self.current_layer): {loc: {"index": 0}}}

    def check_diagonals(self, tile, loc):
        """Check's each corner tile as well calls the function to check its cardinal to see if those positions are
        also the same for the middle tile."""
        check_type = tile['type']
        for direction in [NW, NE, SW, SE]:
            check_loc = str(tile['pos'][0] + direction[0]) + ';' + str(tile['pos'][1] + direction[1])
            if check_loc in self.tilemap[str(self.current_layer)]:
                if check_type == self.tilemap[str(self.current_layer)][check_loc]['type']:
                    corner_tile = self.tilemap[str(self.current_layer)][check_loc]
                    if direction == NW:
                        self.check_corner_cardinal(direction, corner_tile, loc, check_type)
                    elif direction == NE:
                        self.check_corner_cardinal(direction, corner_tile, loc, check_type)
                    elif direction == SE:
                        self.check_corner_cardinal(direction, corner_tile, loc, check_type)
                    elif direction == SW:
                        self.check_corner_cardinal(direction, corner_tile, loc, check_type)

    def check_corner_cardinal(self, direction, corner_tile, loc, check_type):
        """Check's the corner's tile cardinal so if there's 2 tiles of the same type beside it that is also beside
        the middle tile were checking, then add this corner tile's number to the middle tiles total."""
        count = 0
        for shift in DIRECTION_LOOKUP[direction]:
            c_loc = str(corner_tile['pos'][0] + shift[0]) + ';' + str(corner_tile['pos'][1] + shift[1])
            if c_loc in self.tilemap[str(self.current_layer)]:
                if check_type == self.tilemap[str(self.current_layer)][c_loc]['type']:
                    count += 1
        if count == 2:
            self.bitwise_method(loc, (direction[0], direction[1]))

    def change_variants(self):
        """Swaps the variant out with the calculated variant."""
        for location in self.tile_bitmask[str(self.current_layer)]:
            tile = self.tilemap[str(self.current_layer)][location]
            if tile['type'] in AUTOTILE_TYPES:
                bitmask = self.tile_bitmask[str(self.current_layer)][location]['index']
                tile_type = self.tilemap[str(self.current_layer)][location]['type']
                variant = self.rules[tile_type][bitmask]
                tile['variant'] = variant

    def get_tiles_around(self, tile, pos):
        """Returns key: list[] with the 'type' being the key for the tiles added and loc to a list.
        Checks the tiles cardinal and diagonal positions for proper type and if there's a tile there so we can
        update that tiles variant."""
        tiles_around = {}
        for direction in [N, S, E, W, NW, NE, SW, SE]:
            check_loc = str(pos[0] + direction[0]) + ';' + str(pos[1] + direction[1])
            # Check if there's a tile in that direction, and it is a tile on the map
            if check_loc in self.tilemap[str(self.current_layer)]:
                check_type = self.tilemap[str(self.current_layer)][check_loc]['type']
                # Check if that tile is the same type as the one that got placed
                if tile['type'] == check_type:
                    # Make sure we're not checking a tile that will be checked by the main for loop
                    if check_loc not in self.recent_tiles:
                        try:
                            # Make sure were not adding any duplicates
                            if check_loc not in tiles_around[tile['type']]:
                                tiles_around[tile['type']].append(check_loc)
                        except KeyError:
                            tiles_around.update({tile['type']: [check_loc]})
                # If it's not the same type, were going to add it to it's own list for updating it's variant.
                else:
                    # Make sure we're not checking a tile that will be checked by the main for loop
                    if check_loc not in self.recent_tiles:
                        # Grab the correct tile that's not the same type as were checking
                        check_tile = self.tilemap[str(self.current_layer)][check_loc]
                        try:
                            # Make sure we're not adding any duplicates
                            if check_loc not in tiles_around[check_tile['type']]:
                                tiles_around[check_tile['type']].append(check_loc)
                        except KeyError:
                            tiles_around.update({check_tile['type']: [check_loc]})
        return tiles_around

    def autotile(self, delete=False):
        """Auto tiles only the recently placed or removed tiles."""
        self.tile_bitmask = {str(self.current_layer): {}}
        try:
            for loc in self.recent_tiles:
                # Loop through all the recent tile places onto the map or removed from map
                tile = self.tilemap[str(self.current_layer)][loc]
                pos = (tile['pos'][0], tile['pos'][1])
                # Check all 8 directions of each one of the recently placed/removed tiles
                tiles_around = self.get_tiles_around(tile, pos)
                # Calculate the tile we added to the map as long as were not deleting it.
                if not delete:
                    self.check_cardinal(tile, loc)
                    self.check_diagonals(tile, loc)

                # Update the placed tile's variant if not removing it from map
                if not delete:
                    self.change_variants()

                # Remove the tiles from the tilemap
                if delete:
                    del self.tilemap[str(self.current_layer)][loc]
                # Reset the calculations
                self.tile_bitmask = {str(self.current_layer): {}}
                # Calculate all the rest of the tiles around the tiles we placed
                for t in tiles_around:
                    for loc in tiles_around[t]:
                        tile = self.tilemap[str(self.current_layer)][loc]
                        self.check_cardinal(tile, loc)
                        self.check_diagonals(tile, loc)
                    # Update all the other tiles around the tiles we placed to their proper variants.
                    self.change_variants()

            self.recent_tiles = []
        except KeyError:
            self.recent_tiles = []
            pass

    def all_autotile(self):
        """Auto tiles the entire map."""
        self.tile_bitmask = {str(self.current_layer): {}}
        try:
            for loc in self.tilemap[str(self.current_layer)]:
                tile = self.tilemap[str(self.current_layer)][loc]
                # Check the tile type of the tile on each of its sides and check if there is a tile on its sides.
                self.check_cardinal(tile, loc)
                self.check_diagonals(tile, loc)
            # Loop through and swap tiles with the proper variant
            self.change_variants()
        except KeyError:
            pass

    def render(self, surf, offset):
        """Renders only tiles that are within the surf size starting with the offgrid tiles."""
        # For debug purposes
        count = 0
        # Grab all layers from offgrid tiles and tilemap and remove any duplicates
        tilemap_layers = [int(x) for x in self.tilemap.keys()]
        offgrid_layers = [int(x) for x in self.offgrid_tiles.keys()]
        lowest_layer = set(tilemap_layers + offgrid_layers)
        # Loop through the layers in order from negative to positive
        for layer in sorted(lowest_layer, key=int):
            layer = str(layer)
            # Offgrid tiles rendering ______________________________________________________________________
            if layer in self.offgrid_tiles:
                for pos in self.offgrid_tiles[layer]:
                    tile = self.offgrid_tiles[layer][pos]
                    tile_img = self.app.assets[tile['type']][tile['variant']]
                    tile_x = tile['pos'][0] - offset[0]
                    tile_y = tile['pos'][1] - offset[1]
                    range_x = surf.get_width() - offset[0] // self.tile_size
                    range_y = surf.get_height() - offset[1] // self.tile_size
                    if tile_x in range(0 - tile_img.get_width(), range_x + tile_img.get_width()) and \
                            tile_y in range(0 - tile_img.get_height(), range_y + tile_img.get_height()):
                        surf.blit(tile_img, (tile_x, tile_y))
                        if self.show_count:
                            count += 1
            # On grid tiles rendering _____________________________________________________________________
            if layer in self.tilemap:
                for loc in self.tilemap[layer]:
                    tile = self.tilemap[layer][loc]
                    tile_img = self.app.assets[tile['type']][tile['variant']]
                    tile_x = tile['pos'][0] * self.tile_size - offset[0]
                    tile_y = tile['pos'][1] * self.tile_size - offset[1]
                    range_x = surf.get_width() - offset[0] // self.tile_size
                    range_y = surf.get_height() - offset[1] // self.tile_size
                    if tile_x in range(0 - self.tile_size, range_x + 32) and \
                            tile_y in range(0 - self.tile_size, range_y):
                        surf.blit(tile_img, (tile_x, tile_y))
                        if self.show_count:
                            count += 1

        if self.show_count:
            print(f"Tiles Drawn: {count}")
