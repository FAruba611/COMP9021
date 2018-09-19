"""
COMP9021 Assignment 2
Author: Changfeng Li(z5137858)
Last modified: 2017.05.11
Version: 1.3
"""
'''
Desc: Finish polygon searching and analyses with no bug
'''

import os
import sys
import copy
import math
import argparse

class colors:
    BLACK = '\033[0;30m'
    DARK_GRAY = '\033[1;30m'
    LIGHT_GRAY = '\033[0;37m'
    BLUE = '\033[0;34m'
    LIGHT_BLUE = '\033[1;34m'
    GREEN = '\033[0;32m'
    LIGHT_GREEN   = '\033[1;32m'
    CYAN          = '\033[0;36m'
    LIGHT_CYAN    = '\033[1;36m'
    RED           = '\033[0;31m'
    LIGHT_RED     = '\033[1;31m'
    PURPLE        = '\033[0;35m'
    LIGHT_PURPLE  = '\033[1;35m'
    BROWN         = '\033[0;33m'
    YELLOW        = '\033[1;33m'
    WHITE         = '\033[1;37m'
    DEFAULT_COLOR = '\033[00m'
    RED_BOLD      = '\033[01;31m'
    ENDC = '\033[0m'


def wrong_message_judgement(filename, case):
    # filename = args.filename.strip().split('.')
    fw = open(filename[0] + '_output.' + filename[1], 'w')
    if case == 1:
        print('Incorrect input.')
        fw.write('Incorrect input.\n')

    if case == 2:
        print('Cannot get polygons as expected.')
        fw.write('Cannot get polygons as expected.\n')
    fw.close()
    os._exit(0)


def read_txt_to_list(file_name):
    Grid = [[]for _ in range(100)]
    f_flag = 0
    s_flag = 0
    i_flag = 0
    wrong_flag = 0
    try:
        with open(file_name) as file:
            line_index = 0
            len_line_set = []
            i_flag = 0

            for line in file.readlines():
                for digit in line:
                    if digit.replace('.', '').replace('-', '').replace('\n', '').replace(' ', '').isdigit():
                        if int(digit) == 0 or int(digit) == 1:
                            i_flag = 1
                            Grid[line_index].append(int(digit))
                        else:
                            f_flag = 1

                    else:
                        if (ord(digit) >= 33 and ord(digit) <= 47) or (ord(digit) >= 58 and ord(digit) <= 126):
                            s_flag = 1
                line_index += 1

            Grid_final = [x[0] for x in zip(Grid) if x != ([],)]
            for elem in Grid_final:
                len_line_set.append(len(elem))
            len_line_1 = len_line_set[0]
            for item in len_line_set:
                if item != len_line_1:
                    wrong_flag = 1
                    break
            dim_height = len(Grid_final)
            dim_length = len(Grid_final[0])

            if f_flag == 1 or s_flag == 1:
                wrong_flag = 1
            if i_flag == 0 and os.path.getsize(file_name) != 0:
                wrong_flag = 1
            if dim_height < 2 or dim_height > 50 or dim_length < 2 or dim_length > 50:
                wrong_flag = 1
            if wrong_flag == 1:
                Grid_final = []
                wrong_message_judgement(file_name.strip().split('.'), 1)

    except FileNotFoundError:
        print('Incorrect input.')
        sys.exit()
    return dim_height, dim_length, Grid_final

# init dir set
def rejudge_set(rx,ry):
    if rx == 0 and ry == 0:
        dirset = ['NA', 'NA', '3:00_R', '4:30_RD', '6:00_D', 'NA', 'NA', 'NA']
    if rx == 0 and ry == dim_length - 1:
        dirset = ['NA', 'NA', 'NA', 'NA', '6:00_D', '7:30_LD', '9:00_L', 'NA']
    if rx == dim_height - 1 and ry == dim_length - 1:
        dirset = ['0:00_U', 'NA', 'NA', 'NA', 'NA', 'NA', '9:00_L', '10:30_LU']
    if rx == dim_height - 1 and ry == 0:
        dirset = ['0:00_U', '1:30_RU', '3:00_R', 'NA', 'NA', 'NA', 'NA', 'NA']
    if rx == 0 and ry > 0 and ry <= dim_length - 2:
        dirset = ['NA', 'NA', '3:00_R', '4:30_RD', '6:00_D', '7:30_LD', '9:00_L', 'NA']
    if ry == dim_length - 1 and rx > 0 and rx <= dim_height - 2:
        dirset = ['0:00_U', 'NA', 'NA', 'NA', '6:00_D', '7:30_LD', '9:00_L', '10:30_LU']
    if rx == dim_height - 1 and ry > 0 and ry <= dim_length - 2:
        dirset = ['0:00_U', '1:30_RU', '3:00_R', 'NA', 'NA', 'NA', '9:00_L', '10:30_LU']
    if ry == 0 and rx > 0 and rx <= dim_height - 2:
        dirset = ['0:00_U', '1:30_RU', '3:00_R', '4:30_RD', '6:00_D', 'NA', 'NA', 'NA']
    if ry > 0 and ry <= dim_length - 2 and rx > 0 and rx <= dim_height - 2:
        dirset = ['0:00_U', '1:30_RU', '3:00_R', '4:30_RD', '6:00_D', '7:30_LD', '9:00_L', '10:30_LU']
    return dirset

