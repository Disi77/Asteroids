import math


import pyglet
from pyglet import gl


from draw_text import draw_text
from main_menu import menu
from game_settings import GAME_WINDOW, ACCELERATION, ROTATION_SPEED, GAME, OBJECTS, time_to_change_level, time_explosion, ufo_in_game
from SpaceObject import SpaceObject, Ufo, Spaceship, Asteroid, Laser, Engine, Life, explosion
from img import GAME_IMG, explosion_image, background_image, life_image, ship_image, batch_front, batch_effects, batch_objects, batch_ufo, batch_explosion
from control import pressed_keys, on_key_press, on_key_release
from pause import pause



def draw_circle(x, y, radius):
    '''
    Draw circle around object in game.
    Serves to determine collision between objects.
    Now is off.
    It can be helpful, when you change the code.
    '''
    iterations = 20
    s = math.sin(2*math.pi / iterations)
    c = math.cos(2*math.pi / iterations)

    dx, dy = radius, 0

    gl.glBegin(gl.GL_LINE_STRIP)
    for i in range(iterations+1):
        gl.glVertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    gl.glEnd()


def background(opacity,color):
    '''
    Set and draw background image in game.
    If the image is smaller than a window,
    it draws the image repeatedly side by side.
    '''
    background = pyglet.sprite.Sprite(background_image)
    x_count = GAME_WINDOW[0] // background.width + 1
    y_count = GAME_WINDOW[1] // background.height + 1
    for x in range(x_count):
        for y in range(y_count):
            background.x = x * background.width
            background.y = y * background.height
            background.color = color
            background.opacity = opacity
            background.draw()


def on_draw():
    '''
    Draw all objects in game.
    '''
    window.clear()
    background(100,(255,255,255))

    # # You have to visible this 2 rows of code, if you can use "draw_circle"
    # for object in OBJECTS:
    #     draw_circle(object.x, object.y, object.radius)

    batch_effects.draw()
    batch_ufo.draw()
    for x_offset in (-window.width, 0, window.width):
        for y_offset in (-window.height, 0, window.height):
            # Remember the current state
            gl.glPushMatrix()
            # Move everything drawn from now on by (x_offset, y_offset, 0)
            gl.glTranslatef(x_offset, y_offset, 0)

            # Draw
            batch_objects.draw()

            # Restore remembered state (this cancels the glTranslatef)
            gl.glPopMatrix()
    draw_text('LIFES',
                  x= 30,
                  y= 15,
                  size=18,
                  anchor_x='left')
    draw_text(str(GAME['score']),
                  x= GAME_WINDOW[0] - 200,
                  y= 15,
                  size=18,
                  anchor_x='left')
    draw_text('LEVEL   ' + str(GAME['level']),
                  x= GAME_WINDOW[0] // 2,
                  y= 15,
                  size=18,
                  anchor_x='center')
    draw_text('enter   =   pause',
                  x= GAME_WINDOW[0] // 2,
                  y= GAME_WINDOW[1] - 20,
                  size=12,
                  anchor_x='center')
    batch_front.draw()

    # Move to the next level
    if GAME['state'] == 'new_level':
        draw_text('LEVEL   ' + str(GAME['level']+1),
                      x= GAME_WINDOW[0] // 2,
                      y= GAME_WINDOW[1] // 2,
                      size=40,
                      anchor_x='center')

    # Settings for drawing explosion image.
    if GAME['state'] == 'ship explosion' or GAME['state'] == 'ufo explosion' or GAME['state'] == 'game_over':
        if 0<time_explosion[0]<1:
            explosion.scale = 0.3*time_explosion[0]
        elif 1<time_explosion[0]<2:
            explosion.scale = 0.3
            explosion.opacity = 255-127.5*time_explosion[0]
        batch_explosion.draw()

    # Main Menu
    if GAME['state'] == 'menu':
        background(255,(200,200,0))
        menu()

    # Pause in game
    if GAME['state'] == 'pause':
        background(100,(200,200,0))
        pause()

    # Game over
    if GAME['state'] == 'game_over':
        draw_text('game   over',
                      x= GAME_WINDOW[0] // 2,
                      y= GAME_WINDOW[1] // 2,
                      size=40,
                      anchor_x='center')
        draw_text('SCORE   =   {}'.format(GAME['score']),
                      x= GAME_WINDOW[0] // 2,
                      y= GAME_WINDOW[1] // 2 - 60,
                      size=20,
                      anchor_x='center')
        draw_text('LEVEL   =   {}'.format(GAME['level']),
                      x= GAME_WINDOW[0] // 2,
                      y= GAME_WINDOW[1] // 2 - 90,
                      size=20,
                      anchor_x='center')


