#!/usr/bin/python
import numpy as np

def construct(start_x, start_y, shape=''):
    command = shape.split(',')
    x_list = [start_x]
    y_list = [start_y]
    for each in command:
        select = each[0]
        len = float(each[1:])
        if select == 'x':
            start_x += len
        if select == 'y':
            start_y += len
        x_list += [start_x]
        y_list += [start_y]
    return x_list, y_list


def meander(total, xlen_list, ylen_list, radius):
    command = ''
    remain = total
    flag = True

    def draw(flag, remain, command, tag, sign):
        if tag == 'x':
            delta = xlen
        else:
            delta = ylen
        if flag:
            # remain -= abs(delta) + (np.pi / 2 - 2) * radius
            remain -= abs(delta)
            if remain > 0:
                command += f'{tag}{delta * sign},'
            else:
                command += f'{tag}{(remain + delta) * sign},'
                flag = False
        return flag, remain, command

    xlen = xlen_list[0]
    ylen = ylen_list[0]
    flag, remain, command = draw(flag, remain, command, tag='y', sign=1)
    flag, remain, command = draw(flag, remain, command, tag='x', sign=-1)
    xlen = xlen_list[1]
    ylen = ylen_list[1]
    flag, remain, command = draw(flag, remain, command, tag='y', sign=1)
    flag, remain, command = draw(flag, remain, command, tag='x', sign=1)

    while flag:
        flag, remain, command = draw(flag, remain, command, tag='y', sign=1)
        flag, remain, command = draw(flag, remain, command, tag='x', sign=-1)
        flag, remain, command = draw(flag, remain, command, tag='y', sign=1)
        flag, remain, command = draw(flag, remain, command, tag='x', sign=1)
    return command


def inductor(xpad, ypad, spacing, total, direction=1):
    global dx, dy, flag, remain, command, radius
    d = {}
    d.update({'x': 0})
    d.update({'y': 0})
    d.update({'r': []})
    radius = 0
    d['r'] += [radius]
    command = ''
    remain = total
    flag = True

    def draw(xpad, ypad, tag, sign):
        global dx, dy, flag, remain, command, radius
        if flag:
            if tag == 'x':
                xpad = xpad + spacing
                delta = xpad
            else:
                ypad = ypad + spacing
                delta = ypad
            remain -= delta
            if tag == 'y' and sign == 1:
                radius += spacing
            if remain < 500 and tag == 'x' and sign == -direction:
                command += f'{tag}{(delta / 2) * sign},'
                d[tag] += (delta / 2) * sign
                d['r'] += [spacing]
                flag = False
            else:
                command += f'{tag}{delta * sign},'
                d[tag] += delta * sign
                d['r'] += [radius]

        return xpad, ypad

    while flag:
        xpad, ypad = draw(xpad, ypad, tag='y', sign=1)
        xpad, ypad = draw(xpad, ypad, tag='x', sign=-1)
        xpad, ypad = draw(xpad, ypad, tag='y', sign=-1)
        xpad, ypad = draw(xpad, ypad, tag='x', sign=1)
    command += f'y{direction * 250}'
    d['y'] += direction * 250
    return command, -d['x'], -d['y'], d['r']