from typing import Dict, List

import glfw
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_COLOR_BUFFER_BIT
from OpenGL.raw.GL.VERSION.GL_1_0 import glClear

counter: int = 0


class Slot:
    def __init__(self, window, number, closable):
        self.window: int = window
        self.number: int = number
        self.closable: int = closable


def usage() -> None:
    print("Usage: events [-f] [-h] [-n WINDOWS]")
    print("Options:")
    print("  -f use full screen")
    print("  -h show this help")
    print("  -n the number of windows to create")


key_name: Dict[int, str] = {
    # Printable keys
    glfw.KEY_A: "A",
    glfw.KEY_B: "B",
    glfw.KEY_C: "C",
    glfw.KEY_D: "D",
    glfw.KEY_E: "E",
    glfw.KEY_F: "F",
    glfw.KEY_G: "G",
    glfw.KEY_H: "H",
    glfw.KEY_I: "I",
    glfw.KEY_J: "J",
    glfw.KEY_K: "K",
    glfw.KEY_L: "L",
    glfw.KEY_M: "M",
    glfw.KEY_N: "N",
    glfw.KEY_O: "O",
    glfw.KEY_P: "P",
    glfw.KEY_Q: "Q",
    glfw.KEY_R: "R",
    glfw.KEY_S: "S",
    glfw.KEY_T: "T",
    glfw.KEY_U: "U",
    glfw.KEY_V: "V",
    glfw.KEY_W: "W",
    glfw.KEY_X: "X",
    glfw.KEY_Y: "Y",
    glfw.KEY_Z: "Z",
    glfw.KEY_1: "1",
    glfw.KEY_2: "2",
    glfw.KEY_3: "3",
    glfw.KEY_4: "4",
    glfw.KEY_5: "5",
    glfw.KEY_6: "6",
    glfw.KEY_7: "7",
    glfw.KEY_8: "8",
    glfw.KEY_9: "9",
    glfw.KEY_0: "0",
    glfw.KEY_SPACE: "SPACE",
    glfw.KEY_MINUS: "MINUS",
    glfw.KEY_EQUAL: "EQUAL",
    glfw.KEY_LEFT_BRACKET: "LEFT BRACKET",
    glfw.KEY_RIGHT_BRACKET: "RIGHT BRACKET",
    glfw.KEY_BACKSLASH: "BACKSLASH",
    glfw.KEY_SEMICOLON: "SEMICOLON",
    glfw.KEY_APOSTROPHE: "APOSTROPHE",
    glfw.KEY_GRAVE_ACCENT: "GRAVE ACCENT",
    glfw.KEY_COMMA: "COMMA",
    glfw.KEY_PERIOD: "PERIOD",
    glfw.KEY_SLASH: "SLASH",
    glfw.KEY_WORLD_1: "WORLD 1",
    glfw.KEY_WORLD_2: "WORLD 2",
    # Function keys
    glfw.KEY_ESCAPE: "ESCAPE",
    glfw.KEY_F1: "F1",
    glfw.KEY_F2: "F2",
    glfw.KEY_F3: "F3",
    glfw.KEY_F4: "F4",
    glfw.KEY_F5: "F5",
    glfw.KEY_F6: "F6",
    glfw.KEY_F7: "F7",
    glfw.KEY_F8: "F8",
    glfw.KEY_F9: "F9",
    glfw.KEY_F10: "F10",
    glfw.KEY_F11: "F11",
    glfw.KEY_F12: "F12",
    glfw.KEY_F13: "F13",
    glfw.KEY_F14: "F14",
    glfw.KEY_F15: "F15",
    glfw.KEY_F16: "F16",
    glfw.KEY_F17: "F17",
    glfw.KEY_F18: "F18",
    glfw.KEY_F19: "F19",
    glfw.KEY_F20: "F20",
    glfw.KEY_F21: "F21",
    glfw.KEY_F22: "F22",
    glfw.KEY_F23: "F23",
    glfw.KEY_F24: "F24",
    glfw.KEY_F25: "F25",
    glfw.KEY_UP: "UP",
    glfw.KEY_DOWN: "DOWN",
    glfw.KEY_LEFT: "LEFT",
    glfw.KEY_RIGHT: "RIGHT",
    glfw.KEY_LEFT_SHIFT: "LEFT SHIFT",
    glfw.KEY_RIGHT_SHIFT: "RIGHT SHIFT",
    glfw.KEY_LEFT_CONTROL: "LEFT CONTROL",
    glfw.KEY_RIGHT_CONTROL: "RIGHT CONTROL",
    glfw.KEY_LEFT_ALT: "LEFT ALT",
    glfw.KEY_RIGHT_ALT: "RIGHT ALT",
    glfw.KEY_TAB: "TAB",
    glfw.KEY_ENTER: "ENTER",
    glfw.KEY_BACKSPACE: "BACKSPACE",
    glfw.KEY_INSERT: "INSERT",
    glfw.KEY_DELETE: "DELETE",
    glfw.KEY_PAGE_UP: "PAGE UP",
    glfw.KEY_PAGE_DOWN: "PAGE DOWN",
    glfw.KEY_HOME: "HOME",
    glfw.KEY_END: "END",
    glfw.KEY_KP_0: "KEYPAD 0",
    glfw.KEY_KP_1: "KEYPAD 1",
    glfw.KEY_KP_2: "KEYPAD 2",
    glfw.KEY_KP_3: "KEYPAD 3",
    glfw.KEY_KP_4: "KEYPAD 4",
    glfw.KEY_KP_5: "KEYPAD 5",
    glfw.KEY_KP_6: "KEYPAD 6",
    glfw.KEY_KP_7: "KEYPAD 7",
    glfw.KEY_KP_8: "KEYPAD 8",
    glfw.KEY_KP_9: "KEYPAD 9",
    glfw.KEY_KP_DIVIDE: "KEYPAD DIVIDE",
    glfw.KEY_KP_MULTIPLY: "KEYPAD MULTIPLY",
    glfw.KEY_KP_SUBTRACT: "KEYPAD SUBTRACT",
    glfw.KEY_KP_ADD: "KEYPAD ADD",
    glfw.KEY_KP_DECIMAL: "KEYPAD DECIMAL",
    glfw.KEY_KP_EQUAL: "KEYPAD EQUAL",
    glfw.KEY_KP_ENTER: "KEYPAD ENTER",
    glfw.KEY_PRINT_SCREEN: "PRINT SCREEN",
    glfw.KEY_NUM_LOCK: "NUM LOCK",
    glfw.KEY_CAPS_LOCK: "CAPS LOCK",
    glfw.KEY_SCROLL_LOCK: "SCROLL LOCK",
    glfw.KEY_PAUSE: "PAUSE",
    glfw.KEY_LEFT_SUPER: "LEFT SUPER",
    glfw.KEY_RIGHT_SUPER: "RIGHT SUPER",
    glfw.KEY_MENU: "MENU",
}

