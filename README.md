# Pygame-Level-Editor-with-Pygame-gui
A simple level editor/creator made with pygame and pygame-gui. Has built in brush sizes and auto-tiling.

I built this more to see how auto-tiling worked and how it's implemented. 
I decided to put it up here for educational purposes for anyone wanting to learn how others have built basic level editors when their creating their games and for those that don't want to use a game engine and instead build all their own tools.

To start using the editor, you'll have to edit the settings.py file and setup your folder directory with all your assets you'll be using to build your levels.
If you use tilesetter for generating blobset tilesets, this works out of the box for the json export from tile setter. Wang tilesets I haven't looked into yet so I don't know if those will work.

![Capture](https://github.com/FurryKiwi/Pygame-Level-Editor-with-Pygame-gui/assets/104323989/a134350f-ab5d-458e-9ab2-d395d8fe2210)

Make sure when exporting the tileset from Tilesetter that you only select the tiles you want otherwise the json file that gets exported with it might be messed up. (Haven't fully tested but just to be safe)
![Capture1](https://github.com/FurryKiwi/Pygame-Level-Editor-with-Pygame-gui/assets/104323989/ccce1ce0-3034-4a29-acbf-8f87abaa59dd)