# frontier
def color_frontiers():
    global grid_footprints
    global grid_alley
    global O
    global re_judge

    find_polygon_count = 0
    current_color = 1
    Parameter_Polygon = dict()
    for index_x in range(dim_height):
        for index_y in range(dim_length):

            if grid_source[index_x][index_y] == 1:
                grid_footprints = copy.deepcopy(G)
                grid_alley = copy.deepcopy(G)
                O = []
                re_judge = 0

                current_color += 1
                start_position = [index_x, index_y]
                start_brush = '3:00_R'
                ct = 0
                
                frontier(start_position, start_brush, start_position, current_color, ct)
                
                find_polygon_count += 1
                Parameter_Polygon.update({current_color:O})

    kinds_of_different_color = find_polygon_count
    return Parameter_Polygon, kinds_of_different_color

# frontier recursive rules
def frontier(current_point, last_brush_dir, start_point, color, at_home_cnt):
    global grid_footprints
    global grid_alley
    current_x = current_point[0]
    current_y = current_point[1]
    start_x = start_point[0]
    start_y = start_point[1]
    grid_source[current_x][current_y] = color
    grid_footprints[current_x][current_y] = 'H'
    if start_x == current_x and start_y == current_y:
        at_home_cnt += 1

    # special case : corner
    # 1.left_up corner
    if current_x == 0 and current_y == 0:
        # c ?
        # ? ?
        dir_set = ['NA', 'NA', '3:00_R', '4:30_RD', '6:00_D', 'NA', 'NA', 'NA']
        finish_circle, current_brush_dir, current_point = search_polygon(current_x, current_y,
                                                                         last_brush_dir, start_x, start_y, color, at_home_cnt, *dir_set)
        if finish_circle:
            return
        frontier(current_point, current_brush_dir, start_point, color, at_home_cnt)

    # 2.right_up corner
    if current_x == 0 and current_y == dim_length - 1:
        # ? c
        # ? ?
        dir_set = ['NA', 'NA', 'NA', 'NA', '6:00_D', '7:30_LD', '9:00_L', 'NA']
        finish_circle, current_brush_dir, current_point = search_polygon(current_x, current_y,
                                                                         last_brush_dir, start_x, start_y, color, at_home_cnt, *dir_set)
        if finish_circle:
            return
        frontier(current_point, current_brush_dir, start_point, color, at_home_cnt)

    # 3.right_down corner
    if current_x == dim_height - 1 and current_y == dim_length - 1:
        # ? ?
        # ? c
        dir_set = ['0:00_U', 'NA', 'NA', 'NA', 'NA', 'NA', '9:00_L', '10:30_LU']
        finish_circle, current_brush_dir, current_point = search_polygon(current_x, current_y,
                                                                         last_brush_dir, start_x, start_y, color, at_home_cnt, *dir_set)
        if finish_circle:
            return
        frontier(current_point, current_brush_dir, start_point, color, at_home_cnt)

    # 4.left_down corner
    if current_x == dim_height - 1 and current_y == 0:
        # ? ?
        # c ?
        dir_set = ['0:00_U', '1:30_RU', '3:00_R', 'NA', 'NA', 'NA', 'NA', 'NA']
        finish_circle, current_brush_dir, current_point = search_polygon(current_x, current_y,
                                                                         last_brush_dir, start_x, start_y, color, at_home_cnt, *dir_set)
        if finish_circle:
            return
        frontier(current_point, current_brush_dir, start_point, color, at_home_cnt)

    # special case : top bottom right left line
    # 1.top
    if current_x == 0 and current_y > 0 and current_y <= dim_length - 2:
        # ? c ?
        # ? ? ?
        dir_set = ['NA', 'NA', '3:00_R', '4:30_RD', '6:00_D', '7:30_LD', '9:00_L', 'NA']
        finish_circle, current_brush_dir, current_point = search_polygon(current_x, current_y,
                                                                         last_brush_dir, start_x, start_y, color, at_home_cnt, *dir_set)
        if finish_circle:
            return
        frontier(current_point, current_brush_dir, start_point, color, at_home_cnt)

    # 2.right
    if current_y == dim_length - 1 and current_x > 0 and current_x <= dim_height - 2:
        # ? ?
        # ? c
        # ? ?
        dir_set = ['0:00_U', 'NA', 'NA', 'NA', '6:00_D', '7:30_LD', '9:00_L', '10:30_LU']
        finish_circle, current_brush_dir, current_point = search_polygon(current_x, current_y,
                                                                         last_brush_dir, start_x, start_y, color, at_home_cnt, *dir_set)
        if finish_circle:
            return
        frontier(current_point, current_brush_dir, start_point, color, at_home_cnt)

    # 3.bottom
    if current_x == dim_height - 1 and current_y > 0 and current_y <= dim_length - 2:
        # ? ? ?
        # ? c ?
        dir_set = ['0:00_U', '1:30_RU', '3:00_R', 'NA', 'NA', 'NA', '9:00_L', '10:30_LU']
        finish_circle, current_brush_dir, current_point = search_polygon(current_x, current_y,
                                                                         last_brush_dir, start_x, start_y, color, at_home_cnt, *dir_set)
        if finish_circle:
            return
        frontier(current_point, current_brush_dir, start_point, color, at_home_cnt)

    # 4.left
    if current_y == 0 and current_x > 0 and current_x <= dim_height - 2:
        # ? ?
        # c ?
        # ? ?
        dir_set = ['0:00_U', '1:30_RU', '3:00_R', '4:30_RD', '6:00_D', 'NA', 'NA', 'NA']
        finish_circle, current_brush_dir, current_point = search_polygon(current_x, current_y,
                                                                         last_brush_dir, start_x, start_y, color, at_home_cnt, *dir_set)
        if finish_circle:
            return
        frontier(current_point, current_brush_dir, start_point, color, at_home_cnt)

    # normal case:
    if current_y > 0 and current_y <= dim_length - 2 and current_x > 0 and current_x <= dim_height - 2:

        dir_set = ['0:00_U', '1:30_RU', '3:00_R', '4:30_RD', '6:00_D', '7:30_LD', '9:00_L', '10:30_LU']
        finish_circle, current_brush_dir, current_point = search_polygon(current_x, current_y,
                                                                         last_brush_dir, start_x, start_y, color, at_home_cnt, *dir_set)
        if finish_circle:
            return
        frontier(current_point, current_brush_dir, start_point, color, at_home_cnt)

