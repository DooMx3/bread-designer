from math import sqrt
import pygame
import constants as const


class Button:
    # TODO only one button until left mouse button is released
    BACKGROUND_COLOR = (22, 37, 52)
    HOVER_BG_COLOR = (33, 56, 77)

    BUTTON_SIZE = 50

    def __init__(self, x=0, y=0, icon_name="default", lockable=True, color_input=False):
        self.icon = pygame.image.load(f"icons/{icon_name}.png")
        self.action = icon_name
        self.x_cord = x
        self.y_cord = y
        self.hitbox = pygame.Rect(x, y, self.BUTTON_SIZE, self.BUTTON_SIZE)
        self.lockable = lockable
        self.color_input = color_input
        self.hover = False
        self.active = False
        self.clicked = False

    def place(self, x, y):
        self.x_cord = x
        self.y_cord = y
        self.hitbox = pygame.Rect(x, y, self.BUTTON_SIZE, self.BUTTON_SIZE)

    def activate(self):
        if self.lockable:
            self.active = True

    def deactivate(self):
        self.active = False

    def tick(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.hitbox.collidepoint(mouse_pos)

        if self.hover and pygame.mouse.get_pressed()[0] and not self.clicked:
            self.clicked = True
            return True
        elif not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        return False

    def draw(self, window):
        if self.hover:
            color = self.HOVER_BG_COLOR
        else:
            color = self.BACKGROUND_COLOR

        if self.active:
            radius = 17
        else:
            radius = 5

        pygame.draw.rect(window, color, self.hitbox, border_radius=radius)
        window.blit(self.icon, (self.x_cord, self.y_cord))


class PopUp:
    INSTANCES = []

    WIDTH = 550
    HEIGHT = 120
    FONT_SIZE = 24
    DEFAULT_Y = const.DISPLAY_HEIGHT - HEIGHT - 25
    BACKGROUND_COLOR = (67, 125, 200)

    def __init__(self, text):
        self.INSTANCES.append(self)
        sub_y = (len(self.INSTANCES) - 1) * 25
        font = pygame.font.Font(pygame.font.match_font("Calibri"), self.FONT_SIZE)
        self.text_image = font.render(text, True, (0,) * 3)

        self.x_cord = const.DISPLAY_WIDTH
        self.y_cord = self.DEFAULT_Y - sub_y
        self.x_speed = 7
        self.dec_acc = 2

        self.timer = 0
        self.delete = False

    def tick(self):
        self.x_cord -= self.x_speed

        whole_on_screen = const.DISPLAY_WIDTH - self.x_cord >= self.WIDTH
        whole_off_screen = const.DISPLAY_WIDTH - self.x_cord <= 0
        moving_left = self.x_speed > 0
        moving_right = self.x_speed < 0

        if whole_on_screen and moving_left:
            self.x_speed -= self.dec_acc
            self.x_speed = max(self.x_speed, 0)
        elif whole_on_screen and moving_right:
            self.x_speed -= self.dec_acc
            self.x_speed = min(self.x_speed, 7)
        elif whole_off_screen:
            self.delete = True
            self.INSTANCES.remove(self)

        if not moving_left or moving_right:
            self.timer += 1

        if self.timer > 240:
            self.x_speed = -1
            self.timer = 0

        if self.dec_acc > 0.5 and moving_left:
            self.dec_acc -= 0.5
        elif self.dec_acc < 2 and moving_right:
            self.dec_acc += 0.5

    def draw(self, window):
        pygame.draw.rect(window,
                         self.BACKGROUND_COLOR,
                         (self.x_cord, self.y_cord, self.WIDTH, self.HEIGHT))
        window.blit(self.text_image, (self.x_cord, self.y_cord))


class ValueBox:
    FONT = pygame.font.get_default_font()
    FONT_COLOR = (0, 0, 0)
    FONT_SIZE = 40
    BUTTON_COLOR = (20, 40, 120)
    BUTTON_SIZE = (20, 20)
    BUTTON_UP_POS = (100, 100)
    BUTTON_DOWN_POS = (100, 130)

    EXPONENT = 1.00005

    BACKGROUND_COLOR = (118, 158, 197)
    BORDER_COLOR = (179, 201, 223)
    BORDER_WIDTH = 8

    def __init__(self, value: int, x_cord, y_cord):
        self.value = value
        self.add_value = 0
        self.float_value = 0.001
        self.x_cord = x_cord
        self.y_cord = y_cord

        self.FONT = pygame.font.Font(self.FONT, self.FONT_SIZE)
        self.text_display = self.FONT.render(str(self.value), True, self.FONT_COLOR)
        self.button_up = pygame.Rect(self.BUTTON_UP_POS[0], self.BUTTON_UP_POS[1], self.BUTTON_SIZE[0], self.BUTTON_SIZE[1])
        self.button_down = pygame.Rect(self.BUTTON_DOWN_POS[0], self.BUTTON_DOWN_POS[1], self.BUTTON_SIZE[0], self.BUTTON_SIZE[1])

    def tick(self):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        if clicked:
            if self.button_up.collidepoint(mouse_pos):
                self.float_value **= self.EXPONENT
                self.add_value += self.float_value
            elif self.button_down.collidepoint(mouse_pos):
                self.float_value **= 1/self.EXPONENT
                self.add_value -= self.float_value
            self.text_display = self.FONT.render(str(self.value), True, self.FONT_COLOR)
            print(self.add_value)
            self.value += self.add_value
        elif not clicked:
            # self.float_value = 1.1
            pass

    def draw(self, window):
        half_border = self.BORDER_WIDTH // 2
        pygame.draw.rect(window,
                         self.BORDER_COLOR,
                         (self.x_cord - half_border, self.y_cord - half_border, 150 + self.BORDER_WIDTH, 50 + self.BORDER_WIDTH),
                         border_radius=15)

        pygame.draw.rect(window,
                         self.BACKGROUND_COLOR,
                         (self.x_cord, self.y_cord, 150, 50),
                         border_radius=15)

        window.blit(self.text_display, (
            self.text_display.get_rect(center=(
                self.button_up.centerx - 40,
                self.button_up.centery)
            )
        ))
        pygame.draw.rect(window, self.BUTTON_COLOR, self.button_up)
        pygame.draw.rect(window, self.BUTTON_COLOR, self.button_down)


class ToolMenu:
    WIDTH = const.DISPLAY_WIDTH
    HEIGHT = const.MENU_HEIGHT
    POSITION = (0, 0)
    COLOR_BACKGROUND = (55, 93, 129)

    BUTTONS_START = 35
    BUTTONS_Y = 10
    BUTTON_WIDTH = 50
    BUTTONS_SPACING = 30

    LINE_COLOR = (28, 46, 65)

    def __init__(self, option_buttons=(), new_item_buttons=(), action_buttons=()):
        self.background = pygame.Rect(*self.POSITION, self.WIDTH, self.HEIGHT)
        self.palette = ColorPalette(1000, 0)
        self.action = None

        self.option_buttons = [Button(**btn) for btn in option_buttons]
        self.new_item_buttons = [Button(**btn) for btn in new_item_buttons]
        self.action_buttons = [Button(**btn) for btn in action_buttons]

        self.all_buttons = self.action_buttons + self.option_buttons + self.new_item_buttons
        self.lines = list()

        self.place_buttons()

    def deactivate(self):
        for btn in self.all_buttons:
            btn.deactivate()

    def tick(self):
        for btn in self.all_buttons:
            if btn.tick():
                self.action = btn.action
                self.deactivate()
                btn.activate()
                if btn.color_input:
                    self.palette.activate()
                return btn.action

        color = self.palette.tick()
        if color:
            return color

    def place_buttons(self):
        button_x = self.BUTTONS_START

        for button in self.option_buttons:
            button.place(button_x, self.BUTTONS_Y)
            button_x += self.BUTTON_WIDTH + self.BUTTONS_SPACING

        if self.action_buttons:
            self.lines.append(button_x)
            button_x += 5 + self.BUTTONS_SPACING

        for button in self.action_buttons:
            button.place(button_x, self.BUTTONS_Y)
            button_x += self.BUTTON_WIDTH + self.BUTTONS_SPACING

        if self.new_item_buttons:
            self.lines.append(button_x)
            button_x += 5 + self.BUTTONS_SPACING

        for button in self.new_item_buttons:
            button.place(button_x, self.BUTTONS_Y)
            button_x += self.BUTTON_WIDTH + self.BUTTONS_SPACING

    def draw_line(self, window, x, width=5):
        pygame.draw.line(window, self.LINE_COLOR,
                         (x, 0),
                         (x, self.HEIGHT), width)

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR_BACKGROUND, self.background)

        for btn in self.action_buttons:
            btn.draw(window)

        for btn in self.new_item_buttons:
            btn.draw(window)

        for btn in self.option_buttons:
            btn.draw(window)

        for line in self.lines:
            self.draw_line(window, line)

    def draw_palette(self, window):
        self.palette.draw(window)