action_name: Dict[int, str] = {
    glfw.PRESS: "pressed",
    glfw.RELEASE: "released",
    glfw.REPEAT: "repeated",
}

button_name: Dict[int, str] = {
    glfw.MOUSE_BUTTON_LEFT: "left",
    glfw.MOUSE_BUTTON_RIGHT: "right",
    glfw.MOUSE_BUTTON_MIDDLE: "middle",
}


def get_key_name(key: int) -> str:
    try:
        return key_name[key]
    except KeyError:
        return "UNKNOWN"


def get_action_name(action: int) -> str:
    try:
        return action_name[action]
    except KeyError:
        return "caused unknown action"


def get_button_name(button: int) -> str:
    try:
        return button_name[button]
    except KeyError:
        return str(button)


def get_mods_name(mods: int) -> str:
    if mods == 0:
        return " no mods"

    name: str = ""

    if (mods & glfw.MOD_SHIFT) > 0:
        name += " shift"
    if (mods & glfw.MOD_CONTROL) > 0:
        name += " control"
    if (mods & glfw.MOD_ALT) > 0:
        name += " alt"
    if (mods & glfw.MOD_SUPER) > 0:
        name += " super"
    if (mods & glfw.MOD_CAPS_LOCK) > 0:
        name += " capslock-on"
    if (mods & glfw.MOD_NUM_LOCK) > 0:
        name += " numlock-on"

    return name


def error_callback(error: int, description: str) -> None:
    print(f"Error: {description}")


def window_pos_callback(window: int, x: int, y: int) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(
        f"{counter:08X} to {slot.number} at {glfw.get_time():0.3f}: Window position: {x}, {y}"
    )

    counter += 1


def window_size_callback(window: int, width: int, height: int) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(
        f"{counter:08X} to {slot.number} at {glfw.get_time():0.3f}: Window size: {width}, {height}"
    )

    counter += 1


def framebuffer_size_callback(window: int, width: int, height: int) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(
        f"{counter:08X} to {slot.number} at {glfw.get_time():0.3f}: Framebuffer size: {width}, {height}"
    )

    counter += 1


def window_content_scale_callback(window: int, xscale: float, yscale: float) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(
        f"{counter:08X} to {slot.number} at {glfw.get_time():0.3f}: Window content scale: {xscale:0.3f}, {yscale:0.3f}"
    )

    counter += 1