# compass searching polygons
def search_polygon(current_x, current_y, last_brush_dir, start_x, start_y, color, at_home_cnt, *prescribed_dir_set):
    # case: LOOP TERMINAL
    global grid_alley
    global tup
    dir_set = [*prescribed_dir_set]
    if last_brush_dir == 'LOOP' or last_brush_dir == 'TERMINAL':
        grid_source[current_x][current_y] = 1
        grid_alley[current_x][current_y] = 'J'
        backtracking(color, start_x, start_y)
        _last_brush_dir = tup[0]
        r_x = tup[1]
        r_y = tup[2]
        
        dir_set = rejudge_set(r_x, r_y)
        end, terminal, loop, current_brush_dir, next_x, next_y \
            = direction_position_update(r_x, r_y, _last_brush_dir, start_x, start_y, color,
                                        at_home_cnt, *dir_set)
        current_point = [r_x, r_y]
        
        return 0, current_brush_dir, current_point
    # case: NORMAL
    if last_brush_dir != 'LOOP' and last_brush_dir != 'TERMINAL':
        end, terminal, loop, current_brush_dir, next_x, next_y \
            = direction_position_update(current_x, current_y, last_brush_dir, start_x, start_y, color,
                                        at_home_cnt, *dir_set)
        current_point = [next_x, next_y]
        
        if current_brush_dir == 'END' and current_x == start_x and current_y == start_y and at_home_cnt >= 2:
            grid_source[current_x][current_y] = color
            
            return 1, current_brush_dir, current_point

        return 0, current_brush_dir, current_point

def set_param(x_cur, y_cur, x_s, y_s, cur_color, end_flag, keyn, dirn, Dic):
    global grid_source
    global grid_footprints
    global grid_alley
    if x_cur == x_s and y_cur == y_s:
        grid_source[x_cur][y_cur] = cur_color
        grid_footprints[x_cur][y_cur] = 1

    if (grid_source[x_cur][y_cur] == 1 or grid_source[x_cur][y_cur] == cur_color) and end_flag == 0:
        if grid_alley[x_cur][y_cur] != 'J' and grid_footprints[x_cur][y_cur] != 'H':

            Dic.update({keyn: [x_cur, y_cur, dirn]})
    terminal_flag = 0
    find_end_flag = 1
    return terminal_flag, find_end_flag, Dic