class ColorPalette:
    BOX_SIZE = 20
    EXPANDED_HEIGHT = 25
    STOPS_Q = 8
    WIDTH = 5 * BOX_SIZE
    BORDER_WIDTH = 2

    def __init__(self, x_cord, y_cord, steps=5):
        self.color_stops = [(255, 0, 0), (255, 255, 0), (0, 255, 0),
                            (0, 255, 255), (0, 0, 255), (255, 0, 255),
                        ]
        self.steps = steps
        self.active = False
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.rgb_colors = self.color_gradient(steps)
        self.boxes = list()
        self.generate_boxes()

    def color_gradient(self, steps):
        """
        Generate a color gradient from red to yellow, green, cyan, blue, magenta, and shades of gray.
        :param steps: number of steps in the gradient
        :return: list of (r, g, b) tuples
        """

        # Generate the color steps between each stop
        color_steps = []
        for i in range(len(self.color_stops) - 1):
            start = self.color_stops[i]
            end = self.color_stops[i + 1]
            for j in range(steps):
                t = j / steps
                r = int(start[0] + (end[0] - start[0]) * t)
                g = int(start[1] + (end[1] - start[1]) * t)
                b = int(start[2] + (end[2] - start[2]) * t)
                color_steps.append((r, g, b))

        # Add the last color stop
        # color_steps.append(self.color_stops[-1])

        for value in range(0, 255, 255//steps):
            color_steps.append((value, ) * 3)

        return color_steps

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def generate_boxes(self):
        add_x = 0
        add_y = 0
        col = 0
        for _ in self.rgb_colors:
            self.boxes.append(pygame.Rect(self.x_cord + add_x, self.y_cord + add_y, self.BOX_SIZE, self.BOX_SIZE))
            add_x += self.BOX_SIZE
            col += 1
            if col == self.steps * 2:
                col = 0
                add_x = 0
                add_y += self.BOX_SIZE

    def tick(self):
        if not self.active:
            return False

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        for box, color in zip(self.boxes, self.rgb_colors):
            if box.collidepoint(mouse) and click:
                self.deactivate()
                return color
        return False

    def draw(self, window):
        if not self.active:
            return

        mouse = pygame.mouse.get_pos()
        for box, color in zip(self.boxes, self.rgb_colors):
            if not box.collidepoint(mouse):
                pygame.draw.rect(window, color, box)
            else:
                inset_rect = box.inflate(-self.BORDER_WIDTH * 2, -self.BORDER_WIDTH * 2)
                r, g, b = color
                reversed_color = (255 - r, 255 - g, 255 - b)
                pygame.draw.rect(window, reversed_color, box, self.BORDER_WIDTH)
                pygame.draw.rect(window, color, inset_rect)


class Diode:
    HEIGHT = 49

    def __init__(self, x, y, diode_image=None):
        if diode_image is None:
            self.diode_image = pygame.image.load("images/led_diode.png")
        else:
            self.diode_image = diode_image
        self.pins_image = pygame.image.load("images/led_pins.png")
        self.x_cord = x
        self.y_cord = y

    def copy(self):
        return Diode(self.x_cord, self.y_cord, self.diode_image)

    def set_img_to_color(self, color):
        pixels = pygame.PixelArray(self.diode_image)

        # Iterate through the pixel array and set non-transparent pixels to red
        for x in range(self.diode_image.get_width()):
            for y in range(self.diode_image.get_height()):
                if pixels[x, y] != self.diode_image.map_rgb((0, 0, 0, 0)):  # check if pixel is transparent
                    pixels[x, y] = self.diode_image.map_rgb(color)

        self.diode_image = pixels.make_surface()

    def draw(self, window):
        window.blit(self.diode_image, (self.x_cord + const.DIODE_X_OFFSET, self.y_cord))
        window.blit(self.pins_image, (self.x_cord + const.DIODE_X_OFFSET, self.y_cord + self.diode_image.get_height()))


class Pin:
    PIN_SIZE = 14
    MARGIN_LEFT_TOP = 6
    MARGIN_RIGHT_BOTTOM = 7
    PIN_SPACING = MARGIN_RIGHT_BOTTOM + MARGIN_LEFT_TOP

    COLOR_INNER_SELECT = (10, 20, 30)
    COLOR_OUTER_SELECT = (179, 205, 229)

    def __init__(self, x, y, empty=False):
        self.x_cord = x
        self.y_cord = y
        self.empty = empty
        self.hitbox = pygame.Rect(x - self.MARGIN_LEFT_TOP,
                                  y - self.MARGIN_LEFT_TOP,
                                  self.PIN_SIZE + self.PIN_SPACING,
                                  self.PIN_SIZE + self.PIN_SPACING)
        self.inner_hitbox = pygame.Rect(x, y, self.PIN_SIZE, self.PIN_SIZE)

    def tick(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return self.x_cord, self.y_cord - ToolMenu.HEIGHT, self.empty
        return False

    def draw(self, window: pygame.Surface):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, self.COLOR_OUTER_SELECT, self.hitbox)
            if not self.empty:
                pygame.draw.rect(window, self.COLOR_INNER_SELECT, self.inner_hitbox)


class BreadBoard:
    WIDTH = const.BREADBOARD_WIDTH
    HEIGHT = const.BREADBOARD_HEIGHT

    FIRST_POWER_PIN = (70, 30)
    FIRST_DATA_PIN = (16, 127)
    SECOND_DATA_PIN = (16, 285)
    SECOND_POWER_PIN = (70, 463)

    PIN_SPACING = 13
    POWER_BLOCK_SPACING = 40
    POWER_PINS_Q = 50
    POWER_BLOCKS_Q = 10
    BLOCK_PINS_Q = 5
    DATA_PINS_COL_Q = 63
    DATA_PINS_ROW_Q = 5

    PICO_Y = 174

    POSITION = (0, ToolMenu.HEIGHT)

    def __init__(self):
        """
        if attribute is not ment to be stored in breadboard state
        its name should end with underscore
        """
        self.pins_, self.empty_points_ = self.generate_pins()
        self.empty_image_ = pygame.image.load("images/breadboard.png")
        self.image_ = self.empty_image_

        self.pico_image_org_ = pygame.image.load("images/pico.png")
        self.pico_image_ = self.pico_image_org_
        self.pico_pos = None

        self.leds = list()

        self.wires = list()

        self.flipped = False
        self.pico_flipped = False

        self.last_pin = False

    def gen_power_pins(self):
        pins = []
        next_pin = Pin.PIN_SIZE + self.PIN_SPACING
        for power_pins in range(2):
            if power_pins == 0:
                x_cord, y_cord = self.FIRST_POWER_PIN
            else:
                x_cord, y_cord = self.SECOND_POWER_PIN
            y_cord += self.POSITION[1]
            for block in range(self.POWER_BLOCKS_Q):
                for p in range(self.BLOCK_PINS_Q):
                    pins.append(Pin(x_cord, y_cord))
                    pins.append(Pin(x_cord, y_cord + next_pin))
                    x_cord += next_pin
                x_cord += self.POWER_BLOCK_SPACING - self.PIN_SPACING
        return pins

    def gen_data_pins(self):
        pins = []
        next_pin = Pin.PIN_SIZE + self.PIN_SPACING
        for data_pins in range(2):
            if data_pins == 0:
                x_cord, y_cord = self.FIRST_DATA_PIN
            else:
                x_cord, y_cord = self.SECOND_DATA_PIN
            y_cord += self.POSITION[1]
            for column in range(self.DATA_PINS_COL_Q):
                for row in range(self.DATA_PINS_ROW_Q):
                    pins.append(Pin(x_cord, y_cord + next_pin * row))
                x_cord += next_pin
        return pins

    def gen_empty_pins(self):
        empty = []

        def add(x, y):
            empty.append(Pin(x, y, empty=True))

        next_pin = Pin.PIN_SIZE + self.PIN_SPACING
        for power_row in range(2):
            if power_row == 0:
                x_cord, y_cord = self.FIRST_POWER_PIN
            else:
                x_cord, y_cord = self.SECOND_POWER_PIN

            x_cord -= next_pin * 2
            y_cord += self.POSITION[1]
            for _ in range(2):
                add(x_cord, y_cord)
                add(x_cord, y_cord + next_pin)
                x_cord += next_pin
            x_cord += next_pin * 5
            for _ in range(9):
                add(x_cord, y_cord)
                add(x_cord, y_cord + next_pin)
                x_cord += next_pin * 6
            for _ in range(2):
                add(x_cord, y_cord)
                add(x_cord, y_cord + next_pin)
                x_cord += next_pin

        for data_row in range(3):
            if data_row == 0:
                x_cord, y_cord = self.FIRST_DATA_PIN
                y_cord -= 2
            elif data_row == 1:
                x_cord, y_cord = self.SECOND_DATA_PIN
                y_cord += 1
            else:
                x_cord, y_cord = self.SECOND_DATA_PIN
                y_cord += next_pin * 6
            y_cord += self.POSITION[1] - next_pin
            for _ in range(63):
                add(x_cord, y_cord)
                x_cord += next_pin

        x_cord, y_cord = self.FIRST_POWER_PIN
        x_cord -= next_pin * 2
        y_cord += self.POSITION[1] - next_pin
        for _ in range(63):
            add(x_cord, y_cord)
            x_cord += next_pin

        x_cord, y_cord = self.SECOND_POWER_PIN
        x_cord -= next_pin * 2
        y_cord += self.POSITION[1] + next_pin * 2
        for _ in range(63):
            add(x_cord, y_cord)
            x_cord += next_pin

        return empty

    def generate_pins(self):
        pins = []
        empty = self.gen_empty_pins()
        pins.extend(self.gen_power_pins())
        pins.extend(self.gen_data_pins())
        return pins, empty

    @staticmethod
    def create_copy(key, value):
        new_list = []
        for elem in value:
            try:
                new_list.append(elem.copy())
            except AttributeError:
                raise Exception(f"variable {key} is a list of objects with no copy() method: {value}")
        return new_list

    def get_state(self):
        attributes = vars(self)
        filtered_attributes = dict()
        for k, v in attributes.items():
            if not (k.startswith("_") or k.endswith("_")):
                if isinstance(v, list):
                    filtered_attributes[k] = self.create_copy(k, v)
                else:
                    filtered_attributes[k] = v
        return filtered_attributes

    def load_state(self, state):
        print("before", self.wires)
        for name, value in state.items():
            self.__setattr__(name, value)
        print("after", self.wires)

    # gui operations

    def tick(self):
        for pin in self.pins_ + self.empty_points_:
            response = pin.tick()
            if response:
                *r_pin, empty = response
                r_pin = tuple(r_pin)
                if r_pin != self.last_pin:
                    self.last_pin = r_pin
                    # print(r_pin, empty)
                    return r_pin, empty

    def flip(self):
        self.flipped = not self.flipped
        self.image_ = pygame.transform.rotate(self.image_, 180)

    def place_pico(self, side="left"):
        if side == "left":
            self.pico_pos = (0, self.PICO_Y)
            self.pico_image_ = self.pico_image_org_
            self.pico_flipped = False
        elif side == "right":
            self.pico_pos = (self.WIDTH - self.pico_image_.get_width(), self.PICO_Y)
            self.pico_image_ = pygame.transform.rotate(self.pico_image_org_, 180)
            self.pico_flipped = True

        self.pico_image_.set_alpha(192)

        mouse = pygame.mouse.get_pos()
        pico = pygame.Rect(*self.pico_pos, *self.pico_image_.get_size())
        if pygame.mouse.get_pressed()[0] and pico.collidepoint(mouse):
            self.pico_image_.set_alpha(255)
            return True
        return False

    def add_wire(self, color):
        self.wires.append(Wire(color))

    def add_diode(self, point, color):
        x, y = point
        y -= Diode.HEIGHT - Pin.PIN_SIZE
        led = Diode(x, y)
        led.set_img_to_color(color)
        self.leds.append(led)

    def add_wire_point(self, point):
        last_wire = self.wires[-1]
        points = last_wire.points
        last_point = None
        if points:
            last_point = points[-1]
        x, y = point
        x += const.WIRE_X_OFFSET
        y += const.WIRE_Y_OFFSET
        point = x, y
        if point != last_point:
            self.wires[-1].add(point)

    def update_image(self):
        self.image_.blit(self.pico_image_, (0, 0))
        self.image_ = pygame.image.load("images/breadboard.png")
        if self.pico_pos is not None:
            self.image_.blit(self.pico_image_, self.pico_pos)

        for wire in self.wires:
            wire.draw(self.image_)

        for led in self.leds:
            led.draw(self.image_)

    def draw(self, window):
        window.blit(self.image_, self.POSITION)
        for pin in self.pins_:
            pin.draw(window)
        for pin in self.empty_points_:
            pin.draw(window)

    def __eq__(self, other):
        c1 = self.wires == other.wires
        c2 = self.pico_pos == other.pico_pos
        c3 = self.flipped == other.flipped
        print(self.flipped, other.flipped)

        return c1 and c2 and c3

    def __repr__(self):
        return f"<{self.pico_pos} {self.wires}>"


class Wire:
    WIDTH = 8

    def __init__(self, color, points=()):
        self.points = list(points)
        self.fixed_points = list(map(lambda x: (x[0], x[1] - ToolMenu.HEIGHT), self.points))
        self.color = color

    def add(self, point):
        self.points.append(point)

    def draw(self, window):
        qw = self.WIDTH // 4
        if len(self.points) >= 2:
            pygame.draw.lines(window, self.color, False, self.points, self.WIDTH)

            # draws both ends of a wire
            for x, y in (self.points[0], self.points[-1]):
                x_cord = x - const.WIRE_X_OFFSET // 2
                y_cord = y - const.WIRE_Y_OFFSET // 2
                pygame.draw.rect(window, self.color, (x_cord, y_cord, self.WIDTH, self.WIDTH))
                pygame.draw.rect(window, (240, 240, 240), (x_cord + qw, y_cord + qw, self.WIDTH // 2, self.WIDTH // 2))

    def copy(self):
        return Wire(self.color, self.points)

    def __repr__(self):
        return f"|{len(self.points)}|"

    def __eq__(self, other):
        return self.points == other.points


def placing_pico(action):
    if pygame.mouse.get_pos()[0] <= BreadBoard.WIDTH / 2:
        done = action(side="left")
    else:
        done = action(side="right")
    return done


#TODO
class PreviousStates:
    CAPACITY = 50

    def __init__(self, initial):
        self.states = [initial]
        self.index = 0

    def add(self, state):
        last_state = self.states[-1]
        if state == last_state:
            print("TAKI SAM")
            return

        current_length = len(self.states)

        # if restore happened, delete next states
        if self.index < current_length - 2:
            self.states = self.states[:self.index + 1]
        elif self.index < self.CAPACITY:
            self.index += 1

        if current_length < self.CAPACITY:
            self.states.append(state)
        else:
            self.states.pop(0)
            self.states.append(state)

        print("new state, index: ", len(self.states), self.index)

    def restore(self):
        if self.index > 0:
            self.index -= 1
        print("get state", self.index)
        return self.states[self.index]

    def forward(self):
        if self.index < len(self.states) - 1:
            self.index += 1
        return self.states[self.index]
