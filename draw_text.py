import pyglet



def draw_text(text, x, y, size, anchor_x):
    '''
    Draw text in playfield.
    '''
    kenvector_font = pyglet.font.add_file('Font/kenvector_future.ttf')
    text = pyglet.text.Label(
        text,
        font_name='KenVector Future',
        font_size=size,
        x=x, y=y, anchor_x=anchor_x)
    text.draw()