# update compass direction
def direction_position_update(x, y, _last_brush_dir, start_x, start_y, current_color, count, *prescribed_dir_set):
    global O
    global grid_source
    global grid_footprints
    global grid_alley
    x_s = start_x
    y_s = start_y
    Direction_Position = {}
    end_flag = 0
    loop_flag = 0
    terminal_flag = 0
    node_flag = 0
    find_end_flag = 0
    dir_search_set = [*prescribed_dir_set]
    if x == x_s and y == y_s and count>=2:
        end_flag = 1

    for item in O:
        if [x, y] in item and end_flag == 0:
            loop_flag = 1
            break

    if _last_brush_dir == '0:00_U':
        # (Up)
        if dir_search_set[0] == '0:00_U':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x-1, y, x_s, y_s, current_color, end_flag, 0, '0:00_U', Direction_Position)

        # (Right Up)
        if dir_search_set[1] == '1:30_RU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y + 1, x_s, y_s, current_color, end_flag, 1, '1:30_RU', Direction_Position)

        # (Right)
        if dir_search_set[2] == '3:00_R':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y + 1, x_s, y_s, current_color, end_flag, 2, '3:00_R', Direction_Position)

        # (Right Down)
        if dir_search_set[3] == '4:30_RD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y + 1, x_s, y_s, current_color, end_flag, 3, '4:30_RD', Direction_Position)

        # (Left Down)
        if dir_search_set[5] == '7:30_LD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y - 1, x_s, y_s, current_color, end_flag, -3, '7:30_LD', Direction_Position)

        # (Left)
        if dir_search_set[6] == '9:00_L':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y - 1, x_s, y_s, current_color, end_flag, -2, '9:00_L', Direction_Position)

        # (Left Up)
        if dir_search_set[7] == '10:30_LU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y - 1, x_s, y_s, current_color, end_flag, -1, '10:30_LU', Direction_Position)

        # (No Down)
        if dir_search_set[4] == '6:00_D':
            if (grid_footprints[x + 1][y]) == 'H' and loop_flag == 0 and find_end_flag!=1:
                terminal_flag = 1

    if _last_brush_dir == '1:30_RU':
        # (Up)
        if dir_search_set[0] == '0:00_U':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y, x_s, y_s, current_color, end_flag, -1, '0:00_U', Direction_Position)

        # (Right Up)
        if dir_search_set[1] == '1:30_RU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y + 1, x_s, y_s, current_color, end_flag, 0, '1:30_RU', Direction_Position)

        # (Right)
        if dir_search_set[2] == '3:00_R':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y + 1, x_s, y_s, current_color, end_flag, 1, '3:00_R', Direction_Position)

        # (Right Down)
        if dir_search_set[3] == '4:30_RD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y + 1, x_s, y_s, current_color, end_flag, 2, '4:30_RD', Direction_Position)

        # (Down)
        if dir_search_set[4] == '6:00_D':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y, x_s, y_s, current_color, end_flag, 3, '6:00_D', Direction_Position)

        # (Left)
        if dir_search_set[6] == '9:00_L':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y-1, x_s, y_s, current_color, end_flag, -3, '9:00_L', Direction_Position)

        # (Left Up)
        if dir_search_set[7] == '10:30_LU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y - 1, x_s, y_s, current_color, end_flag, -2, '10:30_LU', Direction_Position)

        # (No Left Down)
        if dir_search_set[5] == '7:30_LD' and loop_flag == 0 and find_end_flag != 1:
            if (grid_footprints[x + 1][y - 1]) == 'H':
                terminal_flag = 1

    if _last_brush_dir == '3:00_R':
        # (Up)
        if dir_search_set[0] == '0:00_U':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y, x_s, y_s, current_color, end_flag, -2, '0:00_U', Direction_Position)

        # (Right Up)
        if dir_search_set[1] == '1:30_RU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y + 1, x_s, y_s, current_color, end_flag, -1, '1:30_RU', Direction_Position)

        # (Right)
        if dir_search_set[2] == '3:00_R':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y + 1, x_s, y_s, current_color, end_flag, 0, '3:00_R', Direction_Position)

        # (Right Down)
        if dir_search_set[3] == '4:30_RD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y + 1, x_s, y_s, current_color, end_flag, 1, '4:30_RD', Direction_Position)

        # (Down)
        if dir_search_set[4] == '6:00_D':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y, x_s, y_s, current_color, end_flag, 2, '6:00_D', Direction_Position)

        # (Left Down)
        if dir_search_set[5] == '7:30_LD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y - 1, x_s, y_s, current_color, end_flag, 3, '7:30_LD', Direction_Position)

        # (Left Up)
        if dir_search_set[7] == '10:30_LU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y - 1, x_s, y_s, current_color, end_flag, -3, '10:30_LU', Direction_Position)

        # (No Left)
        if dir_search_set[6] == '9:00_L':
            if (grid_footprints[x][y - 1]) == 'H' and loop_flag == 0 and find_end_flag!=1:
                terminal_flag = 1

    if _last_brush_dir == '4:30_RD':
        # (Up)
        if dir_search_set[0] == '0:00_U':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y, x_s, y_s, current_color, end_flag, -3, '0:00_U', Direction_Position)

        # (Right Up)
        if dir_search_set[1] == '1:30_RU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y + 1, x_s, y_s, current_color, end_flag, -2, '1:30_RU', Direction_Position)

        # (Right)
        if dir_search_set[2] == '3:00_R':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y + 1, x_s, y_s, current_color, end_flag, -1, '3:00_R', Direction_Position)

        # (Right Down)
        if dir_search_set[3] == '4:30_RD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y + 1, x_s, y_s, current_color, end_flag, 0, '4:30_RD', Direction_Position)

        # (Down)
        if dir_search_set[4] == '6:00_D':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y, x_s, y_s, current_color, end_flag, 1, '6:00_D', Direction_Position)

        # (Left Down)
        if dir_search_set[5] == '7:30_LD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y - 1, x_s, y_s, current_color, end_flag, 2, '7:30_LD', Direction_Position)

        # (Left)
        if dir_search_set[6] == '9:00_L':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y - 1, x_s, y_s, current_color, end_flag, 3, '9:00_L', Direction_Position)

        # (No Left Up)
        if dir_search_set[7] == '10:30_LU':
            if (grid_footprints[x - 1][y - 1]) == 'H' and loop_flag == 0 and find_end_flag!=1:
                terminal_flag = 1

    if _last_brush_dir == '6:00_D':

        # (Right Up)
        if dir_search_set[1] == '1:30_RU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y + 1, x_s, y_s, current_color, end_flag, -3, '1:30_RU', Direction_Position)

        # (Right)
        if dir_search_set[2] == '3:00_R':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y + 1, x_s, y_s, current_color, end_flag, -2, '3:00_R', Direction_Position)

        # (Right Down)
        if dir_search_set[3] == '4:30_RD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y + 1, x_s, y_s, current_color, end_flag, -1, '4:30_RD', Direction_Position)

        # (Down)
        if dir_search_set[4] == '6:00_D':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y, x_s, y_s, current_color, end_flag, 0, '6:00_D', Direction_Position)

        # (Left Down)
        if dir_search_set[5] == '7:30_LD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y - 1, x_s, y_s, current_color, end_flag, 1, '7:30_LD', Direction_Position)

        # (Left)
        if dir_search_set[6] == '9:00_L':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y - 1, x_s, y_s, current_color, end_flag, 2, '9:00_L', Direction_Position)

        # (Left Up)
        if dir_search_set[7] == '10:30_LU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y - 1, x_s, y_s, current_color, end_flag, 3, '10:30_LU', Direction_Position)

        # (No Up)
        if dir_search_set[0] == '0:00_U':
            if (grid_footprints[x - 1][y]) == 'H' and loop_flag == 0 and find_end_flag!=1:
                terminal_flag = 1

    if _last_brush_dir == '7:30_LD':
        # (Up)
        if dir_search_set[0] == '0:00_U':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y, x_s, y_s, current_color, end_flag, 3, '0:00_U', Direction_Position)

        # (Right)
        if dir_search_set[2] == '3:00_R':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y + 1, x_s, y_s, current_color, end_flag, -3, '3:00_R', Direction_Position)

        # (Right Down)
        if dir_search_set[3] == '4:30_RD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y + 1, x_s, y_s, current_color, end_flag, -2, '4:30_RD', Direction_Position)

        # (Down)
        if dir_search_set[4] == '6:00_D':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y, x_s, y_s, current_color, end_flag, -1, '6:00_D', Direction_Position)

        # (Left Down)
        if dir_search_set[5] == '7:30_LD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y - 1, x_s, y_s, current_color, end_flag, 0, '7:30_LD', Direction_Position)

        # (Left)
        if dir_search_set[6] == '9:00_L':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y - 1, x_s, y_s, current_color, end_flag, 1, '9:00_L', Direction_Position)

        # (Left Up)
        if dir_search_set[7] == '10:30_LU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y - 1, x_s, y_s, current_color, end_flag, 2, '10:30_LU', Direction_Position)

        # (No Right Up)
        if dir_search_set[1] == '1:30_RU':
            if (grid_footprints[x - 1][y + 1]) == 'H' and loop_flag == 0 and find_end_flag!=1:
                terminal_flag = 1

    if _last_brush_dir == '9:00_L':
        # (Up)
        if dir_search_set[0] == '0:00_U':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y, x_s, y_s, current_color, end_flag, 2, '0:00_U', Direction_Position)

        # (Right Up)
        if dir_search_set[1] == '1:30_RU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y + 1, x_s, y_s, current_color, end_flag, 3, '1:30_RU', Direction_Position)


        # (Right Down)
        if dir_search_set[3] == '4:30_RD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y + 1, x_s, y_s, current_color, end_flag, -3, '4:30_RD', Direction_Position)

        # (Down)
        if dir_search_set[4] == '6:00_D':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y, x_s, y_s, current_color, end_flag, -2, '6:00_D', Direction_Position)

        # (Left Down)
        if dir_search_set[5] == '7:30_LD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y - 1, x_s, y_s, current_color, end_flag, -1, '7:30_LD', Direction_Position)

        # (Left)
        if dir_search_set[6] == '9:00_L':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y - 1, x_s, y_s, current_color, end_flag, 0, '9:00_L', Direction_Position)

        # (Left Up)
        if dir_search_set[7] == '10:30_LU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y - 1, x_s, y_s, current_color, end_flag, 1, '10:30_LU', Direction_Position)

        # (No Right)
        if dir_search_set[5] == '3:00_R':
            if (grid_footprints[x][y + 1]) == 'H' and loop_flag == 0 and find_end_flag!=1:
                terminal_flag = 1

    if _last_brush_dir == '10:30_LU':
        # (Up)
        if dir_search_set[0] == '0:00_U':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y, x_s, y_s, current_color, end_flag, 1, '0:00_U', Direction_Position)


        # (Right Up)
        if dir_search_set[1] == '1:30_RU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y + 1, x_s, y_s, current_color, end_flag, 2, '1:30_RU', Direction_Position)

        # (Right)
        if dir_search_set[2] == '3:00_R':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y + 1, x_s, y_s, current_color, end_flag, 3, '3:00_R', Direction_Position)

        # (Down)
        if dir_search_set[4] == '6:00_D':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y, x_s, y_s, current_color, end_flag, -3, '6:00_D', Direction_Position)

        # (Left Down)
        if dir_search_set[5] == '7:30_LD':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x + 1, y - 1, x_s, y_s, current_color, end_flag, -2, '7:30_LD', Direction_Position)

        # (Left)
        if dir_search_set[6] == '9:00_L':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x, y - 1, x_s, y_s, current_color, end_flag, -1, '9:00_L', Direction_Position)

        # (Left Up)
        if dir_search_set[7] == '10:30_LU':
            terminal_flag, find_end_flag, Direction_Position = \
                set_param(x - 1, y - 1, x_s, y_s, current_color, end_flag, 0, '10:30_LU', Direction_Position)

        # (No Right Down)
        if dir_search_set[5] == '4:30_RD':
            if (grid_footprints[x + 1][y + 1]) == 'H' and loop_flag == 0 and find_end_flag!=1:
                terminal_flag = 1

    # ====== ------ ++++++
    if len(Direction_Position) == 0:
        if loop_flag ==0 and end_flag == 0:
            terminal_flag = 1
        position_temp = [x, y]

    if len(Direction_Position) >= 1:
        if len(Direction_Position) >= 2:
            node_flag = 1
        #D.append([[x, y], sorted(Direction_Position.items(), key=lambda d: d[0], reverse=True)])
        most_outward_direction = min(list(Direction_Position.keys()))
        position_temp = Direction_Position[most_outward_direction][0:2]
        dir_temp = Direction_Position[most_outward_direction][2]
        O.append(([_last_brush_dir, [x, y], node_flag, dir_temp]))

    if end_flag == 1:
        return end_flag,terminal_flag,loop_flag, 'END', x_s , y_s

    if terminal_flag == 1 and len(Direction_Position) == 0:
        terminal_flag = 2
        dir_temp = 'TERMINAL'
        if x == x_s and y == y_s: #point
            wrong_message_judgement(args.filename, 2)
        else:
            O.append(([_last_brush_dir, [x, y], node_flag, dir_temp]))
        return end_flag, terminal_flag, loop_flag, dir_temp, position_temp[0], position_temp[1]

    if loop_flag == 1:
        if len(Direction_Position) == 0:
            dir_temp = 'LOOP'
        else:
            loop_flag = 0
        return end_flag, terminal_flag, loop_flag, dir_temp, position_temp[0], position_temp[1]

    if end_flag == 0:
        return end_flag, terminal_flag, loop_flag, dir_temp, position_temp[0], position_temp[1]

