from os import walk
from PIL import Image, ImageDraw
from gui import *


class BreadBoard:
    XOFFSET = -2
    YOFFSET = -1.5

    def __init__(self, state):
        self.leds: list[Diode] = list()
        self.wires: list[Wire] = list()
        self.flipped = False
        self.pico_flipped = False
        self.pico_pos = None
        for name, value in state.items():
            self.__setattr__(name, value)

        self.background = Image.open('images/breadboard.png').convert("RGBA")
        self.pico = Image.open("images/pico.png")
        self.diode_image = Image.open("images/led_diode.png").convert("RGBA")
        self.pins_image = Image.open("images/led_pins.png").convert("RGBA")

        self.draw = ImageDraw.Draw(self.background)

        if self.flipped:
            self.background = self.background.transpose(method=Image.ROTATE_180)

        if self.pico_flipped:
            self.pico = self.pico.transpose(method=Image.ROTATE_180)

        if self.pico_pos:
            self.background.paste(self.pico, self.pico_pos)

        self.draw_wires()

        self.draw_diodes()

    def draw_wires(self):
        for wire in self.wires:
            points = wire.fixed_points

            for point1, point2 in zip(points[:-1], points[1:]):
                x1, y1 = point1
                x2, y2 = point2
                x1 += self.XOFFSET
                x2 += self.XOFFSET
                y1 += self.YOFFSET
                y2 += self.YOFFSET
                self.draw.line((x1, y1, x2, y2), fill=wire.color, width=wire.WIDTH)

            for ind in range(-1, 1):
                x1, y1 = points[ind]
                x1, y1 = x1 - 6, y1 - 6
                self.draw.rectangle((x1, y1, x1 + 9, y1 + 9), fill=wire.color)
                self.draw.ellipse((x1 + 3, y1 + 3, x1 + 6, y1 + 6), fill=(230, 230, 230))

    def draw_diodes(self):  # TODO
        width1, height1 = self.diode_image.size
        width2, height2 = self.pins_image.size
        for diode in self.leds:
            self.background.paste(diode.diode_image, box=(diode.x_cord, diode.y_cord, diode.x_cord + width1, diode.y_cord + height1))
            self.background.paste(diode.pins_image, box=(diode.x_cord, diode.y_cord + height1, diode.x_cord + width2, diode.y_cord + height2))

    def get_image(self):
        return self.background


class Files:
    DEFAULT_PATH = "output/"
    DEFAULT_EXT = ".png"
    DEFAULT_NAME = f"rycina #{DEFAULT_EXT}"

    def __init__(self):
        self.saves_counter = self.get_last_id() + 1
        self.path = self.DEFAULT_PATH

    def get_last_id(self):
        *_, files = next(walk(self.DEFAULT_PATH))
        max_id = 0
        for file in files:
            if file.endswith(self.DEFAULT_EXT):
                rmv1, rmv2 = self.DEFAULT_NAME.split("#")
                file = file.replace(rmv1, "")
                file = file.replace(rmv2, "")
                id_ = int(file)
                if id_ > max_id:
                    max_id = id_

        return max_id

    def export(self, image):
        filename = self.DEFAULT_NAME.replace("#", str(self.saves_counter))
        image.save(self.DEFAULT_PATH + filename)
        self.saves_counter += 1
        return self.path, filename

    def export_v2(self, image):
        filename = self.DEFAULT_NAME.replace("#", str(self.saves_counter))
        # image.save(self.DEFAULT_PATH + filename)
        pygame.image.save(image, self.DEFAULT_PATH + filename, "namehint")
        self.saves_counter += 1
        return self.path, filename


f = Files()
f.get_last_id()
# # Open the two images
# foreground = Image.open('foreground.png')
#
# # Paste the foreground image onto the background image
# # background.paste(foreground, (150, 50))
# draw = ImageDraw.Draw(background)
# draw.line((5, 5, 100, 5), fill=(0, 0, 255), width=5, joint="curve")
# # Save the resulting image
# background.save('pasted_image.png')