def window_close_callback(window: int) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(f"{counter:08X} to {slot.number} at {glfw.get_time():0.3f}: Window close")

    counter += 1

    if not slot.closable:
        print(
            f"(( closing is disabled, press {glfw.get_key_name(glfw.KEY_C, 0)} to re-enable )"
        )

    glfw.set_window_should_close(window, slot.closable)


def window_refresh_callback(window: int) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(f"{counter:08X} to {slot.number} at {glfw.get_time():0.3f}: Window refresh")

    counter += 1

    glfw.make_context_current(window)
    glClear(GL_COLOR_BUFFER_BIT)
    glfw.swap_buffers(window)


def window_focus_callback(window: int, focused: bool) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(
        f"{counter:08x} to {slot.number} at {glfw.get_time():0.3f}: Window {'focused' if focused else 'unfocused'}"
    )

    counter += 1


def window_iconify_callback(window: int, iconified: bool) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(
        f"{counter:08x} to {slot.number} at {glfw.get_time():0.3f}: Window was {'iconified' if iconified else 'uniconified'}"
    )

    counter += 1


def window_maximize_callback(window: int, maximized: bool) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(
        f"{counter:08x} to {slot.number} at {glfw.get_time():0.3f}: Window was {'maximized' if maximized else 'unmaximized'}"
    )

    counter += 1


def mouse_button_callback(window: int, button: int, action: int, mods: int) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(
        f"{counter:08x} to {slot.number} at {glfw.get_time():0.3f}: Mouse button {button} ({get_button_name(button)}) (with{get_mods_name(mods)}) was {get_action_name(action)}"
    )

    counter += 1


def cursor_position_callback(window: int, x: float, y: float) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(
        f"{counter:08x} to {slot.number} at {glfw.get_time():0.3f}: Cursor position: {x} {y}"
    )

    counter += 1


def cursor_enter_callback(window: int, entered: bool) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(
        f"{counter:08x} to {slot.number} at {glfw.get_time():0.3f}: Cursor {'entered' if entered else 'left'} window"
    )

    counter += 1


def scroll_callback(window: int, x: float, y: float) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    print(
        f"{counter:08x} to {slot.number} at {glfw.get_time():0.3f}: Scroll: {x:0.3f} {y:0.3f}"
    )

    counter += 1


def key_callback(window: int, key: int, scancode: int, action: int, mods: int) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    name = glfw.get_key_name(key, scancode)

    if name:
        print(
            f"{counter:08x} to {slot.number} at {glfw.get_time():0.3f}: Key 0x{key:04x} Scancode 0x{scancode:04x} ({get_key_name(key)}) ({name}) (with{get_mods_name(mods)}) was {get_action_name(action)}"
        )
    else:
        print(
            f"{counter:08x} to {slot.number} at {glfw.get_time():0.3f}: Key 0x{key:04x} Scancode 0x{scancode:04x} ({get_key_name(key)}) (with{get_mods_name(mods)}) was {get_action_name(action)}"
        )

    counter += 1

    if action != glfw.PRESS:
        return

    if action == glfw.KEY_C:
        slot.closable = not slot.closable

        print(f"(( closing {'enabled' if slot.closable else 'disabled'} ))")
    elif action == glfw.KEY_L:
        state = glfw.get_input_mode(window, glfw.LOCK_KEY_MODS)
        glfw.set_input_mode(window, glfw.LOCK_KEY_MODS, not state)

        print(f"(( lock key mods {'enabled' if not state else 'disabled'} ))")


def char_callback(window: int, codepoint: int) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)
    string = chr(codepoint)

    print(
        f"{counter:08x} to {slot.number} at {glfw.get_time():0.3f}: Character 0x{codepoint:08x} ({string}) input"
    )

    counter += 1


def drop_callback(window: int, paths: List[str]) -> None:
    global counter

    slot = glfw.get_window_user_pointer(window)

    print(f"{counter:08x} to {slot.number} at {glfw.get_time():0.3f}: Drop input")

    for i, path in enumerate(paths):
        print(f'  {i}: "{path}"')

    counter += 1


def monitor_callback(monitor: int, event: int) -> None:
    global counter

    if event == glfw.CONNECTED:
        mode = glfw.get_video_mode(monitor)

        x, y = glfw.get_monitor_pos(monitor)
        widthMM, heightMM = glfw.get_monitor_physical_size(monitor)

        print(
            f"{counter:08x} at {glfw.get_time():0.3f}: Monitor {glfw.get_monitor_name(monitor)} ({mode.width}x{mode.height} at {x}x{y}, {widthMM}x{heightMM} mm) was connected"
        )

        counter += 1
    elif event == glfw.DISCONNECTED:
        print(
            f"{counter:08x} at {glfw.get_time():0.3f}: Monitor {glfw.get_monitor_name(monitor)} was disconnected"
        )

        counter += 1


