# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#   explanation written by Björn Bergström of the FOV algorithm used here can
#   be found from:
#   http://roguebasin.roguelikedevelopment.org/index.php/
#   FOV_using_recursive_shadowcasting
#
#   original implementation by Eric D. Burgess is from:
#   http://roguebasin.roguelikedevelopment.org/index.php/
#   Python_shadowcasting_implementation

"""
Line of sight implementation
"""

from pyherc.data import level_size, blocks_los

mult = [[1,  0,  0, -1, -1,  0,  0,  1],
        [0,  1, -1,  0,  0, -1,  1,  0],
        [0,  1,  1,  0,  0, -1, -1,  0],
        [1,  0,  0,  1, -1,  0,  0, -1]]

#TODO: parametrize for vision and movement
def cast_light(cx, cy, row, start, end, radius, xx, xy, yx, yy, fov_matrix,
               level):
    """
    Recursive lightcasting function

    Returns:
        fov_matrix
    """
    if start < end:
        return
    radius_squared = radius*radius
    for j in range(row, radius+1):
        dx, dy = -j-1, -j
        blocked = False
        while dx <= 0:
            dx += 1
            # Translate the dx, dy coordinates into map coordinates:
            X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
            # l_slope and r_slope store the slopes of the left and right
            # extremities of the square we're considering:
            l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
            if start < r_slope:
                continue
            elif end > l_slope:
                break
            else:
                # Our light beam is touching this square; light it:
                if dx*dx + dy*dy < radius_squared:
                    #transform from map to light_matrix
                    fov_matrix[(X, Y)] = True
                if blocked:
                    # we're scanning a row of blocked squares:
                    if blocks_los(level, (X, Y)):
                        new_start = r_slope
                        continue
                    else:
                        blocked = False
                        start = new_start
                else:
                    if blocks_los(level, (X, Y)) and j < radius:
                        # This is a blocking square, start a child scan:
                        blocked = True
                        cast_light(cx, cy, j+1, start, l_slope,
                                   radius, xx, xy, yx, yy, fov_matrix, level)
                        new_start = r_slope
        # Row is scanned; do next row unless last square was blocked:
        if blocked:
            break

    return fov_matrix


def do_fov(x, y, radius, fov_matrix, level):
    """
    Calculate lit squares from the given location and radius
    """
    for oct in range(8):
        cast_light(x, y, 1, 1.0, 0.0, radius,
                   mult[0][oct], mult[1][oct],
                   mult[2][oct], mult[3][oct], fov_matrix, level)

    return fov_matrix


def get_fov_matrix(location, level, distance):
    """
    Calculate field of vision matrix

    :param location: center of fov calculation
    :type location: (int, int)
    :param level: level where fov is calculated
    :type level: Level
    :param distance: distance of vision
    :type distance: int
    :returns: matrix of True / False
    """
    fov_matrix = {}

    fov_matrix[location] = True

    return do_fov(location[0],
                  location[1], distance,
                  fov_matrix, level)
