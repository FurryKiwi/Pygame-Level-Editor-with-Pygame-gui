import pygame
import pygame_gui as gui
import os
from Scripts.settings import *

BUTTON_SIZE = (80, 30)
DROP_DOWN_MENU = (135, 30)
LABEL_OFFSET = 150, 30


class UIApp:

    def __init__(self, editor, parent_size, size):
        self.editor = editor
        self.parent_size = parent_size
        self.size = size
        self.top_left = (parent_size[0] - size[0], 0)
        self.center_screen = (parent_size[0] // 2, parent_size[1] // 2)
        path = os.path.join(os.getcwd(), "Scripts", "pg_gui_elements", "theme.json")
        self.manager = gui.UIManager(parent_size, path, enable_live_theme_updates=False)

        self.panel = gui.elements.UIPanel(relative_rect=pygame.Rect(self.top_left, size), manager=self.manager)

        # Main UI panel elements
        self.file_dialog = None
        self.fps_counter = None
        self.load_map_button = None
        self.save_map_button = None
        self.map_label = None
        self.layer_label = None
        self.size_label = None
        self.create_map_button = None
        self.auto_tile_label = None
        self.on_grid_label = None
        self.layers_properties_button = None
        self.tiles_properties_button = None
        # Save window elements
        self.save_window = None
        self.text_entry = None
        self.path_button = None
        self.save_map_dialog = None
        # Tile sets window and elements
        self.tilesets_panel = None
        self.tiles_dropdown = None
        self.scroll_bar = None
        # Create new window elements
        self.create_new_dialog = None
        # Layers properties window elements
        self.layers_window = None
        # Tile properties window elements
        self.tile_pro_window = None

        self.map_paths = MAP_PATHS

        # To disable all buttons and drop down menus
        self.all_buttons = []

        # Stores all UI.Image objects
        self.tile_images = {}

        self.selected_tile = 0

    def create_ui(self):
        # Labels ______________________________________________________________________________________________
        self.fps_counter = gui.elements.UILabel(
            relative_rect=pygame.Rect((self.size[0] - LABEL_OFFSET[0], 0), (-1, 20)),
            text="FPS: ", manager=self.manager, object_id='#fps_counter',
            container=self.panel)
        self.layer_label = gui.elements.UILabel(
            relative_rect=pygame.Rect((self.size[0] - LABEL_OFFSET[0], 0), (-1, 20)),
            text=f"Layer: {self.editor.tilemap.current_layer}",
            manager=self.manager, object_id='#layer_label',
            container=self.panel, anchors={'top': 'top',
                                           'left': 'left',
                                           'bottom': 'top',
                                           'right': 'left',
                                           'top_target': self.fps_counter})
        self.size_label = gui.elements.UILabel(relative_rect=pygame.Rect((self.size[0] - LABEL_OFFSET[0], 0), (-1, 20)),
                                               text=f"Size: {self.editor.tilemap.brush_size}", manager=self.manager,
                                               object_id='#size_label',
                                               container=self.panel, anchors={'top': 'top',
                                                                              'left': 'left',
                                                                              'bottom': 'top',
                                                                              'right': 'left',
                                                                              'top_target': self.layer_label})
        self.auto_tile_label = gui.elements.UILabel(
            relative_rect=pygame.Rect((self.size[0] - LABEL_OFFSET[0], 0), (-1, 20)),
            text=f"Autotile: {self.editor.auto_tile}", manager=self.manager,
            object_id='#autotile_label',
            container=self.panel, anchors={'top': 'top',
                                           'left': 'left',
                                           'bottom': 'top',
                                           'right': 'left',
                                           'top_target': self.size_label})
        self.on_grid_label = gui.elements.UILabel(
            relative_rect=pygame.Rect((self.size[0] - LABEL_OFFSET[0], 0), (-1, 20)),
            text=f"On_Grid: {self.editor.ongrid}",
            manager=self.manager, object_id='#on_grid_label',
            container=self.panel, anchors={'top': 'top',
                                           'left': 'left',
                                           'bottom': 'top',
                                           'right': 'left',
                                           'top_target': self.auto_tile_label})
        self.map_label = gui.elements.UILabel(relative_rect=pygame.Rect((self.size[0] - LABEL_OFFSET[0], 0), (-1, 20)),
                                              text=f"Map: {self.editor.tilemap.current_map}", manager=self.manager,
                                              object_id='#map_label',
                                              container=self.panel, anchors={'top': 'top',
                                                                             'left': 'left',
                                                                             'bottom': 'bottom',
                                                                             'right': 'right',
                                                                             'top_target': self.on_grid_label})
        # Buttons _____________________________________________________________________________________________
        self.create_map_button = gui.elements.UIButton(
            relative_rect=pygame.Rect((5, 3), BUTTON_SIZE),
            object_id=gui.core.ObjectID(class_id='@buttons', object_id='#buttons'),
            text='Create', manager=self.manager, container=self.panel, anchors={'top': 'top',
                                                                                'left': 'left',
                                                                                'bottom': 'top',
                                                                                'right': 'left'})
        self.all_buttons.append(self.create_map_button)
        self.load_map_button = gui.elements.UIButton(
            relative_rect=pygame.Rect((5, 3), BUTTON_SIZE),
            object_id=gui.core.ObjectID(class_id='@buttons', object_id='#buttons'),
            text='Load', manager=self.manager, container=self.panel, anchors={'top': 'top',
                                                                              'left': 'left',
                                                                              'bottom': 'top',
                                                                              'right': 'left',
                                                                              'left_target': self.create_map_button})
        self.all_buttons.append(self.load_map_button)

        self.save_map_button = gui.elements.UIButton(
            relative_rect=pygame.Rect((5, 3), BUTTON_SIZE),
            text='Save', manager=self.manager, container=self.panel,
            object_id=gui.core.ObjectID(class_id='@buttons', object_id='#buttons'),
            anchors={'top': 'top',
                     'left': 'left',
                     'bottom': 'top',
                     'right': 'left',
                     'left_target': self.load_map_button})
        self.all_buttons.append(self.save_map_button)
        # Tilesets Window ____________________________________________________________________________________
        self.tilesets_panel = gui.elements.UIPanel(pygame.Rect((5, 151), (self.size[0] - 16, self.size[1] - 490)),
                                                   manager=self.manager, container=self.panel)
        tilesets = [i for i in self.editor.assets if i != 'background']
        self.tiles_dropdown = gui.elements.UIDropDownMenu(tilesets, starting_option=tilesets[0],
                                                          relative_rect=pygame.Rect((5, 118), DROP_DOWN_MENU),
                                                          manager=self.manager, container=self.panel,
                                                          object_id=gui.core.ObjectID(class_id='@dropdown',
                                                                                      object_id='#dropdown'),
                                                          anchors={'top': 'top',
                                                                   'left': 'left',
                                                                   'bottom': 'bottom',
                                                                   'right': 'right'},
                                                          expansion_height_limit=130)
        self.all_buttons.append(self.tiles_dropdown)
        self.create_tile_layout()

        self.layers_properties_button = gui.elements.UIButton(
            relative_rect=pygame.Rect((5, 3), BUTTON_SIZE),
            text='Layers', manager=self.manager, container=self.panel,
            object_id=gui.core.ObjectID(class_id='@buttons', object_id='#buttons'),
            anchors={'top': 'top',
                     'left': 'left',
                     'bottom': 'top',
                     'right': 'left',
                     'left_target': self.save_map_button})
        self.all_buttons.append(self.layers_properties_button)
        self.tiles_properties_button = gui.elements.UIButton(
            relative_rect=pygame.Rect((5, 3), BUTTON_SIZE),
            text='Tiles', manager=self.manager, container=self.panel,
            object_id=gui.core.ObjectID(class_id='@buttons', object_id='#buttons'),
            anchors={'top': 'top',
                     'left': 'left',
                     'bottom': 'top',
                     'right': 'left',
                     'left_target': self.layers_properties_button})
        self.all_buttons.append(self.tiles_properties_button)

        self.layers_window = LayerProperties(self)
        self.tile_pro_window = TileProperties(self)

    def show_fps(self, fps):
        self.fps_counter.set_text(f'FPS: {fps:.2f}')

    def get_current_tile(self):
        return self.tiles_dropdown.selected_option, self.selected_tile

    def get_tile_settings(self):
        return self.tile_pro_window.current_settings

    def get_center_of_element(self, size):
        return self.center_screen[0] - (size[0] // 2), self.center_screen[1] - (size[1] // 2)

    def create_file_dialog(self, text, obj_id):
        center = self.get_center_of_element((500, 300))
        self.file_dialog = gui.windows.UIFileDialog(pygame.Rect(center, (500, 300)),
                                                    manager=self.manager,
                                                    window_title=text, allow_picking_directories=True,
                                                    allow_existing_files_only=True,
                                                    object_id=obj_id, initial_file_path='data/maps')

    def create_save_window(self):
        center = self.get_center_of_element((500, 200))
        self.save_window = gui.elements.UIWindow(pygame.Rect(center, (500, 200)),
                                                 window_display_title="Set Path for Saving",
                                                 manager=self.manager, draggable=False)
        current_map = self.map_paths + self.editor.tilemap.current_map
        self.text_entry = gui.elements.UITextEntryLine(pygame.Rect((0, 0), (250, 50)),
                                                       manager=self.manager,
                                                       container=self.save_window, initial_text=current_map,
                                                       anchors={'centerx': 'centerx'}
                                                       )
        self.path_button = gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), BUTTON_SIZE),
                                                 text='Save', manager=self.manager, container=self.save_window,
                                                 object_id=gui.core.ObjectID(class_id='@buttons', object_id='#buttons'),
                                                 anchors={'centerx': 'centerx',
                                                          'top_target': self.text_entry})

    def create_tile_layout(self):
        for i in self.tile_images.values():
            i.kill()
        self.tile_images = {}
        self.selected_tile = 0
        rect = self.tilesets_panel.get_relative_rect()
        size = (rect[2], rect[3])

        cur_tileset = self.tiles_dropdown.selected_option

        if cur_tileset != 'large_decor':
            tile_size = self.editor.assets[cur_tileset][0].get_size()
            region_x = size[0] // (tile_size[0] * 2 + tile_size[0])
            region_y = size[1] // (tile_size[1] * 2 + tile_size[1])
            count_of_tiles = len(self.editor.assets[cur_tileset])
            if region_x > count_of_tiles:
                region_x -= count_of_tiles
            if region_y > count_of_tiles:
                region_y = 1
            x, y = 0, 0
            for index, tile in enumerate(self.editor.assets[cur_tileset]):
                if x >= region_x:
                    y += 1
                    if y > region_y:
                        break
                    x = 0
                scaled_image = pygame.transform.scale2x(tile)
                new_tile = gui.elements.UIImage(pygame.Rect(((x * (tile_size[0] * 2 + tile_size[0])) + tile_size[0],
                                                             y * (tile_size[1] * 2 + tile_size[1]) + tile_size[1]),
                                                            (scaled_image.get_size())), scaled_image,
                                                manager=self.manager,
                                                image_is_alpha_premultiplied=False, container=self.tilesets_panel)
                self.tile_images.update({index: new_tile})
                x += 1
        else:
            # TODO: This will have to get re-written in the future to account for many different size images in a
            #  folder and space them out accordingly. For now, this is fine.
            # count_of_tiles = len(self.editor.assets[cur_tileset])
            space_between_x = 32
            space_between_y = 16
            # region_x = size[0]
            # region_y = size[1]
            x, y = 0, 0
            last_tile_size = 0
            for index, tile in enumerate(self.editor.assets[cur_tileset]):
                tile_size = tile.get_size()[0]
                scaled_image = pygame.transform.scale2x(tile)
                scaled_size = scaled_image.get_size()
                new_tile = gui.elements.UIImage(pygame.Rect(((x * (tile_size + space_between_x)) + last_tile_size,
                                                             y + space_between_y),
                                                            scaled_size),
                                                scaled_image, manager=self.manager,
                                                image_is_alpha_premultiplied=False, container=self.tilesets_panel)

                self.tile_images.update({index: new_tile})
                last_tile_size = tile_size
                x += 1

        first_image = self.tile_images[0]
        self.update_selected(0, first_image)

    def setup_elements(self):
        layers = self.editor.tilemap.get_layers()
        if layers:
            self.layers_window.layer_selection_element.set_item_list(layers)
        else:
            self.layers_window.layer_selection_element.set_item_list(['0'])
        self.layers_window.switch_layer('0')

        self.layers_window.player_layer_label.set_text(f'Player Layer: {self.editor.tilemap.player_layer}')

        self.update_labels()

    def create_new(self):
        self.editor.tilemap.create_new()
        self.setup_elements()
        self.update_labels()

    def load_map(self, path):
        ext = os.path.splitext(path)[1]
        if ext != '.json':
            # TODO: Add Logger here
            print("ERROR: Filename can't be loaded.")
            return None

        self.editor.tilemap.load(path)
        self.setup_elements()

    def save_map(self, path):
        ext = os.path.splitext(path)[1]
        if ext != '.json':
            # TODO: Add Logger here
            print("ERROR: Cant save a none extension path file. Need to add '.json' to end of filename.")
            return None
        center = self.get_center_of_element((260, 200))
        self.save_map_dialog = gui.windows.UIConfirmationDialog(pygame.Rect(center, (260, 200)),
                                                                action_long_desc="Save New Map! Is the name correct?",
                                                                manager=self.manager, window_title="Confirm")

    def disable_all_buttons(self):
        for b in self.all_buttons:
            b.disable()

    def enable_all_buttons(self):
        for b in self.all_buttons:
            b.enable()

    def update_labels(self):
        self.layer_label.set_text(f"Layer: {self.editor.tilemap.current_layer}")
        self.size_label.set_text(f"Size: {self.editor.tilemap.brush_size}")
        self.auto_tile_label.set_text(f"Autotile: {self.editor.auto_tile}")
        self.on_grid_label.set_text(f"On_Grid: {self.editor.ongrid}")
        self.map_label.set_text(f"Map: {self.editor.tilemap.current_map}")

    def update_selected(self, variant, image):
        if self.selected_tile is None:
            self.selected_tile = variant
            pygame.draw.rect(image.image, (255, 0, 0), (0, 0, image.rect[2], image.rect[3]), width=1)
        else:
            old_image = self.tile_images[self.selected_tile]
            replace_image = self.editor.assets[self.tiles_dropdown.selected_option][self.selected_tile]
            scaled_image = pygame.transform.scale2x(replace_image)
            old_image.set_image(scaled_image)

            self.selected_tile = variant
            pygame.draw.rect(image.image, (255, 0, 0), (0, 0, image.rect[2], image.rect[3]), width=1)

    def process_events(self, event, mpos):
        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.load_map_button:
                self.create_file_dialog("Load Map", "loadmaps")
                self.disable_all_buttons()
            elif event.ui_element == self.save_map_button:
                self.create_save_window()
                self.disable_all_buttons()
            elif event.ui_element == self.path_button:
                self.save_map(self.text_entry.get_text())
            elif event.ui_element == self.create_map_button:
                center = self.get_center_of_element((500, 200))
                self.create_new_dialog = gui.windows.UIConfirmationDialog(
                    pygame.Rect(center, (500, 200)),
                    action_long_desc="Create New Map! Have you saved?",
                    manager=self.manager, window_title="Confirm")
            elif event.ui_element == self.layers_properties_button:
                self.layers_window.set_position((self.top_left[0] - 5, 555))

            elif event.ui_element == self.tiles_properties_button:
                self.tile_pro_window.set_position((self.top_left[0] + 280, 555))

        if event.type == gui.UI_FILE_DIALOG_PATH_PICKED:
            if event.ui_element == self.file_dialog:
                if self.file_dialog.object_ids[0] == 'loadmaps':
                    self.load_map(event.text)

        if event.type == gui.UI_WINDOW_CLOSE:
            if event.ui_element == self.file_dialog or event.ui_element == self.save_window:
                self.enable_all_buttons()
                self.file_dialog = None

        if event.type == gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            if event.ui_element == self.create_new_dialog:
                self.create_new()
            if event.ui_element == self.save_map_dialog:
                self.editor.tilemap.save(self.text_entry.get_text())
                self.update_labels()
                self.save_window.kill()

        if event.type == gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.tiles_dropdown:
                self.create_tile_layout()

        if event.type == pygame.MOUSEBUTTONDOWN and self.tilesets_panel.is_focused:
            if event.button == 1:
                for var, image in self.tile_images.items():
                    if image.rect.collidepoint(mpos):
                        self.update_selected(var, image)
        if self.layers_window:
            self.layers_window.process_events(event, mpos)
        if self.tile_pro_window:
            self.tile_pro_window.process_events(event, mpos)
        self.manager.process_events(event)


