from game_settings import GAME_WINDOW



def distance(a, b, wrap_size):
    '''
    Distance in one direction (x or y).
    '''
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result


def overlaps(a, b):
    '''
    Returns true iff two space objects overlap.
    '''
    distance_squared = (distance(a.x, b.x, GAME_WINDOW[0]) ** 2 +
                        distance(a.y, b.y, GAME_WINDOW[1]) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared
