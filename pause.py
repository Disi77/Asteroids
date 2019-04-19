from draw_text import draw_text
from game_settings import GAME_WINDOW


def pause():
    '''
    Pause in game. Some text is drawing in window.
    '''
    draw_text('Pause',
                  x=GAME_WINDOW[0]//2,
                  y=GAME_WINDOW[1]//2,
                  size=50,
                  anchor_x='center')
    draw_text('enter   =   continue',
                  x=GAME_WINDOW[0]//2,
                  y=GAME_WINDOW[1]//2 - 50,
                  size=20,
                  anchor_x='center')
    draw_text('M   =   main  menu  (end  the  game)',
                  x=GAME_WINDOW[0]//2,
                  y=GAME_WINDOW[1]//2 - 80,
                  size=20,
                  anchor_x='center')