def add_asteroids():
    '''
    Adds asteroids to the game. Higher level = more asteroids.
    '''
    for i in range(1, GAME['level'] + 3):
        OBJECTS.append(Asteroid(0, 0, 0, 0, 1))


def new_game():
    '''
    Restart game conditions.
    '''
    GAME['score'] = 0
    GAME['shield'] = 3
    GAME['level'] = 1

    OBJECTS.clear()
    ufo_in_game[1] = 20

    spaceship1 = Spaceship()
    OBJECTS.append(spaceship1)

    add_asteroids()

    GAME['lifes'] = 3
    for i in range(1,4):
        OBJECTS.append(Life(i))


def new_level():
    '''
    Move to the next level.
    '''
    GAME['level'] +=1
    GAME['shield'] = 3
    GAME['state'] = 'game'
    add_asteroids()


def tick(dt):
    '''
    Restore game conditions every tick.
    '''
    # If Asteroids in game = 0   --->   new level
    asteroid_num_in_game = 0
    for object in OBJECTS:
        if isinstance(object, Asteroid):
            asteroid_num_in_game = 1
    if asteroid_num_in_game == 0:
        GAME['state'] = 'new_level'
        time_to_change_level[0] += dt
        if time_to_change_level[0] > 3:
            new_level()
            time_to_change_level[0] = 0

    # Ufo in game every 20 second. Only one Ufo can be in game in the same time.
    if ufo_in_game[0] == 0 and GAME['state'] == 'game':
        ufo_in_game[1] -= dt
    if ufo_in_game[0] == 0 and ufo_in_game[1] < 0:
        ufo = Ufo()
        OBJECTS.append(ufo)
        ufo_in_game[0] = 1
        ufo_in_game[1] = 20

    # Spaceship explosion
    if GAME['state'] == 'ship explosion':
        time_explosion[0] += dt
        for object in OBJECTS:
            if isinstance(object, Asteroid) or isinstance(object, Life) or isinstance(object, Ufo):
                object.tick(dt)
            else:
                object.sprite.opacity = 0
        if time_explosion[0] > 2:
            time_explosion[0] = 0
            GAME['state'] = 'game'

    # Ufo explosion
    if GAME['state'] == 'ufo explosion':
        time_explosion[0] += dt
        for object in OBJECTS:
            if isinstance(object, Asteroid) or isinstance(object, Life) or isinstance(object, Spaceship) or isinstance(object, Laser):
                object.tick(dt)
            else:
                object.sprite.opacity = 0
        if time_explosion[0] > 2:
            time_explosion[0] = 0
            GAME['state'] = 'game'

    # Game over = Spaceship explosion. Go to the main menu. Restart game conditions.
    if GAME['state'] == 'game_over':
        time_explosion[0] += dt
        for object in OBJECTS:
            if isinstance(object, Asteroid) or isinstance(object, Life) or isinstance(object, Ufo):
                object.tick(dt)
            else:
                object.sprite.opacity = 0
        if time_explosion[0] > 5:
            time_explosion[0] = 0
            GAME['state'] = 'menu'


    # If state is game or new level is starting, all abject in game still moving.
    if GAME['state'] == 'game' or GAME['state'] == 'new_level':
        for object in OBJECTS:
            object.tick(dt)

    # Main menu and user press ENTER
    if GAME['state'] == 'menu':
        if ('enter', 0) in pressed_keys:
            pressed_keys.clear()
            GAME['state'] = 'game'
            new_game()

    # Game and user press ENTER
    if GAME['state'] == 'game':
        if ('enter', 0) in pressed_keys:
            pressed_keys.clear()
            GAME['state'] = 'pause'

    # Pause and user press ENTER
    if GAME['state'] == 'pause':
        if ('enter', 0) in pressed_keys:
            pressed_keys.clear()
            GAME['state'] = 'game'

    # Pause and user press M and go to the Main menu
    if GAME['state'] == 'pause':
        if ('M', 0) in pressed_keys:
            pressed_keys.clear()
            GAME['state'] = 'menu'


window = pyglet.window.Window(GAME_WINDOW[0],GAME_WINDOW[1])


new_game()


window.push_handlers(
    on_draw=on_draw,
    on_key_press=on_key_press,
    on_key_release=on_key_release,
)


pyglet.clock.schedule_interval(tick, 1/30)


pyglet.app.run()