# back track to tag point
def backtracking(current_color, x_s, y_s):
    global re_judge
    global tup
    global grid_source
    global grid_footprints
    global grid_alley
    re_judge = 0
    tup = ['3:00_R', 0, 0]
    O.pop(-1)
    current_x = O[-1][1][0]
    current_y = O[-1][1][1]
    if O[-1][2] == 1:
        re_judge = 1
        grid_source[current_x][current_y] = current_color
        brush_dir = O[-1][0]
        tup = [brush_dir, current_x, current_y]
        return
    else:
        grid_source[current_x][current_y] = 1
        grid_alley[current_x][current_y] = 'J'
        if current_x == x_s and current_y == y_s and re_judge == 0:
            wrong_message_judgement(args.filename, 2)
        backtracking(current_color, x_s, y_s)

# cal vertex
def get_vertex(polygon):
    i = 0
    vertex = []
    while i < len(polygon):
        vertex_flag = 0
        if i == len(polygon) - 1:
            former_x = polygon[i - 1][0]
            former_y = polygon[i - 1][1]
            current_x = polygon[i][0]
            current_y = polygon[i][1]
            latter_x = polygon[0][0]
            latter_y = polygon[0][1]
        # a[-1] is the last element in list a
        else:
            former_x = polygon[i - 1][0]
            former_y = polygon[i - 1][1]
            current_x = polygon[i][0]
            current_y = polygon[i][1]
            latter_x = polygon[i + 1][0]
            latter_y = polygon[i + 1][1]
        if latter_x - current_x == -1 and latter_y - current_y == 0:
            if former_x - current_x != -1 or former_y - current_y != 0:
                vertex_flag = 1
        if latter_x - current_x == -1 and latter_y - current_y == 1:
            if current_x - former_x != -1 or current_y - former_y != 1:
                vertex_flag = 1
        if latter_x - current_x == 0 and latter_y - current_y == 1:
            if current_x - former_x != 0 or current_y - former_y != 1:
                vertex_flag = 1
        if latter_x - current_x == 1 and latter_y - current_y == 1:
            if current_x - former_x != 1 or current_y - former_y != 1:
                vertex_flag = 1
        if latter_x - current_x == 1 and latter_y - current_y == 0:
            if current_x - former_x != 1 or current_y - former_y != 0:
                vertex_flag = 1
        if latter_x - current_x == 1 and latter_y - current_y == -1:
            if current_x - former_x != 1 or current_y - former_y != -1:
                vertex_flag = 1
        if latter_x - current_x == 0 and latter_y - current_y == -1:
            if current_x - former_x != 0 or current_y - former_y != -1:
                vertex_flag = 1
        if latter_x - current_x == -1 and latter_y - current_y == -1:
            if current_x - former_x != -1 or current_y - former_y != -1:
                vertex_flag = 1

        if vertex_flag == 1:
            vertex.append((current_x, current_y))
        i += 1
    return vertex

