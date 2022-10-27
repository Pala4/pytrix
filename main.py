# -*- coding: utf-8 -*import

import sys
import subprocess
import time
import math

import keyboard as kbd

fild_width = 20
fild_height = 22
fild = [[' '] * fild_width for i in range(fild_height)]

glass_x_start = 1
glass_y_start = 0
glass_x_end = 10
glass_y_end = 19
glass_width = glass_x_end - glass_x_start + 1
glass_height = glass_y_end - glass_y_start + 1

z_shape_templ = [['@', '@', ' '],
                 [' ', '@', '@']]
s_shape_templ = [[' ', '#', '#'],
                 ['#', '#', ' ']]

heap = [[' '] * glass_width for i in range(glass_height)]


def clear_fild():
    fill_rect(0, 0, fild_width - 1, fild_height - 1, ' ')


def fill_rect(x_start, y_start, x_end, y_end, fill_s=''):
    x_start = 0 if x_start < 0 else x_start
    y_start = 0 if y_start < 0 else y_start
    x_end = fild_width - 1 if x_end > fild_width - 1 else x_end
    y_end = fild_height - 1 if y_end > fild_height - 1 else y_end
    if x_start > x_end:
        x_start, x_end = x_end, x_start
    if y_start > y_end:
        y_start, y_end = y_end, y_start
    for row in range(y_start, y_end + 1):
        for col in range(x_start, x_end + 1):
            fild[row][col] = fill_s


def draw_v_line(x, y_start, y_end, fill_s=''):
    if x < 0 or x > fild_width - 1:
        return
    y_start = 0 if y_start < 0 else y_start
    y_start = fild_height - 1 if y_start > fild_height - 1 else y_start
    y_end = 0 if y_end < 0 else y_end
    y_end = fild_height - 1 if y_end > fild_height - 1 else y_end
    if y_start > y_end:
        y_start, y_end = y_end, y_start
    for y in range(y_start, y_end + 1):
        fild[y][x] = fill_s


def draw_h_line(y, x_start, x_end, fill_s=''):
    if y < 0 or y > fild_height - 1:
        return
    x_start = 0 if x_start < 0 else x_start
    x_start = fild_width - 1 if x_start > fild_width - 1 else x_start
    x_end = 0 if x_end < 0 else x_end
    x_end = fild_width - 1 if x_end > fild_width - 1 else x_end
    if x_start > x_end:
        x_start, x_end = x_end, x_start
    for x in range(x_start, x_end + 1):
        fild[y][x] = fill_s


def clear_glass():
    fill_rect(glass_x_start, glass_y_start, glass_x_end, glass_y_end, ' ')


def draw_shape(shape, x, y, angle=1.57):
    for id_y in range(len(shape)):
        for id_x in range(len(shape[id_y])):
            if shape[id_y][id_x] != ' ':
                fild[y + round(id_x*math.sin(angle) + id_y*math.cos(angle))][x + round(id_x*math.cos(angle) - id_y*math.sin(angle))] = shape[id_y][id_x]


def put_shape_to_heap(x, y, shape):
    for id_y in range(len(shape)):
        for id_x in range(len(shape[id_y])):
            if shape[id_y][id_x] != ' ':
                heap[y + id_y][x + id_x - 1] = shape[id_y][id_x]


def draw_heap():
    for row in range(glass_y_start, glass_y_end + 1):
        for col in range(glass_x_start, glass_x_end + 1):
            if heap[row - glass_y_start][col - glass_x_start] != ' ':
                fild[row][col] = heap[row - glass_y_start][col - glass_x_start]


def collide_x(cur_x, new_x, cur_y, shape):
    if cur_x - new_x > 0:
        for id_y in range(len(shape)):
            if shape[id_y][0] != ' ':
                if fild[cur_y + id_y][new_x] != ' ':
                    return True
    elif new_x - cur_x > 0:
        for id_y in range(len(shape)):
            if shape[id_y][len(shape[id_y]) - 1] != ' ':
                if fild[cur_y + id_y][new_x + len(shape[id_y]) - 1] != ' ':
                    return True
    return False


def collide_y(cur_x, cur_y, new_y, shape):
    if cur_y - new_y > 0:
        for id_x in range(len(shape[0])):
            if shape[0][id_x] != ' ':
                if fild[new_y][cur_x + id_x] != ' ':
                    return True
    elif new_y - cur_y > 0:
        for id_x in range(len(shape[len(shape) - 1])):
            if shape[len(shape) - 1][id_x] != ' ':
                if fild[new_y + len(shape) - 1][cur_x + id_x] != ' ':
                    return True
    return False


if sys.platform.startswith("win"):
    def clear_screen():
        subprocess.call(["cmd.exe", "/C", "cls"])
else:
    def clear_screen():
        subprocess.call(["clear"])


def render():
    clear_screen()
    for row in fild:
        for col in row:
            print(col, end='')
        print('')


def time_delta(time_start):
    return int((time.perf_counter_ns() - time_start)/1000000)


if __name__ == '__main__':
    clear_fild()
    draw_v_line(0, 0, 20, '│')
    draw_v_line(11, 0, 20, '│')
    draw_h_line(20, 0, 0, '└')
    draw_h_line(20, 11, 11, '┘')
    draw_h_line(20, 1, 10, '─')

    cur_shape = list()
    new_y_pos = 0
    y_pos = new_y_pos
    new_x_pos = 5
    x_pos = new_x_pos
    next_figure = True
    update_kb_pos_time_start = time.perf_counter_ns()
    change_y_pos_time_start = time.perf_counter_ns()
    key = ''
    rend = True
    while True:
        if next_figure:
            cur_shape = z_shape_templ
            next_figure = False
            new_y_pos = 0
            y_pos = new_y_pos
            new_x_pos = 5
            x_pos = new_x_pos

        if key == '':
            key = kbd.scan_key()
        if time_delta(update_kb_pos_time_start) >= 50:
            if key != '':
                if key == kbd.KEY_LEFT:
                    new_x_pos -= 1
                if key == kbd.KEY_RIGHT:
                    new_x_pos += 1
                if key == kbd.KEY_DOWN:
                    new_y_pos += 1
                if key == kbd.KEY_UP:
                    pass
                if key == 'q':
                    break
                rend = True
                key = ''
                kbd.flush()
            update_kb_pos_time_start = time.perf_counter_ns()

        if time_delta(change_y_pos_time_start) >= 1000:
            new_y_pos += 1
            change_y_pos_time_start = time.perf_counter_ns()
            rend = True

        is_collide_x = False
        if collide_x(x_pos, new_x_pos, new_y_pos, cur_shape):
            new_x_pos = x_pos
            is_collide_x = True

        is_collide_y = False
        if collide_y(x_pos, y_pos, new_y_pos, cur_shape):
            new_y_pos = y_pos
            is_collide_y = True

        if is_collide_y:
            put_shape_to_heap(x_pos, y_pos, cur_shape)
            next_figure = True

        x_pos = new_x_pos
        y_pos = new_y_pos

        if rend:
            clear_glass()
            if not next_figure:
                draw_shape(cur_shape, x_pos, y_pos)
            draw_heap()
            render()
            rend = False
