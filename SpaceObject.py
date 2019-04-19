import math
from random import choice, randrange


import pyglet


from game_settings import GAME_WINDOW, GAME, OBJECTS, ROTATION_SPEED, ACCELERATION, ufo_in_game
from img import GAME_IMG, explosion_image, life_image, ship_image, ufo_image, batch_front, batch_effects, batch_objects, batch_ufo, batch_explosion
from control import pressed_keys
from overlaps import overlaps


explosion = pyglet.sprite.Sprite(explosion_image, batch=batch_explosion)


class SpaceObject:
    '''
    Superclass for all objects in game.
    '''
    def __init__(self):
        self.x
        self.y
        self.rotation
        self.x_speed
        self.y_speed
        self.sprite
        self.radius = min(self.sprite.width, self.sprite.height)//2

    def tick(self, dt):
        '''
        Definicion the basics of movement.
        '''
        self.x = self.x + dt * self.x_speed
        self.y = self.y + dt * self.y_speed

        # If the object is out of the window, it returns to teh other side.
        if self.x > GAME_WINDOW[0]:
            self.x = self.x - GAME_WINDOW[0]
        if self.x < 0:
            self.x = self.x + GAME_WINDOW[0]
        if self.y > GAME_WINDOW[1]:
            self.y = self.y - GAME_WINDOW[1]
        if self.y < 0:
            self.y = self.y + GAME_WINDOW[1]

        # Inserts the coordinates and rotation to the sprite.
        self.sprite.rotation = 90 - math.degrees(self.rotation)
        self.sprite.x = self.x
        self.sprite.y = self.y

    def delete_object(self):
        '''
        Deleting the object from list "objects"
        '''
        del OBJECTS[OBJECTS.index(self)]
        self.sprite.delete()

    def explosion(self, type):
        '''
        Explosion - for Spaceship or Ufo.
        '''
        GAME['state'] = type
        explosion.scale = 0.000001
        explosion.opacity = 255
        explosion.x = self.x
        explosion.y = self.y


