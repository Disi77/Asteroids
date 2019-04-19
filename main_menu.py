from draw_text import draw_text
from game_settings import GAME_WINDOW


def menu():
    '''
    Main menu text.
    '''
    draw_text('asteroids',
                  x=100,
                  y=GAME_WINDOW[1] - 100,
                  size=60,
                  anchor_x='left')
    draw_text('in python',
                  x=550,
                  y=GAME_WINDOW[1] - 150,
                  size=16,
                  anchor_x='left')
    draw_text('by   pylady   petra',
                  x=550,
                  y= GAME_WINDOW[1] - 130,
                  size=16,
                  anchor_x='left')
    draw_text('controls:',
                  x=100,
                  y=GAME_WINDOW[1] - 200,
                  size=30,
                  anchor_x='left')
    draw_text('Arrow   keys   ↑   →  ←',
                  x=200,
                  y=GAME_WINDOW[1] - 240,
                  size=16,
                  anchor_x='left')
    draw_text('spacebar',
                  x=200,
                  y=GAME_WINDOW[1] - 260,
                  size=16,
                  anchor_x='left')
    draw_text('press   enter   to   start',
                  x=100,
                  y=GAME_WINDOW[1] - 320,
                  size=30,
                  anchor_x='left')
    draw_text('special thanks to:',
                  x=100,
                  y=80,
                  size=16,
                  anchor_x='left')
    draw_text('Pyladies   ostrava     www . pyladies . cz',
                  x=200,
                  y=55,
                  size=16,
                  anchor_x='left')
    draw_text('Kenney   Vleugels     www . kenney . nl',
                  x=200,
                  y=35,
                  size=16,
                  anchor_x='left')
    draw_text('kjpargeter     www . Freepik . com',
                  x=200,
                  y=15,
                  size=16,
                  anchor_x='left')