# cal area
def cal_area(polygon):
    len_p = len(polygon)
    area = 0.0
    p = polygon[:]
    p.reverse()
    for i in range(len_p):
        area += p[i][0] * 0.4 * p[(i + 1) % len_p][1] * 0.4 - p[(i + 1) % len_p][0] * 0.4 * p[i][1] * 0.4
    area *= 0.5
    return "%.2f" % area

# cal dep
def cal_depth(polygons_all, polygon_certain):
    global node
    global grid_source
    global nb_of_shapes
    eye_x = polygon_certain[0][0]
    eye_y = polygon_certain[0][1]
    depth = 0
    through = [0 for _ in range(nb_of_shapes)]
    sum_of_index_on_line = 0
    line_flag = 'NO'
    if eye_y == 0:
        depth = 0
    else:
        for sight in range(eye_y-1, -1, -1):
            if grid_source[eye_x][sight] != 0:
                current_polygon_value = grid_source[eye_x][sight]
                if (eye_x, sight) in polygons_all[current_polygon_value-2]:
                    current_point = (eye_x, sight)
                    current_index = polygons_all[current_polygon_value-2].index(current_point)
                    if sight == len(grid_source[0]) - 1:
                        next_index = 0
                        before_index = current_index - 1
                    else:
                        next_index = current_index + 1
                        if next_index >= len(polygons_all[current_polygon_value-2]):
                            next_index=0
                        before_index = current_index - 1

                    next_point = polygons_all[current_polygon_value - 2][next_index]
                    before_point = polygons_all[current_polygon_value - 2][before_index]
                    if (next_point[0] - current_point[0]) * (before_point[0] - current_point[0]) == 0:
                        line_flag = 'OK'
                        sum_of_index_on_line += (next_point[0] - current_point[0] + before_point[0] - current_point[0])
                        through[current_polygon_value-2] += 0

                    if (next_point[0] - current_point[0]) * (before_point[0] - current_point[0]) > 0:
                        if sum_of_index_on_line == 0 and line_flag == 'OK':
                            line_flag = 'NO'
                            through[current_polygon_value - 2] += 1
                        else:
                            line_flag = 'NO'
                            through[current_polygon_value - 2] += 0
                        through[current_polygon_value-2] += 0

                    if (next_point[0] - current_point[0]) * (before_point[0] - current_point[0]) < 0:
                        if sum_of_index_on_line == 0 and line_flag == 'OK':
                            line_flag = 'NO'
                            through[current_polygon_value - 2] += 1
                        else:
                            line_flag = 'NO'
                            through[current_polygon_value - 2] += 0
                        through[current_polygon_value-2] += 1

        for value in through:
            if value % 2 == 1:
                depth += 1
    return depth