class Ufo(SpaceObject):
    '''
    Ufo (Enemy) class.
    '''
    def __init__(self):
        # Find Spaceship in game and copy its coordinates for set own movement.
        for object in OBJECTS:
            if isinstance(object, Spaceship):
                ship_x = object.x
                ship_y = object.y

        if 0 < ship_x < GAME_WINDOW[0]//2:
            self.x = GAME_WINDOW[0] + 50
        else:
            self.x = 0 - 50
        if 0 < ship_y < GAME_WINDOW[1]//2:
            self.y = randrange(GAME_WINDOW[1]//2, GAME_WINDOW[1])
        else:
            self.y = randrange(0, GAME_WINDOW[1]//2)

        self.sprite = pyglet.sprite.Sprite(ufo_image, self.x, self.y, batch=batch_ufo)
        self.rotation = 0

        x = (ship_x - self.x)
        y = (ship_y - self.y)
        speed = abs(100 / x)

        self.x_speed = speed * x
        self.y_speed = speed * y

        self.laser_available = 3  # For the firt time, Ufo can fire after 3 seconds
        super().__init__()

    def tick(self, dt):
        self.rotation = self.rotation + dt * (+ ROTATION_SPEED//2)
        self.x = self.x + dt * self.x_speed
        self.y = self.y + dt * self.y_speed
        self.sprite.rotation = 90 - math.degrees(self.rotation)
        self.sprite.x = self.x
        self.sprite.y = self.y

        # Delete Ufo, if is out of game window
        if self.x_speed < 0 and self.y_speed < 0:
            if self.x < -50 or self.y < -50:
                self.delete_object()
                ufo_in_game[0] = 0
        if self.x_speed < 0 and self.y_speed > 0:
            if self.x < -50 or self.y > GAME_WINDOW[1]+50:
                self.delete_object()
                ufo_in_game[0] = 0
        if self.x_speed > 0 and self.y_speed < 0:
            if self.x > GAME_WINDOW[0]+50 or self.y < -50:
                self.delete_object()
                ufo_in_game[0] = 0
        if self.x_speed > 0 and self.y_speed > 0:
            if self.x > GAME_WINDOW[0]+50 or self.y > GAME_WINDOW[1]+50:
                self.delete_object()
                ufo_in_game[0] = 0

        # If is Laser Available, Ufo shoots
        self.laser_available -= dt
        if self.laser_available < 0:
            OBJECTS.append(Laser(self.x, self.y, self.x_speed, self.y_speed, self.rotation, 2))
            self.laser_available = 1  # Ufo can fire every 1 second


class Spaceship(SpaceObject):
    '''
    Spaceship class.
    '''
    def __init__(self):
        self.x = GAME_WINDOW[0]//2
        self.y = GAME_WINDOW[1]//2
        self.sprite = pyglet.sprite.Sprite(ship_image, self.x, self.y, batch=batch_objects)
        self.x_speed = 0
        self.y_speed = 0
        self.laser_available = 0.1
        self.rotation = math.pi/2
        OBJECTS.append(Engine())  # Every Spaceship has own Engine
        super().__init__()

    def tick(self, dt):
        # User press arrow keys up, left or right
        if ('up', 0) in pressed_keys:
            self.x_speed += dt * ACCELERATION * math.cos(self.rotation)
            self.y_speed += dt * ACCELERATION * math.sin(self.rotation)
        if ('left', 0) in pressed_keys:
            self.rotation = self.rotation + dt * (+ ROTATION_SPEED)
        if ('right', 0) in pressed_keys:
            self.rotation = self.rotation + dt * (- ROTATION_SPEED)

        # If Laser available, User can fire by pressing enter
        self.laser_available -= dt
        if ('fire', 0) in pressed_keys and self.laser_available < 0:
            OBJECTS.append(Laser(self.x, self.y, self.x_speed, self.y_speed, self.rotation, 1))
            self.laser_available = 0.3

        # If Spaceship has Shield, the Ship is flashing
        GAME['shield'] -= dt
        i = GAME['shield']
        if i > 0:
            if 3 > i > 2.5 or 2 > i > 1.5 or 1 > i > 0.5:
                self.sprite.opacity = 150
            else:
                self.sprite.opacity = 50
        else:
            self.sprite.opacity = 255

        for object in OBJECTS:
            # If Asteriod overlaps with Spaceship and Shield is off
            if isinstance(object, Asteroid) and overlaps(object, self) and GAME['shield'] < 0:
                if object.level in [1]:
                    for i in range(2):
                        OBJECTS.append(Asteroid(object.x, object.y, object.x_speed, object.y_speed, object.level + 1))
                object.delete_object()
                self.hit_by_spaceship()

            # Engine is on, when User press UP and copy the Spaceship's movement.
            if isinstance(object, Engine) and ('up', 0) in pressed_keys:
                object.sprite.opacity = 255
                object.x = self.x - math.cos(self.rotation) * 60
                object.y = self.y - math.sin(self.rotation) * 60
                object.x_speed = self.x_speed
                object.y_speed = self.y_speed
                object.rotation = self.rotation
            # Else Engine is off.
            if isinstance(object, Engine) and ('up', 0) not in pressed_keys:
                object.sprite.opacity = 0
        super().tick(dt)

    def hit_by_spaceship(self):
        '''
        Collision of the ship and asteroid.
        '''
        self.explosion('ship explosion')
        self.sprite.opacity = 0
        for object in OBJECTS:
            if isinstance(object, Life) and object.rank == GAME['lifes']:
                object.delete_object()
                GAME['lifes'] -= 1
                GAME['shield'] = 3
        if GAME['lifes'] == 0:
            GAME['state'] = 'game_over'
        else:
            self.restart_spaceship()

    def restart_spaceship(self):
        '''
        Restart Spaceship after collision.
        '''
        self.x = GAME_WINDOW[0]//2
        self.y = GAME_WINDOW[1]//2
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = math.pi/2
        pressed_keys.clear()


class Engine(SpaceObject):
    '''
    Engine (for Spaceship) class.
    '''
    def __init__(self):
        self.rotation = 0
        self.x = 0
        self.y = 0
        self.x_speed = 0
        self.y_speed = 0
        self.sprite = pyglet.sprite.Sprite(GAME_IMG['fire01'], self.x, self.x, batch=batch_effects)
        self.sprite.scale = 2
        super().__init__()


class Asteroid(SpaceObject):
    '''
    Asteroid class.
    '''
    def __init__(self, x, y, x_speed, y_speed, level):
        # New level = coordinates of Asteroid is at the edge of the window.
        if x == 0 and y == 0:
            if choice([0, 1]) == 0:
                self.x, self.y = 0, choice(range(100, GAME_WINDOW[1]+1, 100))
            else:
                self.y, self.x = 0, choice(range(100, GAME_WINDOW[0]+1, 100))
        # After exploding of big Asteroid can be created the smaller one on the same place.
        else:
            self.x, self.y = x, y

        self.rotation = 0
        # Speed is random
        self.x_speed = choice(list(range(10, 81, 10))) * choice([-1, 1]) * level
        self.y_speed = choice(list(range(10, 81, 10))) * choice([-1, 1]) * level

        # Asteroids can be in 4 sizes (levels), but this part of code is not complete
        # only use of asteroid size 1 and 2 is now implemented in the game
        self.level = level
        level_list = [('big', 4), ('med', 2), ('small', 2), ('tiny', 2)]

        self.image_name = 'meteor' + choice(['Brown', 'Grey']) + '_' + level_list[level-1][0] + str(choice(range(1, level_list[level-1][1]+1)))
        self.sprite = pyglet.sprite.Sprite(GAME_IMG[self.image_name], self.x, self.x, batch=batch_objects)
        super().__init__()

    def tick(self, dt):
        self.rotation = self.rotation + dt * (+ ROTATION_SPEED//2)
        super().tick(dt)


class Laser(SpaceObject):
    '''
    Laser class (for Spaceship and Ufo).
    '''
    def __init__(self, x, y, x_speed, y_speed, rotation, ship1_ufo2):
        self.rotation = rotation
        self.x = x + math.cos(self.rotation) * 50
        self.y = y + math.sin(self.rotation) * 50
        self.x_speed = x_speed + math.cos(self.rotation) * 400
        self.y_speed = y_speed + math.sin(self.rotation) * 400
        self.sprite = pyglet.sprite.Sprite(GAME_IMG['laserBlue06'], self.x, self.x, batch=batch_effects)
        self.expiration = 1.5  # laser does not hit any object = disappear
        self.shooting_object = ship1_ufo2  # value 1 = ship;  2 = ufo
        super().__init__()

    def tick(self, dt):
        # Laser can shoot Asteroid, Ufo or Spaceship.
        for object in OBJECTS:
            if isinstance(object, Asteroid) and overlaps(object, self):
                if self.shooting_object == 1:
                    GAME['score'] += object.level * 10
                return self.hit_by_laser(object, 'Asteroid')
            if isinstance(object, Ufo) and overlaps(object, self) and self.shooting_object == 1:
                GAME['score'] += 100
                return self.hit_by_laser(object, 'Ufo')
            if isinstance(object, Spaceship) and GAME['shield'] < 0 and overlaps(object, self) and self.shooting_object == 2:
                return self.hit_by_laser(object, 'Spaceship')

        # laser does not hit any object = disappear
        self.expiration -= dt
        if self.expiration < 0:
            return self.delete_object()
        # laser out of window = disappear
        if 15 > self.x or self.x > GAME_WINDOW[0]-15:
            return self.delete_object()
        if 15 > self.y or self.y > GAME_WINDOW[1]-15:
            return self.delete_object()
        super().tick(dt)

    def hit_by_laser(self, object, what_was_destroyed):
        '''
        What happen with objects after hitting of Laser.
        '''
        self.delete_object()
        if what_was_destroyed == 'Spaceship':
            object.hit_by_spaceship()
        if what_was_destroyed == 'Asteroid':
            if object.level in [1]:
                for i in range(2):
                    OBJECTS.append(Asteroid(object.x, object.y, object.x_speed, object.y_speed, object.level+1))
            object.delete_object()
        if what_was_destroyed == 'Ufo':
            object.explosion('ufo explosion')
            object.delete_object()
            ufo_in_game[0] = 0


class Life(SpaceObject):
    '''
    Class for little Spaceship, that represents life in the game.
    '''
    def __init__(self, rank):
        self.rank = rank
        self.x = rank*45
        self.y = 50
        self.sprite = pyglet.sprite.Sprite(life_image, self.x, self.y, batch=batch_front)
        self.radius = 10

    def tick(self, dt):
        pass
