import copy
import random
import numpy as np
from leaves import *
from placement import *
from last_step import double_shape
round = 2
keep = 50
longest = 50
final_keep = 6 #for after placing back and kept

def keep_placing(input_shapes, table, shapes, first, last, rows, switch, new_map):
    #show original depth
    ori_depth = len(new_map[0])
    double_shape, double_depth = check_combine_depth(new_map, new_map)
    reduction = ori_depth * 2 - double_depth
    ori_total_depth = ori_depth * (round + 1) - round * reduction
    print("original", round + 1, " iterations depth: ", ori_total_depth)
    print("original reduction ", reduction)
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
    short_table, short_shapes = sort_shapes(last_table, last_shapes)
    print(len(short_shapes), " short shapes")
    final_shapes = [[] for _ in range(round + 1)]
    final_depth = [[] for _ in range(round + 1)]
    final_space = [[] for _ in range(round + 1)]
    temp_shape = []
    temp_depth = []
    temp_space = []
    for shape in input_shapes:
        temp_shape.append(shape)
        temp_depth.append(len(shape[0]))
        _, space = fill_shape(shape)
        temp_space.append(space)
    temp_shapes, temp_depths, temp_spaces = sort_round_shape(input_shapes, temp_depth, temp_space)
    final_shapes[0] = temp_shapes
    for shape in temp_shapes:
        final_depth[0].append(len(shape[0]))
        _, space = fill_shape(shape)
        final_space[0].append(space)
    #iterate through all rounds
    for r in range(round):
        temp_shapes = []
        temp_depths = []
        temp_spaces = []
        print(r, ' Round')
        if switch and r % 2 == 0:
            flip = 1
        else:
            flip = 0
        for i in range(len(final_shapes[r])):
            print(i, ' previous shapes')
            previous_shape = final_shapes[r][i]
            for j in range(len(short_shapes)):
                print(j, ' short shapes')
                starts = copy.deepcopy(short_table[j]['starts'])
                ends = copy.deepcopy(short_table[j]['ends'])
                shape = short_shapes[j]
                shapes, depths, spaces = place_next(shape, starts, ends, all_paths, max_first, first, last, all_leaves, previous_shape, flip)
                temp_shapes = temp_shapes + shapes
                temp_depths = temp_depths + depths
                temp_spaces = temp_spaces + spaces
        temp_shapes, temp_depths, temp_spaces = sort_round_shape(temp_shapes, temp_depths, temp_spaces)
        final_shapes[r + 1] = temp_shapes
        final_depth[r + 1] = temp_depths
        final_space[r + 1] = temp_spaces
    print("Optimized", round + 1, " iterations depth: ", final_depth[-1][0])
    optimized_reduction = ((round + 1) * len(input_shapes[0][0]) - final_depth[-1][0]) / round
    print("Optimized reduction", optimized_reduction)


def place_next(shape, starts, ends, all_paths, max_first, first, last, all_leaves, previous_shape, flip):
    front_shapes = [[] for _ in range(len(starts) + 1)] #the first one is the original
    front_leaves = [[] for _ in range(len(starts) + 1)]
    front_locs = [[] for _ in range(len(starts) + 1)]
    back_shapes = [[] for _ in range(len(starts) + 1)]
    back_leaves = [[] for _ in range(len(starts) + 1)]
    back_locs = [[] for _ in range(len(starts) + 1)]
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
    #only choose one of the shortest
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
        if len(front_shapes[i + 1]) == 0:
            print('front fail')
        front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1], depth_list = fit_front(front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1],
                                                                                                depth_list, previous_shape, flip)
    if len(depth_list) > 1:
        front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1], depth_list = fit_front(
            front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1], depth_list, previous_shape, flip, 1)
    #place the back
    back_shapes[0].append(copy.deepcopy(original_shape))
    back_leaves[0].append([])
    back_locs[0].append([])
    for i in range(len(ends)):
        shortest = 100000
        depth_list = []
        end_index = end_rank[i]
        for j in range(len(back_shapes[i])):
            available_locs, available_dirs = check_end(back_shapes[i][j], ends[end_index])
            for k in range(len(available_locs)):
                new_shapes, new_leaves = place_leaf_end(back_shapes[i][j], back_leaves[i][j], available_locs[k],
                                                        all_paths[last[end_index] - 1])
                back_leaves[i + 1] = back_leaves[i + 1] + new_leaves
                for l in range(len(new_shapes)):
                    new_locs = copy.deepcopy(back_locs[i][j])
                    new_locs.append(available_dirs[k])
                    back_locs[i + 1].append(new_locs)
                for new_shape in new_shapes:
                    back_shapes[i + 1].append(new_shape)
                    depth = count_depth(new_shape)
                    depth_list.append(depth)
                    if depth < shortest:
                        shortest = depth
        if len(depth_list) > longest:
            back_shapes[i + 1], back_leaves[i + 1], back_locs[i + 1], depth_list = remove_short_end(back_shapes[i + 1],
                                                                                                    back_leaves[i + 1],
                                                                                                    back_locs[i + 1],
                                                                                                    depth_list, longest)
        if len(back_shapes[i + 1]) == 0:
            print('back fail')
    if len(depth_list) > final_keep:
        back_shapes[i + 1], back_leaves[i + 1], back_locs[i + 1], depth_list, space_list = \
            remove_short_end_space(back_shapes[i + 1], back_leaves[i + 1], back_locs[i + 1], depth_list, final_keep)
    new_front_leaves, new_front_locs, new_back_leaves, new_back_locs = shuffle_locs(start_rank, front_leaves[-1],
                                                                                    front_locs[-1], end_rank,
                                                                                    back_leaves[-1], back_locs[
                                                                                        -1])  # used to shuffle back the correct position
    shortest_depth, shortest_shapes = count_shortest(original_shape, all_paths, front_shapes[-1], new_front_leaves,
                                                     new_front_locs, starts, first,
                                                     back_shapes[-1], new_back_leaves, new_back_locs, ends, last)
    final_shapes = []
    final_depth = []
    final_space = []
    if flip:
        new_shapes = flip_shape(shortest_shapes)
    else:
        new_shapes = shortest_shapes
    for shape in new_shapes:
        temp_shape, temp_depth = check_combine_depth(previous_shape, shape)
        _, temp_space = fill_shape(temp_shape)
        final_shapes.append(temp_shape)
        final_depth.append(temp_depth)
        final_space.append(temp_space)
    return final_shapes, final_depth, final_space

