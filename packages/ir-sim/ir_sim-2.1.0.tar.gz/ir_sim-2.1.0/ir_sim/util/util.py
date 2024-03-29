import os
import sys
from math import pi, atan2, sin, cos
import numpy as np
from shapely import ops

def file_check(file_name):

    # check whether file exist or the type is correct'
    
    if file_name is None: return None
        
    if os.path.exists(file_name):
        abs_file_name = file_name
    elif os.path.exists(sys.path[0] + '/' + file_name):
        abs_file_name = sys.path[0] + '/' + file_name
    elif os.path.exists(os.getcwd() + '/' + file_name):
        abs_file_name = os.getcwd() + '/' + file_name
    else:
        abs_file_name = None
        raise FileNotFoundError("File not found: " + file_name)

    return abs_file_name


def WrapToPi(rad):
    # transform the rad to the range [-pi, pi]
    while rad > pi:
        rad = rad - 2 * pi
    
    while rad < -pi:
        rad = rad + 2 * pi
    
    return rad

def WrapToRegion(rad, range):
    # transform the rad to defined range, 
    # the length of range should be 2 * pi
    assert(len(range) >= 2 and range[1] - range[0] == 2*pi)

    while rad > range[1]:
        rad = rad - 2 * pi
    
    while rad < range[0]:
        rad = rad + 2 * pi
    
    return rad

def extend_list(input_list, number):

    if not isinstance(input_list, list):
        return [input_list] * number

    if number == 0:
        return []

    if len(input_list) == 0:
        return None

    if len(input_list) <= number: 
        input_list.extend([input_list[-1]] * (number - len(input_list)) )

    if len(input_list) > number:
        input_list = input_list[:number]

    return input_list


def convert_list_length(input_data, number=0):

    '''
    convert the input to a list with a specific length of number
    '''

    if number == 0:
        return []

    if not isinstance(input_data, list) or is_list_of_numbers(input_data):
        return [input_data] * number
    
    if len(input_data) <= number: 
        input_data.extend([input_data[-1]] * (number - len(input_data)) )

    if len(input_data) > number:
        input_data = input_data[:number]

    return input_data

def convert_list_length_dict(input_data, number=0):

    '''
    convert the input to a list with a specific length of number
    '''

    if number == 0:
        return []

    if not isinstance(input_data, list) or is_list_of_dicts(input_data):
        return [input_data] * number
    
    if len(input_data) <= number: 
        input_data.extend([input_data[-1]] * (number - len(input_data)) )

    if len(input_data) > number:
        input_data = input_data[:number]

    return input_data

    
def is_list_of_dicts(lst):
    return isinstance(lst, list) and all(isinstance(sub, dict) for sub in lst)


def is_list_of_numbers(lst):
    return isinstance(lst, list) and all(isinstance(sub, (int, float)) for sub in lst)


def is_list_of_lists(lst):
    return isinstance(lst, list) and any(isinstance(sub, list) for sub in lst)

def is_list_not_list_of_lists(lst):
    return isinstance(lst, list) and all(not isinstance(sub, list) for sub in lst)


def relative_position(position1, position2, topi=True):

    diff = position2[0:2]-position1[0:2]
    distance = np.linalg.norm(diff)
    radian = atan2(diff[1, 0], diff[0, 0])

    if topi: radian = WrapToPi(radian)

    return distance, radian

def get_transform(state):
    # from state to rotation and transition matrix
    # state: (3, 1) or (2 ,1)
    if state.shape == (2, 1):
        rot = np.array([ [1, 0], [0, 1] ])
        trans = state[0:2]

    else:
        rot = np.array([ [cos(state[2, 0]), -sin(state[2, 0])], [sin(state[2, 0]), cos(state[2, 0])] ])
        trans = state[0:2]

    return trans, rot 

def get_affine_transform(state):
    # 2d: 6 paramters: [a, b, d, e, xoff, yoff] reference: https://shapely.readthedocs.io/en/stable/manual.html
    return [cos(state[2, 0]), -sin(state[2, 0]), sin(state[2, 0]), cos(state[2, 0]), state[0, 0], state[1, 0]]

def geometry_transform(geometry, state):

    def transfor_with_state(x, y):

        trans, rot = get_transform(state)

        # point = np.array([[x], [y]])
        points = np.array([x, y])

        new_points = rot @ points + trans

        return (new_points[0, :], new_points[1, :])
    
    new_geometry = ops.transform(transfor_with_state, geometry)

    return new_geometry


def omni_to_diff(state_ori, vel_omni, w_max=1.5, guarantee_time = 0.2, tolerance = 0.1, mini_speed=0.02):

    if isinstance(vel_omni, list):
        vel_omni = np.array(vel_omni).reshape((2, 1))

    speed = np.sqrt(vel_omni[0, 0] ** 2 + vel_omni[1, 0] ** 2)
    
    if speed <= mini_speed:
        return np.zeros((2, 1))

    vel_radians = atan2(vel_omni[1, 0], vel_omni[0, 0])
    robot_radians = state_ori
    diff_radians = robot_radians - vel_radians
    # w_max = self.vel_max[1, 0]

    diff_radians = WrapToPi(diff_radians)

    if abs(diff_radians) < tolerance: w = 0
    else:
        w = -diff_radians / guarantee_time
        if w > w_max: w = w_max
        if w < -w_max: w = -w_max

    v = speed * cos(diff_radians)
    if v<0: v = 0

    return np.array([[v], [w]])


def diff_to_omni(state_ori, vel_diff):

    if len(vel_diff.shape)==0:
        return np.zeros((2, 1))

    vel_linear = vel_diff[0, 0]
    theta = state_ori
    vx = vel_linear * cos(theta)
    vy = vel_linear * sin(theta)

    return np.array([[vx], [vy]])


# def extend_list(lst, target_length):

#     if len(lst) == 0:
#         return None  # Can't extend an empty list
    
#     while len(lst) < target_length:
#         lst.append(lst[-1])
        
#     return lst