# cal peri
def cal_perimeter(polygon):
    integer = 0
    decimal = 0
    len_p = len(polygon)
    for i in range(len_p):
        para_f = abs(polygon[i][0] - polygon[(i + 1) % len_p][0])
        para_b = abs(polygon[i][1] - polygon[(i + 1) % len_p][1])
        v_x = para_f + para_b
        if v_x == 1:
            integer += 0.4
        else:
            decimal += 1
    if integer == 0:
        return str(decimal) + "*sqrt(.32)"
    if decimal == 0:
        return "%.1f" % integer
    return "%.1f" % integer + " + " + str(decimal) + "*sqrt(.32)"

# jdg vertex
def is_convex(polygon):
    len_p = len(polygon)
    p = polygon[:]
    p.reverse()
    convex_flag = True
    for i in range(len_p):
        p0 = p[i]
        p1 = p[(i + 1) % len_p]
        p2 = p[(i + 2) % len_p]
        delta_20_0 = p2[0] - p0[0]
        delta_10_1 = p1[1] - p0[1]
        delta_10_0 = p1[0] - p0[0]
        delta_20_1 = p2[1] - p0[1]
        m_front = (delta_20_0) * (delta_10_1)
        m_behind = (delta_10_0) * (delta_20_1)

        point_reveals_not_convex = m_front - m_behind
        if point_reveals_not_convex > 0:
            convex_flag = False
            break
    if convex_flag:
        return 'yes'
    return 'no'

# jdg invariant
def invariant(polygon):
    d_inv = {}
    len_p = len(polygon)
    sample_x = 0.0
    sample_y = 0.0
    for i in range(len_p):
        sample_x += polygon[i][0]
        sample_y += polygon[i][1]
    sample_x = sample_x * 1.0 / len_p
    sample_y = sample_y * 1.0 / len_p
    for i in range(len_p):
        d_inv[(polygon[i][0] - sample_x, polygon[i][1] - sample_y)] = i
    invariant_flag = True

    # degree: 90
    for i in range(len_p):
        x = polygon[i][0] - sample_x
        y = polygon[i][1] - sample_y
        mirror_x = -y
        mirror_y = x
        if d_inv.get((mirror_x, mirror_y)) == None:
            invariant_flag = False
            break
    if invariant_flag:
        return 4

    # degree: 180
    invariant_flag = True
    for i in range(len_p):
        x = polygon[i][0] - sample_x
        y = polygon[i][1] - sample_y
        mirror_x = -x
        mirror_y = -y
        if d_inv.get((mirror_x, mirror_y)) == None:
            invariant_flag = False
            break
    if invariant_flag:
        return 2
    return 1

# filldraw latex formatting files
def filldraw(polygon_set, polygon, max_area, min_area):
    len_p = len(polygon)
    p = []
    p.append(polygon[0]); p.append(polygon[1])
    x = polygon[1][0] - polygon[0][0]
    y = polygon[1][1] - polygon[0][1]
    for i in range(len_p):
        new_x = polygon[(i + 1) % len_p][0] - polygon[i][0]
        new_y = polygon[(i + 1) % len_p][1] - polygon[i][1]
        if new_x == x and new_y == y:
            p.pop()
        else:
            x = new_x
            y = new_y
        if i == len_p - 1:
            break
        p.append(polygon[i + 1])
    area = float(cal_area(p))
    if max_area == min_area:
        ratio = 0
    else:
        ratio = int(round((max_area - area) / (max_area - min_area) * 100))
    s = '\\filldraw[fill=orange!' + str(ratio) + '!yellow] '
    for i in range(len(p)):
        s += '(' + str(p[i][1])+', ' + str(p[i][0]) + ') -- '
    dep = cal_depth(polygon_set, polygon)
    s += 'cycle;\n'
    return dep, s

