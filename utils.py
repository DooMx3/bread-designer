from pygame import Rect, mouse


def hovered(hitbox: Rect, res_scale=1):
    x = hitbox.x * res_scale
    y = hitbox.y * res_scale
    width = hitbox.width * res_scale
    height = hitbox.height * res_scale

    new_hitbox = Rect(x, y, width, height)
    mouse_pos = mouse.get_pos()
    return new_hitbox.collidepoint(mouse_pos)


def brighten_color(color, value):
    r, g, b = color
    r = min(r + value, 255)
    g = min(g + value, 255)
    b = min(b + value, 255)

    return r, g, b


def darken_color(color, value):
    r, g, b = color
    r = max(r - value, 0)
    g = max(g - value, 0)
    b = max(b - value, 0)

    return r, g, b
