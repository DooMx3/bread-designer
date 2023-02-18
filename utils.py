from pygame import Rect, mouse


def hovered(hitbox: Rect, res_scale=1):
    x = hitbox.x * res_scale
    y = hitbox.y * res_scale
    width = hitbox.width * res_scale
    height = hitbox.height * res_scale

    new_hitbox = Rect(x, y, width, height)
    mouse_pos = mouse.get_pos()
    return new_hitbox.collidepoint(mouse_pos)