class TileProperties(gui.elements.UIWindow):
    _options = ["True", "False"]
    _drop_down_size = (80, 30)

    def __init__(self, ui_app):
        self.ui_app = ui_app
        self.manager = self.ui_app.manager
        self.editor = self.ui_app.editor
        self.top_left = self.ui_app.top_left
        rect = pygame.Rect((self.ui_app.top_left[0] + 280, 555), (305, 350))
        gui.elements.UIWindow.__init__(self, rect, manager=self.manager, window_display_title="Tile Properties",
                                       resizable=True, draggable=True)
        self.close_window_button = False

        self.interaction_dropdown = None

        self.current_settings = {'interaction': False}

        self.create_ui()

    def create_ui(self):
        # Labels _____________________________________________________________________________________
        interaction_label = gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 30), (-1, 20)),
            text="Interaction: ", manager=self.manager,
            container=self, anchors={'top': 'top',
                                     'left': 'left',
                                     'bottom': 'top',
                                     'right': 'left'})

        # Drop down ___________________________________________________________________________________________
        self.interaction_dropdown = gui.elements.UIDropDownMenu(self._options, starting_option=self._options[1],
                                                                relative_rect=pygame.Rect((170, 25),
                                                                                          self._drop_down_size),
                                                                manager=self.manager, container=self,
                                                                object_id=gui.core.ObjectID(class_id='@dropdown',
                                                                                            object_id='#dropdown'),
                                                                anchors={'top': 'top',
                                                                         'left': 'left',
                                                                         'bottom': 'top',
                                                                         'right': 'left'},
                                                                expansion_height_limit=130)

    def process_events(self, event, mpos):
        if event.type == gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.interaction_dropdown:
                selection = self.interaction_dropdown.selected_option
                self.current_settings['interaction'] = selection


