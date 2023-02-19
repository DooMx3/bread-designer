import ctypes
from gui import *
import image


class Display:
    SETTINGS_BACKGROUND = (103, 155, 202)
    EXPORT_MSG = "Wyeksportowano do #1 jako #2"

    def __init__(self):
        pygame.init()

        self.size = (const.DISPLAY_WIDTH, const.DISPLAY_HEIGHT)
        self.scaled_size = (const.DISPLAY_WIDTH * res_scale, const.DISPLAY_HEIGHT * res_scale)

        self.fps = settings_file["fps"]

        self.window = pygame.Surface(self.size)
        self.scaled_window = pygame.display.set_mode(self.scaled_size)
        self.breadboard = BreadBoard()
        self.files = image.Files()
        self.states = PreviousStates(self.breadboard.get_state())
        self.popups = list()

        self.main_tool_menu = ToolMenu(
            option_buttons=(
                {"icon_name": "export", "lockable": False},
                {"icon_name": "erase", "lockable": False},
                {"icon_name": "prev", "lockable": False},
                {"icon_name": "next", "lockable": False},
                {"icon_name": "settings", "lockable": False},
            ),
            new_item_buttons=(
                {"icon_name": "pico"},
                {"icon_name": "wire", "color_input": True},
                {"icon_name": "led", "color_input": True},
            ),
            action_buttons=(
                {"icon_name": "select"},
                {"icon_name": "switch", "lockable": False},
            )
        )

        self.settings_tool_menu = ToolMenu(
            option_buttons=(
                {"icon_name": "back", "lockable": False},
            )
        )

    def export_state(self, state):
        breadboard = image.BreadBoard(state)
        path, filename = self.files.export_v2(breadboard.get_image())
        message = self.EXPORT_MSG
        message = message.replace("#1", path)
        message = message.replace("#2", filename)
        return message

    def export_image(self):
        path, filename = self.files.export_v2(self.breadboard.image_)
        message = self.EXPORT_MSG
        message = message.replace("#1", path)
        message = message.replace("#2", filename)
        return message

    def transform_display(self):
        scaled = pygame.transform.scale(self.window, self.scaled_size)
        self.scaled_window.blit(scaled, (0, 0))
        pygame.display.flip()

    def settings_page(self):
        window_size_box = ValueBox(100, 50, 100)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            resp = self.settings_tool_menu.tick()
            window_size_box.tick()

            if resp == "back":
                return True

            self.window.fill(self.SETTINGS_BACKGROUND)
            self.settings_tool_menu.draw(self.window)
            window_size_box.draw(self.window)
            self.transform_display()

    def add_popup(self, text):
        self.popups.append(PopUp(text))

    def main_loop(self):
        color = tuple()
        adding_wire = False
        pin_empty = False
        action = None
        reset_action = False
        running = True
        while running:
            pygame.time.Clock().tick(self.fps)

            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            point = self.breadboard.tick(keys)
            if point:
                point, pin_empty = point
            resp = self.main_tool_menu.tick()
            for popup in self.popups:
                popup.tick()
                if popup.delete:
                    self.popups.remove(popup)

            self.breadboard.update_image()

            if isinstance(resp, tuple):
                color = resp
            elif isinstance(resp, str):
                if action == resp:
                    reset_action = True
                action = resp

            if action not in ["wire", "led"] or reset_action:
                adding_wire = False
                color = tuple()

            if action is None:
                self.main_tool_menu.deactivate()

            if action == "switch":
                self.breadboard.flip()
                self.states.add(self.breadboard.get_state())
                action = None
            elif action == "pico":
                done = placing_pico(self.breadboard.place_pico)
                if done:
                    self.states.add(self.breadboard.get_state())
                    action = None
            elif action == "export":
                msg = self.export_image()
                self.add_popup(msg)
                action = None
            elif action == "wire":
                if adding_wire is False and color:
                    self.breadboard.add_wire(color)
                    self.states.add(self.breadboard.get_state())
                    adding_wire = True
                elif adding_wire:
                    if point:
                        self.breadboard.add_wire_point(point)
                        self.states.add(self.breadboard.get_state())
            elif action == "led" and color and point and pin_empty is False:
                self.breadboard.add_diode(point, color)
                self.states.add(self.breadboard.get_state())
                action = None
            elif action == "erase":
                self.breadboard = BreadBoard()
                self.states.add(self.breadboard.get_state())
                action = None
            elif action == "prev":
                self.breadboard.load_state(self.states.restore())
                action = None
            elif action == "next":
                self.breadboard.load_state(self.states.forward())
                action = None
            elif action == "settings":
                r = self.settings_page()
                if not r:
                    running = False

            reset_action = False

            self.window.fill((0, 0, 0))
            self.main_tool_menu.draw(self.window)
            self.breadboard.draw(self.window)
            self.main_tool_menu.draw_palette(self.window)
            for popup in self.popups:
                popup.draw(self.window)

            self.transform_display()

        pygame.quit()


def main():
    if __name__ == "__main__":
        display = Display()
        # display.main_loop()
        try:
            display.main_loop()
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, "code error: " + str(e), "Error", 0x10)


main()