def joystick_callback(jid: int, event: int) -> None:
    global counter

    if event == glfw.CONNECTED:
        axisCount = glfw.get_joystick_axes(jid)
        buttonCount = glfw.get_joystick_buttons(jid)
        hatCount = glfw.get_joystick_hats(jid)

        print(
            f"{counter:08x} at {glfw.get_time():0.3f}: Joystick {jid} ({glfw.get_joystick_name(jid)}) was connected with {axisCount} axes, {buttonCount} buttons, and {hatCount} hats"
        )

        if glfw.joystick_is_gamepad(jid):
            print(
                f"  Joystick {jid} ({glfw.get_joystick_guid(jid)}) has a gamepad mapping ({glfw.get_gamepad_name(jid)})"
            )
        else:
            print(
                f"  Joystick {jid} ({glfw.get_joystick_guid(jid)}) has no gamepad mapping"
            )
    else:
        print(
            f"{counter:08x} at {glfw.get_time():0.3f}: Joystick {jid} was disconnected"
        )

    counter += 1


def main():
    glfw.set_error_callback(error_callback)

    if not glfw.init():
        exit(-1)

    print("Library initialized")

    glfw.set_monitor_callback(monitor_callback)
    glfw.set_joystick_callback(joystick_callback)

    count = 3
    monitor = None
    # while ((ch = getopt(argc, argv, "hfn:")) != -1)
    # {
    #         switch (ch)
    #     {
    #         case 'h': \
    #             usage()
    #             exit(EXIT_SUCCESS)
    #
    #         case 'f': \
    #             monitor = glfwGetPrimaryMonitor()
    #             break
    #
    #         case 'n':
    #             count = (int) strtoul(optarg, NULL, 10)
    #             break
    #
    #         default:
    #             usage()
    #             exit(EXIT_FAILURE)
    #     }
    # }

    if monitor is not None:
        mode = glfw.get_video_mode(monitor)

        glfw.window_hint(glfw.REFRESH_RATE, mode.refresh_rate)
        glfw.window_hint(glfw.RED_BITS, mode.red_bits)
        glfw.window_hint(glfw.GREEN_BITS, mode.green_bits)
        glfw.window_hint(glfw.BLUE_BITS, mode.blue_bits)

        width = mode.width
        height = mode.height
    else:
        width = 640
        height = 480

    slots = []

    for i in range(count):
        slot = Slot(0, i + 1, glfw.TRUE)

        title: str = f"Event Linter (Window {slot.number})"

        if monitor is not None:
            print(
                f"Creating full screen window {slot.number} ({width}x{height} on {glfw.get_monitor_name(monitor)})"
            )
        else:
            print(f"Creating windowed mode window {slot.number} ({width}x{height})")

        slot.window = glfw.create_window(width, height, title, monitor, None)
        if not slot.window:
            glfw.terminate()
            exit(-1)

        glfw.set_window_user_pointer(slot.window, slot)

        glfw.set_window_pos_callback(slot.window, window_pos_callback)
        glfw.set_window_size_callback(slot.window, window_size_callback)
        glfw.set_framebuffer_size_callback(slot.window, framebuffer_size_callback)
        glfw.set_window_content_scale_callback(
            slot.window, window_content_scale_callback
        )
        glfw.set_window_close_callback(slot.window, window_close_callback)
        glfw.set_window_refresh_callback(slot.window, window_refresh_callback)
        glfw.set_window_focus_callback(slot.window, window_focus_callback)
        glfw.set_window_iconify_callback(slot.window, window_iconify_callback)
        glfw.set_window_maximize_callback(slot.window, window_maximize_callback)
        glfw.set_mouse_button_callback(slot.window, mouse_button_callback)
        glfw.set_cursor_pos_callback(slot.window, cursor_position_callback)
        glfw.set_cursor_enter_callback(slot.window, cursor_enter_callback)
        glfw.set_scroll_callback(slot.window, scroll_callback)
        glfw.set_key_callback(slot.window, key_callback)
        glfw.set_char_callback(slot.window, char_callback)
        glfw.set_drop_callback(slot.window, drop_callback)

        glfw.make_context_current(slot.window)
        # gladLoadGL(glfwGetProcAddress)
        glfw.swap_interval(1)

        slots.append(slot)

    print("Main loop starting")

    while True:
        index = 0
        for i, slot in enumerate(slots):
            index = i + 1
            if glfw.window_should_close(slot.window):
                break

        if index < count:
            break

        glfw.wait_events()

        # Workaround for an issue with msvcrt and mintty
        # fflush(stdout)

    # free(slots)
    glfw.terminate()
    exit(0)


if __name__ == "__main__":
    main()