class LayerProperties(gui.elements.UIWindow):

    def __init__(self, ui_app):
        self.ui_app = ui_app
        self.manager = self.ui_app.manager
        self.editor = self.ui_app.editor
        self.top_left = self.ui_app.top_left

        self.player_layer_button = None
        self.player_layer_label = None

        self.add_layer_button = None
        self.delete_layer_button = None
        self.layer_selection_element = None

        self.shift = False

        rect = pygame.Rect((self.top_left[0] - 5, 555), (305, 350))
        gui.elements.UIWindow.__init__(self, rect, manager=self.manager, window_display_title="Layer Properties",
                                       resizable=True, draggable=True)
        self.close_window_button = False
        self.set_minimum_dimensions((298, 350))
        self.create_ui()

    def create_ui(self):
        # Player layer elements
        self.player_layer_button = gui.elements.UIButton(relative_rect=pygame.Rect((5, 5), BUTTON_SIZE),
                                                         manager=self.manager, container=self, text="Set",
                                                         anchors={'top': 'top',
                                                                  'left': 'left',
                                                                  'bottom': 'top',
                                                                  'right': 'left'})

        self.player_layer_label = gui.elements.UILabel(relative_rect=pygame.Rect((30, 8), (-1, -1)),
                                                       manager=self.manager,
                                                       container=self,
                                                       text=f'Player Layer: {self.editor.tilemap.player_layer}',
                                                       anchors={'top': 'top',
                                                                'left': 'left',
                                                                'bottom': 'top',
                                                                'right': 'left',
                                                                'left_target': self.player_layer_button})

        # Buttons
        self.add_layer_button = gui.elements.UIButton(
            relative_rect=pygame.Rect((5, 13), BUTTON_SIZE),
            object_id=gui.core.ObjectID(class_id='@buttons', object_id='#buttons'),
            text='Add', manager=self.manager, container=self,
            anchors={'top': 'top',
                     'left': 'left',
                     'bottom': 'top',
                     'right': 'left',
                     'top_target': self.player_layer_label})
        self.delete_layer_button = gui.elements.UIButton(
            relative_rect=pygame.Rect((5, 13), BUTTON_SIZE),
            object_id=gui.core.ObjectID(class_id='@buttons', object_id='#buttons'),
            text='Delete', manager=self.manager, container=self,
            anchors={'top': 'top',
                     'left': 'left',
                     'bottom': 'top',
                     'right': 'left',
                     'left_target': self.add_layer_button,
                     'top_target': self.player_layer_label})
        # Selection List
        self.layer_selection_element = gui.elements.UISelectionList(relative_rect=pygame.Rect((5, 3), (165, 210)),
                                                                    manager=self.manager,
                                                                    container=self,
                                                                    item_list=["0"],
                                                                    starting_height=20,
                                                                    anchors={'top': 'top',
                                                                             'bottom': 'bottom',
                                                                             'left': 'left',
                                                                             'right': 'right',
                                                                             'top_target': self.add_layer_button},
                                                                    parent_element=self)

    def add_layer(self):
        if len(self.layer_selection_element.item_list) == 10:
            print("INFO: Can only have 10 layers currently.")
            return
        last_item = self.layer_selection_element.item_list[-1]
        new_item = int(last_item['text']) + 1
        self.layer_selection_element.add_items([str(new_item)])
        self.switch_layer('0')
        self.editor.tilemap.add_layer(new_item)

    def delete_layer(self):
        selection = self.layer_selection_element.get_single_selection()
        if selection == '0' or selection is None:
            return
        self.editor.tilemap.delete_layer(selection)
        self.layer_selection_element.remove_items([selection])
        self.switch_layer('-1', direction='delete')

    def switch_layer(self, layer: str, direction='reset'):
        # If item was deleted reset back to the first item
        if direction == 'reset':
            item = self.layer_selection_element.item_list[0]
            item['selected'] = True
            item['button_element'].select()
            self.editor.tilemap.change_layer(item['text'])
            self.ui_app.update_labels()
        elif direction == 'delete':
            item = self.layer_selection_element.item_list[-1]
            item['selected'] = True
            item['button_element'].select()
            self.editor.tilemap.change_layer(item['text'])
            self.ui_app.update_labels()
        elif direction == 'clicked':
            for index, item in enumerate(self.layer_selection_element.item_list):
                if item['text'] == layer:
                    item['selected'] = True
                    item['button_element'].select()
                    self.editor.tilemap.change_layer(item['text'])
                    self.ui_app.update_labels()
        elif direction == 'up':
            for index, item in enumerate(self.layer_selection_element.item_list):
                if item['text'] == layer:
                    new_index = index + 1
                    try:
                        new_item = self.layer_selection_element.item_list[new_index]
                        new_item['button_element'].select()
                        new_item['selected'] = True
                        item['selected'] = False
                        item['button_element'].unselect()
                        self.editor.tilemap.change_layer(new_item['text'])
                        self.ui_app.update_labels()
                    except (IndexError, AttributeError):
                        return
        elif direction == 'down':
            for index, item in enumerate(self.layer_selection_element.item_list):
                if item['text'] == layer:
                    new_index = index - 1
                    if new_index < 0:
                        return
                    try:
                        new_item = self.layer_selection_element.item_list[new_index]
                        new_item['button_element'].select()
                        new_item['selected'] = True
                        item['selected'] = False
                        item['button_element'].unselect()

                        self.editor.tilemap.change_layer(new_item['text'])
                        self.ui_app.update_labels()
                    except (IndexError, AttributeError):
                        return

    def process_events(self, event, mpos):
        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.add_layer_button:
                self.add_layer()

            elif event.ui_element == self.delete_layer_button:
                self.delete_layer()

            elif event.ui_element == self.player_layer_button:
                selected = self.layer_selection_element.get_single_selection()
                self.editor.tilemap.change_player_layer(selected)
                self.player_layer_label.set_text(f'Player Layer: {self.editor.tilemap.player_layer}')

        if event.type == gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self.layer_selection_element:
                self.switch_layer(self.layer_selection_element.get_single_selection(), direction="clicked")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                self.shift = False

        if event.type == pygame.KEYDOWN and pygame.mouse.get_focused():
            if event.key == pygame.K_LSHIFT:
                self.shift = True

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused():
            # Mouse wheel for going up layers and up brush sizes
            if self.shift:
                if event.button == 4:
                    layer = self.layer_selection_element.get_single_selection()
                    self.switch_layer(layer, "up")

                if event.button == 5:
                    layer = self.layer_selection_element.get_single_selection()
                    self.switch_layer(layer, "down")
