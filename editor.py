import sys
import pygame
import time
import os

from Scripts.utils import load_images, load_tileset
from Scripts.tilemap import EditorTileMap
from Scripts.pg_gui_elements.ui_app import UIApp
from Scripts.settings import *

WINDOW_SIZE = (1480, 900)
DISPLAY = (400, 400)
SCALE_SIZE = (900, 900)
UI_DISPLAY = (580, 900)
RENDER_SCALE_X = SCALE_SIZE[0] / DISPLAY[0]
RENDER_SCALE_Y = SCALE_SIZE[1] / DISPLAY[1]
BASE_COLOR = (10, 30, 40)
UI_COLOR = (30, 40, 50)
MAP_NAME = "data\\maps\\test.json"

TARGET_FPS = 60
SET_FPS = 60


class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Editor')
        self.flags = pygame.HWACCEL
        try:
            self.screen = pygame.display.set_mode(WINDOW_SIZE, flags=self.flags, vsync=True)
            v_sync = True
            print(f"VSync: {v_sync}")
        except pygame.error:
            self.screen = pygame.display.set_mode(WINDOW_SIZE)
            v_sync = False
            print(f"VSync: {v_sync}")
        self.display = pygame.Surface(DISPLAY, pygame.SRCALPHA)

        self.clock = pygame.time.Clock()

        self.assets = self.load_assets()

        self.movement = [False, False, False, False]

        self.scroll = [0, 0]

        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.ctrl = False
        self.ongrid = True
        self.fps_visible = True
        self.last_tick = time.time()
        self.time_delta = None
        self.auto_tile = True
        self.mouse_focus = True
        self.d_scale_width = SCALE_SIZE[0]
        self.d_scale_height = SCALE_SIZE[1]

        self.tilemap = EditorTileMap(self)
        self.ui_manager = UIApp(self, WINDOW_SIZE, UI_DISPLAY)
        self.ui_manager.create_ui()

        try:
            self.ui_manager.load_map(MAP_NAME)
        except FileNotFoundError:
            self.ui_manager.create_new()
    def load_assets(self):
        data = {}
        for key, path in TILE_SETS_PATHS.items():
            ext = os.path.splitext(path)[1]

            if ext == '.png':
                data.update({key: load_tileset(path)})
            else:
                data.update({key: load_images(path)})
        return data

    def show_fps(self):
        if self.fps_visible:
            self.ui_manager.show_fps(self.clock.get_fps())
        else:
            self.ui_manager.show_fps(0)

    def run(self):
        while True:
            self.clock.tick(SET_FPS)
            # Time delta calculation
            self.time_delta = time.time() - self.last_tick
            self.time_delta *= TARGET_FPS
            self.last_tick = time.time()

            self.display.fill(BASE_COLOR)

            self.scroll[0] += ((self.movement[1] - self.movement[0]) * 4) * self.time_delta
            self.scroll[1] += ((self.movement[3] - self.movement[2]) * 4) * self.time_delta
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            self.tile_group, self.tile_variant = self.ui_manager.get_current_tile()
            tile_settings = self.ui_manager.get_tile_settings()
            
            try:
                current_tile_img = self.assets[self.tile_group][self.tile_variant].copy()
                current_tile_img.set_alpha(150)
            except IndexError:
                current_tile_img = self.assets[self.tile_group][0].copy()
                current_tile_img.set_alpha(150)

            mpos = pygame.mouse.get_pos()
            true_mpos = mpos
            self.mouse_focus = pygame.mouse.get_focused()
            mpos = (mpos[0] / RENDER_SCALE_X, mpos[1] / RENDER_SCALE_Y)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                        int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            # Shows an overlay of the current tile to be placed at the location
            if self.ongrid and self.mouse_focus:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                                                     tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
                if self.tilemap.brush_size == 5:
                    for shift in [N, S, E, W]:
                        self.display.blit(current_tile_img,
                                          ((tile_pos[0] + shift[0]) * self.tilemap.tile_size - self.scroll[0],
                                           (tile_pos[1] + shift[1]) * self.tilemap.tile_size - self.scroll[1]))
                if self.tilemap.brush_size == 9:
                    for shift in [N, S, E, W, NW, NE, SW, SE]:
                        self.display.blit(current_tile_img,
                                          ((tile_pos[0] + shift[0]) * self.tilemap.tile_size - self.scroll[0],
                                           (tile_pos[1] + shift[1]) * self.tilemap.tile_size - self.scroll[1]))
            elif not self.ongrid and self.mouse_focus:
                self.display.blit(current_tile_img, mpos)

            # Placing tiles onto grid
            if self.clicking and self.ongrid:
                self.tilemap.add_tile(self.tile_group, self.tile_variant, tile_pos, tile_settings)
                if self.auto_tile:
                    self.tilemap.autotile()

            # Removing tiles from on and off grid
            if self.right_clicking:
                # On Grid Tiles
                self.tilemap.remove_tile(tile_pos)
                # Off Grid Tiles
                self.tilemap.remove_tile_offgrid(self.scroll, mpos)
                if self.auto_tile:
                    self.tilemap.autotile(delete=True)

            # Display the current selected tile in top left corner
            self.display.blit(current_tile_img, (5, 3))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and self.mouse_focus:
                    if event.button == 1 and not self.ui_manager.manager.hovering_any_ui_element:
                        self.clicking = True
                        # Place off grid tiles. Have to have this here, so it's a per click call and not hold click
                        if not self.ongrid:
                            position = round(mpos[0] + self.scroll[0]), round(mpos[1] + self.scroll[1])
                            self.tilemap.add_tile_offgrid(self.tile_group, self.tile_variant, position, tile_settings)

                    if event.button == 3 and not self.ui_manager.manager.hovering_any_ui_element:
                        self.right_clicking = True

                    if self.ctrl:
                        if event.button == 4:
                            self.tilemap.increase_brush()
                            self.ui_manager.update_labels()
                        if event.button == 5:
                            self.tilemap.decrease_brush()
                            self.ui_manager.update_labels()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                elif event.type == pygame.KEYDOWN and self.mouse_focus:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                        self.ui_manager.update_labels()
                    if event.key == pygame.K_t:
                        self.tilemap.all_autotile()
                    if event.key == pygame.K_F12:
                        self.fps_visible = not self.fps_visible
                    if event.key == pygame.K_F11:
                        self.auto_tile = not self.auto_tile
                        self.ui_manager.update_labels()
                    # FOR DEBUG PURPOSES
                    if event.key == pygame.K_F10:
                        self.tilemap.show_count = not self.tilemap.show_count
                    if event.key == pygame.K_LCTRL:
                        self.ctrl = True
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LCTRL:
                        self.ctrl = False

                self.ui_manager.process_events(event, true_mpos)

            self.ui_manager.manager.update(self.time_delta)

            self.show_fps()

            self.screen.blit(pygame.transform.scale(self.display,
                                                    (self.d_scale_width, self.d_scale_height)), (0, 0))

            self.ui_manager.manager.draw_ui(self.screen)

            pygame.display.update()


if __name__ == '__main__':
    Editor().run()
