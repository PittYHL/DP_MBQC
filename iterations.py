import copy
import random
import numpy as np
from leaves import *
from placement import *
from last_step import double_shape
round = 10
keep = 100
final_keep = 10

def keep_placing(table, shapes, first, last, rows, switch):
    #sort the shortest shape
    for i in range(len(first)):
        if first[i] < 0:
            first[i] = abs(first[i])
    last_table = table
    last_shapes = shapes
    final_shapes = []
    max_first = max(first)
    all_length = first + last
    available_length = list(set(all_length))
    available_length.sort()
    all_leaves, all_paths = generate_leaves(available_length) #generate leaves of all the length
    short_table, short_shapes = sort_shape(last_table, last_shapes)
    final_shapes = [[] for _ in range(round + 1)]
    final_depth = [[] for _ in range(round + 1)]
    final_space = [[] for _ in range(round + 1)]
    final_shapes[0].append([])
    final_depth[0].append([])
    final_space[0].append([])
    #place the first round
    print('First Round')
    for r in range(round):
        temp_shapes = []
        temp_tables = []
        temp_spaces = []
        print(r, ' Round')
        if switch and r % 2 == 1:
            flip = 1
        else:
            flip = 0
        for i in range(len(final_shapes[r])):
            previous_shape = final_shapes[r][i]
            for j in range(len(short_shapes)):
                starts = copy.deepcopy(short_table[i]['starts'])
                ends = copy.deepcopy(short_table[i]['ends'])
                shape = short_shapes[j]
                shapes, depths, spaces = place_next(shape, starts, ends, all_paths, max_first, first, last, all_leaves, previous_shape, flip)
                temp_shapes.append(shapes[0])
                temp_tables.append(depths[0])
                temp_spaces.append(spaces[0])


def place_next(shape, starts, ends, all_paths, max_first, first, last, all_leaves, previous_shape, flip):
    front_shapes = [[] for _ in range(len(starts) + 1)] #the first one is the original
    front_leaves = [[] for _ in range(len(starts) + 1)]
    front_locs = [[] for _ in range(len(starts) + 1)]
    start_rank, _, _ = rank_starts(starts, shape)
    end_rank, _, _ = rank_ends(ends, shape)
    for i in range(len(starts)):
        starts[i][1] = starts[i][1] + max_first #change the x locs
        ends[i][1] = ends[i][1] + max_first
    # starts.sort(reverse=True, key=lambda x: x[1])
    # ends.sort(key=lambda x: x[1])
    original_shape = copy.deepcopy(shape)
    for i in range(len(original_shape)):
        original_shape[i] = [0] * max_first + original_shape[i] + [0] * max(last)
    front_shapes[0].append(copy.deepcopy(original_shape))
    front_leaves[0].append([])
    front_locs[0].append([])
    #test one time after placing one leaf
    for i in range(len(starts)):
        shortest = 100000
        depth_list = []
        start_index = start_rank[i]
        for j in range(len(front_shapes[i])):
            available_locs, available_dirs = check_start(front_shapes[i][j], starts[start_index])
            for k in range(len(available_locs)):
                new_shapes, new_leaves = place_leaf_front(front_shapes[i][j], front_leaves[i][j], available_locs[k], all_paths[first[start_index] - 1])
                front_leaves[i + 1] = front_leaves[i + 1] + new_leaves
                for l in range(len(new_shapes)):
                    new_locs = copy.deepcopy(front_locs[i][j])
                    new_locs.append(available_dirs[k])
                    front_locs[i + 1].append(new_locs)
                for new_shape in new_shapes:
                    front_shapes[i + 1].append(new_shape)
                    depth = count_depth(new_shape)
                    depth_list.append(depth)
                    if depth < shortest:
                        shortest = depth
        if len(depth_list) > longest:
            front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1], depth_list = fit_front(front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1],
                                                                                                depth_list, previous_shape, flip)
        if len(front_shapes[i + 1]) == 0:
            print('front fail')
    if len(depth_list) > 1:
        front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1], depth_list = fit_front(
            front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1], depth_list, previous_shape, flip, 1)


    print('g')
    #return final_shapes, final_depth, final_space

def fit_front(shapes, leaves, locs, depth_list, previous_shape, flip, longest = longest): #choose the best front that fit the previous shape
    if previous_shape == []:
        shapes, leaves, locs, depth_list = remove_short_front(shapes, leaves, locs, depth_list)
        return shapes, leaves, locs, depth_list
    if flip:
        new_shapes = double_shape(shapes)
    else:
        new_shapes = shapes
    new_depth = []
    for i in range(len(new_shapes)):
        new_depth.append(check_combine_depth(previous_shape,new_shapes[i]))
    shortest = min(new_depth)
    while (len(shapes) > longest and len(list(set(new_depth))) != 1):
        max_depth = max(new_depth)
        max_list = []
        for i in range(len(new_depth)):
            if new_depth[i] == max_depth:
                max_list.append(i)
        for i in reversed(max_list):
            shapes.pop(i)
            leaves.pop(i)
            locs.pop(i)
            new_depth.pop(i)
            depth_list.pop(i)
    if len(list(set(new_depth))) == 1 and len(shapes) > longest:
        indexes = []
        for i in range(len(new_depth)):
            indexes.append(i)
        chosen = random.sample(indexes, len(new_depth) - longest)
        chosen.sort()
        for i in reversed(chosen):
            shapes.pop(i)
            leaves.pop(i)
            locs.pop(i)
            depth_list.pop(i)
            new_depth.pop(i)
    return shapes, leaves, locs, depth_list



def check_combine_depth(ori_shape, next_shape):
    new_shape = []
    for i in range(len(ori_shape)):
        new_shape.append(ori_shape[i] + [0] + next_shape[i])
    back_locs = []
    for row in ori_shape:
        for j in reversed(range(len(row))):
            if row[j] != 0:
                back_locs.append(j + 1)
                break
            elif j == 0:
                back_locs.append(0)
    found_reduc = 1
    for i in range(len(new_shape)):
        if new_shape[i][back_locs[i]] != 0:
            found_reduc = 0
            return len(new_shape[0])
    if found_reduc:
        reduc = 0
        temp_shape = copy.deepcopy(ori_shape)
        for i in range(len(temp_shape)):
            temp_shape[i].append(0)
        while found_reduc:
            for i in range(len(new_shape)):
                if i == 0 and (
                        new_shape[i][back_locs[i] + 1] != 0 or (new_shape[i + 1][back_locs[i]] != 0 and
                                                                ori_shape[i + 1][back_locs[i]] == 0)):
                    found_reduc = 0
                    break
                elif i == len(new_shape) - 1 and (new_shape[i][back_locs[i] + 1] != 0 or
                                                  (new_shape[i - 1][back_locs[i]] != 0 and
                                                   temp_shape[i - 1][back_locs[i]] == 0)):
                    found_reduc = 0
                    break
                elif i > 0 and i < len(new_shape) - 1 and (new_shape[i][back_locs[i] + 1] != 0 or
                                                           (new_shape[i - 1][back_locs[i]] != 0 and
                                                            temp_shape[i - 1][back_locs[i]] == 0) or
                                                           (new_shape[i + 1][back_locs[i]] != 0 and
                                                            temp_shape[i + 1][back_locs[i]] == 0)):
                    found_reduc = 0
                    break
            if found_reduc:
                for i in range(len(new_shape)):
                    new_shape[i].pop(back_locs[i])
                reduc = reduc + 1
    return len(new_shape[0])
