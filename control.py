from pyglet.window import key



pressed_keys = set()


def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        pressed_keys.add(('left',0))
    if symbol == key.RIGHT:
        pressed_keys.add(('right',0))
    if symbol == key.UP:
        pressed_keys.add(('up',0))
    if symbol == key.SPACE:
        pressed_keys.add(('fire',0))
    if symbol == key.ENTER:
        pressed_keys.add(('enter',0))
    if symbol == key.M:
        pressed_keys.add(('M',0))


def on_key_release(symbol, modifiers):
    if symbol == key.LEFT:
        pressed_keys.discard(('left',0))
    if symbol == key.RIGHT:
        pressed_keys.discard(('right',0))
    if symbol == key.UP:
        pressed_keys.discard(('up',0))
    if symbol == key.SPACE:
        pressed_keys.discard(('fire',0))
    if symbol == key.M:
        pressed_keys.discard(('M',0))