def fit_front(shapes, leaves, locs, depth_list, previous_shape, flip, longest = longest): #choose the best front that fit the previous shape
    new_shapes = []
    if flip:
        temp_shapes = flip_shape(shapes)
    else:
        temp_shapes = shapes
    for shape in temp_shapes:
        temp_shape = copy.deepcopy(shape)
        new_shapes.append(remove_empty(temp_shape))
    new_depth = []
    for i in range(len(new_shapes)):
        _, temp_depth = check_combine_depth(previous_shape,new_shapes[i])
        new_depth.append(temp_depth)
    shortest = min(new_depth)
    while (len(shapes) > longest and len(list(set(new_depth))) != 1):
        max_depth = max(new_depth)
        max_list = []
        for i in range(len(new_depth)):
            if new_depth[i] == max_depth:
                max_list.append(i)
        if len(shapes) - longest >= len(max_list):
            chosen = max_list
        else:
            chosen = random.sample(max_list, len(new_depth) - longest)
        chosen.sort()
        for i in reversed(chosen):
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
    if len(ori_shape) != len(next_shape):
        print('g')
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
        if new_shape[i][back_locs[i] + 1] != 0:
            found_reduc = 0
            return new_shape, len(new_shape[0])
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
    return new_shape, len(new_shape[0])

def sort_round_shape(shapes, new_depth, spaces, longest = final_keep):
    while (len(shapes) > longest and len(list(set(new_depth))) != 1):
        max_depth = max(new_depth)
        max_list = []
        for i in range(len(new_depth)):
            if new_depth[i] == max_depth:
                max_list.append(i)
        for i in reversed(max_list):
            shapes.pop(i)
            spaces.pop(i)
            new_depth.pop(i)
    if len(list(set(new_depth))) == 1 and len(shapes) > longest:
        indexes = []
        for i in range(len(new_depth)):
            indexes.append(i)
        temp_spaces = copy.deepcopy(spaces)
        temp_spaces.sort()
        for i in range(len(temp_spaces) - longest):
            for j in range(len(shapes)):
                if spaces[j] == temp_spaces[i]:
                    shapes.pop(j)
                    spaces.pop(j)
                    new_depth.pop(j)
                    break
    return shapes, new_depth, spaces

def remove_short_end_space(shapes, back_leaves, back_locs, new_depth, final_keep):
    spaces = []
    for shape in shapes:
        _, space = fill_shape(shape)
        spaces.append(space)
    while (len(shapes) > final_keep and len(list(set(new_depth))) != 1):
        max_depth = max(new_depth)
        max_list = []
        for i in range(len(new_depth)):
            if new_depth[i] == max_depth:
                max_list.append(i)
        for i in reversed(max_list):
            shapes.pop(i)
            spaces.pop(i)
            back_leaves.pop(i)
            back_locs.pop(i)
            new_depth.pop(i)
    if len(list(set(new_depth))) == 1 and len(shapes) > final_keep:
        indexes = []
        for i in range(len(new_depth)):
            indexes.append(i)
        temp_spaces = copy.deepcopy(spaces)
        temp_spaces.sort()
        for i in range(len(shapes) - final_keep):
            for j in range(len(shapes)):
                if spaces[j] == temp_spaces[i]:
                    shapes.pop(j)
                    spaces.pop(j)
                    back_leaves.pop(j)
                    back_locs.pop(j)
                    new_depth.pop(j)
                    break
    return shapes, back_leaves, back_locs, new_depth, spaces

def flip_shape(shortest_shape):
    new_shapes = []
    for shape in shortest_shape:
        new_shape = []
        for row in reversed(shape):
            new_shape.append(row)
        new_shapes.append(new_shape)
    return new_shapes
