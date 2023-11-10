import time
import curses

from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetPowerUsage, nvmlDeviceGetPowerManagementLimitConstraints

# Green -> Yellow -> Red
COLORS = [10, 2, 11, 3, 9, 1]


def moving_average(data, window_size):
    return [sum(data[i - window_size:i]) / window_size for i in range(window_size, len(data) + 1)]

def get_gpu_power(device):
    return nvmlDeviceGetPowerUsage(device) / 1000.0

def get_color(normalized_value):
    index = int(round(normalized_value * (len(COLORS) - 1)))
    if index < 0:
        index = 0
    elif index >= len(COLORS):
        index = len(COLORS) - 1
    return curses.color_pair(index + 1)

def draw_y_axis(window, max_power):
    try:
        max_y, _ = window.getmaxyx()
        y_axis_label = "Power (W)"
        window.addstr(0, 0, y_axis_label)

        max_tick_width = len(str(max_power))
        for i in range(0, max_power + 1, 50):
            y = max_y - int((i / max_power) * (max_y - 2)) - 1
            if y >= 0 and y <= max_y - 1:
                window.addstr(y, len(y_axis_label) + 1, str(i).rjust(max_tick_width))
        
        for y in range(max_y):
            window.addch(y, len(y_axis_label) + max_tick_width + 2, '|')
    except curses.error:
        pass

def main(window):
    nvmlInit()
    device = nvmlDeviceGetHandleByIndex(0)
    max_power = max(nvmlDeviceGetPowerManagementLimitConstraints(device)) // 1000

    # Initialize six colors from green to red
    curses.start_color()
    curses.use_default_colors()
    for i, color in enumerate(COLORS):
        curses.init_pair(i + 1, color, -1)

    window.nodelay(True)
    data = []
    max_y, max_x = window.getmaxyx()
    y_axis_offset = len("Power (W)") + len(str(max_power)) + 3
    window_size = 10

    while True:
        power = get_gpu_power(device)
        max_y, max_x = window.getmaxyx()
        data.append(power)
        if len(data) > max_x - 2 - y_axis_offset:
            data.pop(0)

        if len(data) < window_size:
            continue
        smoothed_data = moving_average(data, window_size)

        window.clear()
        draw_y_axis(window, max_power)

        for i in range(len(smoothed_data) - 1):
            x = i + y_axis_offset
            normalized_power = (smoothed_data[i] / max_power)
            y = max_y - int(normalized_power * (max_y - 1)) - 1
            try:
                if 0 <= x < max_x and 0 <= y < max_y:
                    window.addch(y, x, "*", get_color(normalized_power))
                elif 0 <= x < max_x:
                    if y < 0:
                        window.addch(0, x, "*", get_color(1.0))
                    else:
                        window.addch(max_y - 1, x, "*", get_color(0.0))
            except curses.error as e:
                if str(e) == "addch() returned ERR":
                    # Terminal resize event, continue to redraw the entire graph
                    continue

        window.refresh()
        time.sleep(0.2)


if __name__ == "__main__":
    curses.wrapper(main)