# support function: display_grid(gri)
def display_grid(gri):
    for i in range(dim_height):
        print('    ', end='')
        for j in range(dim_length):
            if gri[i][j]!='H' and gri[i][j]!='J':
                if gri[i][j] < 4:
                    print(' {}'.format(colors.BLUE + '{}'.format(gri[i][j]) + colors.ENDC), end='') if gri[i][
                        j] else print(' *', end='')
                elif gri[i][j] < 7:
                    print(' {}'.format(colors.GREEN + '{}'.format(gri[i][j]) + colors.ENDC), end='') if gri[i][
                        j] else print(' *', end='')
                elif gri[i][j] < 10:
                    print(' {}'.format(colors.RED + '{}'.format(gri[i][j]) + colors.ENDC), end='') if gri[i][
                        j] else print(' *', end='')
                elif gri[i][j] < 13:
                    print('{}'.format(colors.CYAN + '{}'.format(gri[i][j]) + colors.ENDC), end='') if gri[i][
                        j] else print(' *', end='')
                elif gri[i][j] < 16:
                    print('{}'.format(colors.PURPLE + '{}'.format(gri[i][j]) + colors.ENDC), end='') if gri[i][
                        j] else print(' *', end='')
                elif gri[i][j] < 16:
                    print('{}'.format(colors.BROWN + '{}'.format(gri[i][j]) + colors.ENDC), end='') if gri[i][
                        j] else print(' *', end='')
                else:
                    print('{}'.format(colors.BLACK + '{}'.format(gri[i][j]) + colors.ENDC), end='') if gri[i][
                        j] else print(' *', end='')
            else:
                print(' {}'.format(gri[i][j]), end='') if gri[i][j] else print(' -', end='')
        print()
    print()

def deleteDuplicatedElementFromList(listA):
    # return list(set(listA))
    return sorted(set(listA), key=listA.index)

# --------- main part
parser = argparse.ArgumentParser()
parser.add_argument('-print', action = 'store_true', default=False, required = False)
parser.add_argument('--file', dest='filename', required = True)
args = parser.parse_args()

sys.setrecursionlimit(5000)

tup = []
O = []
rejudge = 0

dim_height, dim_length, G = read_txt_to_list(args.filename)

grid_source = copy.deepcopy(G)
grid_footprints = copy.deepcopy(G)
grid_alley = copy.deepcopy(G)
polygon_set, nb_of_shapes = color_frontiers()
polygon_coordinate = []
polygon = []
display_grid(grid_source)

for i in range(len(polygon_set)):
    for element in range(len(polygon_set[i+2])):
        polygon_coordinate.append(tuple(polygon_set[i+2][element][1]))
    polygon_coordinate_fix = deleteDuplicatedElementFromList(polygon_coordinate)
    polygon.append(polygon_coordinate_fix)
    polygon_coordinate = []

# ===============================
# TEX MODE
if args.print == True:
    filename = args.filename.strip().split('.')
    fw = open(filename[0] + '.tex', 'w')
    fw.write('\\documentclass[10pt]{article}\n')
    fw.write('\\usepackage{tikz}\n')
    fw.write('\\usepackage[margin=0cm]{geometry}\n')
    fw.write('\\pagestyle{empty}\n')
    fw.write('\n')
    fw.write('\\begin{document}\n')
    fw.write('\n')
    fw.write('\\vspace*{\\fill}\n')
    fw.write('\\begin{center}\n')
    fw.write('\\begin{tikzpicture}[x=0.4cm, y=-0.4cm, thick, brown]\n')
    fw.write('\\draw[ultra thick] ' + '(0, 0) -- ' + '(' + str(dim_length - 1) + ', 0) -- ' + '(' + str(dim_length - 1) + ', ' + str(dim_height - 1) + ') -- ' + '(0, ' + str(dim_height - 1) + ') -- cycle;\n')

    max_area = float(cal_area(polygon[0]))
    min_area = float(cal_area(polygon[0]))
    for i in range(len(polygon) - 1):
        max_area = max(max_area, float(cal_area(polygon[i])))
        min_area = min(min_area, float(cal_area(polygon[i])))

    dictionary_of_content_fill = {}
    max_dep = 0
    for i in range(len(polygon)):
        dep, s = filldraw(polygon, polygon[i], max_area, min_area)
        max_dep = max(max_dep, dep + 1)
        if dictionary_of_content_fill.get(dep) == None:
            dictionary_of_content_fill[dep] = []
        dictionary_of_content_fill[dep].append(s)

    for i in range(max_dep):
        fw.write('%Depth ' + str(i) + '\n')
        for j in range(len(dictionary_of_content_fill[i])):
            fw.write(dictionary_of_content_fill[i][j])
    fw.write('\\end{tikzpicture}\n')
    fw.write('\\end{center}\n')
    fw.write('\\vspace*{\\fill}\n')
    fw.write('\n')
    fw.write('\\end{document}\n')
    fw.close()
# TXT MODE
else:
    filename = args.filename.strip().split('.')
    fw = open(filename[0] + '_output.' + filename[1], 'w')
    for i in range(len(polygon)):
        #print("polygon {}".format(i + 1))
        fw.write('Polygon ' + str(i + 1) + ":\n")
        fw.write('    Perimeter: ' + cal_perimeter(polygon[i]) + "\n")
        fw.write('    Area: ' + str(cal_area(polygon[i])) + "\n")
        fw.write('    Convex: ' + is_convex(polygon[i]) + "\n")
        fw.write('    Nb of invariant rotations: ' + str(invariant(polygon[i])) + "\n")
        fw.write('    Depth: ' + str(cal_depth(polygon, polygon[i])) + "\n")
        # print('Polygon ' + str(i + 1) + ":")
        # print('    Perimeter: ' + cal_perimeter(polygon[i]))
        # print('    Area: ' + str(cal_area(polygon[i])))
        # print('    Convex: ' + is_convex(polygon[i]))
        # print('    Nb of invariant rotations: ' + str(invariant(polygon[i])))
        # print('    Depth: ' + str(cal_depth(polygon, polygon[i])))
    fw.close()

