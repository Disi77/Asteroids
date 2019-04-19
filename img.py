import pyglet
from pathlib import Path


# Loading images for game
batch_objects = pyglet.graphics.Batch()
batch_effects = pyglet.graphics.Batch()
batch_front = pyglet.graphics.Batch()
batch_ufo = pyglet.graphics.Batch()
batch_explosion = pyglet.graphics.Batch()


ship_image = pyglet.image.load('PNG/playerShip2_blue.png')
ship_image.anchor_x = ship_image.width // 2
ship_image.anchor_y = ship_image.height // 2


ufo_image = pyglet.image.load('PNG/ufoRed.png')
ufo_image.anchor_x = ufo_image.width // 2
ufo_image.anchor_y = ufo_image.height // 2


life_image = pyglet.image.load('PNG/UI/playerLife2_blue.png')
life_image.anchor_x = life_image.width // 2
life_image.anchor_y = life_image.height // 2


background_image = pyglet.image.load('PNG/Backgrounds/space3.jpg')


explosion_image = pyglet.image.load('PNG/Explosion/Orange Explosion/explosion00.png')
explosion_image.anchor_x = explosion_image.width // 2
explosion_image.anchor_y = explosion_image.height // 2


TILES_DIRECTORY = Path('PNG/Meteors')

GAME_IMG = {}
for path in TILES_DIRECTORY.glob('*.png'):
    GAME_IMG[path.stem] = pyglet.image.load(path)

TILES_DIRECTORY = Path('PNG/Lasers')
for path in TILES_DIRECTORY.glob('*.png'):
    GAME_IMG[path.stem] = pyglet.image.load(path)

TILES_DIRECTORY = Path('PNG/Effects')
for path in TILES_DIRECTORY.glob('*.png'):
    GAME_IMG[path.stem] = pyglet.image.load(path)

for title, image in GAME_IMG.items():
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2
