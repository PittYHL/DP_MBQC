import copy
import random
import numpy as np
from leaves import *
from placement import *
from last_step import double_shape
round = 3
keep = 30
longest = 30
final_keep = 6 #for after placing back and kept
def keep_placing(input_shapes, table, shapes, first, last, rows, switch, new_map, first_loc, ori_depth, shortest_depth, file_name, keep, original_wire, hwea):
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
    all_leaves, all_paths, leaves_width, leaves_space, leaves_depth = generate_leaves(available_length) #generate leaves of all the length
    #short_table, short_shapes = sort_shapes(last_table, last_shapes)
    short_table = copy.deepcopy(last_table)
    short_shapes = copy.deepcopy(last_shapes)
    print(len(short_shapes), " short shapes")
    final_shapes = [[] for _ in range(round + 1)]
    final_depth = [[] for _ in range(round + 1)]
    final_space = [[] for _ in range(round + 1)]
    final_single_depth = [[] for _ in range(round + 1)]
    temp_shapes = []
    temp_depth = []
    temp_space = []
    for shape in input_shapes:
        temp_shapes.append(shape)
        temp_depth.append(len(shape[0]))
        _, space = fill_shape(shape)
        temp_space.append(space)
    # temp_shapes, temp_depths, temp_spaces = sort_round_shape(input_shapes, temp_depth, temp_space)
    final_shapes[0] = temp_shapes
    for shape in temp_shapes:
        final_depth[0].append(len(shape[0]))
        _, space = fill_shape(shape)
        final_space[0].append(space)
        final_single_depth[0].append([len(shape[0])])
    #iterate through all rounds
    for r in range(round):
        temp_shapes = []
        temp_depths = []
        temp_spaces = []
        temp_single_depth = []
        print(r, ' Round')
        if switch and r % 2 == 0:
            flip = 1
        else:
            flip = 0
        if (first_loc == 'd' and r % 2 == 0) or (first_loc == 'u' and r % 2 == 1):
            loc = 'd'
        elif (first_loc == 'd' and r % 2 == 1) or (first_loc == 'u' and r % 2 == 0):
            loc = 'u'
        else:
            loc = 'm'
        for i in range(len(final_shapes[r])):
            print(i, ' previous shapes')
            previous_shape = final_shapes[r][i]
            previous_shape = fill_previous(previous_shape, rows, loc)
            previous_sinhle_depth = final_single_depth[r][i]
            for j in range(len(short_shapes)):
                print(j, ' short shapes')
                shape = short_shapes[j]
                if loc == 'd':
                    if flip:
                        upper = min(rows - len(shape), max(first[-1], last[-1]))
                    else:
                        upper = min(rows - len(shape), max(first[0], last[0]))
                    # print('upper ', upper)
                    for upper_row in range(upper + 1):
                        lower_row = rows - upper_row - len(shape)
                        starts = copy.deepcopy(short_table[j]['starts'])
                        ends = copy.deepcopy(short_table[j]['ends'])
                        if flip:
                            shapes, depths, spaces, single_depths = place_next(shape, starts, ends, all_paths, max_first, first,
                                last, all_leaves, previous_shape, flip, lower_row, upper_row, leaves_width, leaves_space, leaves_depth, keep, hwea)
                        else:
                            shapes, depths, spaces, single_depths = place_next(shape, starts, ends, all_paths, max_first, first,
                                last, all_leaves, previous_shape, flip, upper_row, lower_row, leaves_width, leaves_space, leaves_depth, keep, hwea)
                        temp_shapes = temp_shapes + shapes
                        temp_depths = temp_depths + depths
                        temp_spaces = temp_spaces + spaces
                        for k in range(len(single_depths)):
                            single_depth = copy.deepcopy(previous_sinhle_depth)
                            single_depth.append(single_depths[k])
                            temp_single_depth.append(single_depth)
                elif loc == 'u':
                    if flip:
                        lower = min(rows - len(shape), max(first[0], last[0]))
                    else:
                        lower = min(rows - len(shape), max(first[-1], last[-1]))
                    # print('lower ', lower)
                    for lower_row in range(lower + 1):
                        upper_row = rows - lower_row - len(shape)
                        starts = copy.deepcopy(short_table[j]['starts'])
                        ends = copy.deepcopy(short_table[j]['ends'])
                        if flip:
                            shapes, depths, spaces, single_depths = place_next(shape, starts, ends, all_paths, max_first, first,
                                last, all_leaves, previous_shape, flip, lower_row, upper_row, leaves_width, leaves_space, leaves_depth, keep, hwea)
                        else:
                            shapes, depths, spaces, single_depths = place_next(shape, starts, ends, all_paths, max_first, first,
                                last, all_leaves, previous_shape, flip, upper_row, lower_row, leaves_width, leaves_space, leaves_depth, keep, hwea)
                        temp_shapes = temp_shapes + shapes
                        temp_depths = temp_depths + depths
                        temp_spaces = temp_spaces + spaces
                        for k in range(len(single_depths)):
                            single_depth = copy.deepcopy(previous_sinhle_depth)
                            single_depth.append(single_depths[k])
                            temp_single_depth.append(single_depth)
                elif loc == 'm':
                    extra_row = rows - len(shape)
                    upper_row = 0  # number of extra rows that upper the shape
                    lower_row = 0
                    while extra_row != 0:
                        if extra_row % 2 == 0:
                            upper_row = upper_row + 1
                        else:
                            lower_row = lower_row + 1
                        extra_row = extra_row - 1
                    starts = copy.deepcopy(short_table[j]['starts'])
                    ends = copy.deepcopy(short_table[j]['ends'])
                    shapes, depths, spaces, single_depths = place_next(shape, starts, ends, all_paths, max_first, first, last,
                            all_leaves, previous_shape, flip, upper_row, lower_row, leaves_width, leaves_space, leaves_depth, keep, hwea)
                    temp_shapes = temp_shapes + shapes
                    temp_depths = temp_depths + depths
                    temp_spaces = temp_spaces + spaces
                    for k in range(len(single_depths)):
                        single_depth = copy.deepcopy(previous_sinhle_depth)
                        single_depth.append(single_depths[k])
                        temp_single_depth.append(single_depth)
        final_k = min(keep, final_keep)
        temp_shapes, temp_depths, temp_spaces, temp_single_depth = sort_round_shape(temp_shapes, temp_depths, temp_spaces, temp_single_depth, final_k)
        final_shapes[r + 1] = temp_shapes
        final_depth[r + 1] = temp_depths
        final_space[r + 1] = temp_spaces
        final_single_depth[r + 1] = temp_single_depth
        final_shapes[r] = []
    final_wires = count_wire(final_shapes[-1])
    average_wire = final_wires[0]/(round + 1)
    optimized_reduction = (sum(final_single_depth[-1][0]) - final_depth[-1][0]) / round
    average = sum(final_single_depth[-1][0]) / (round + 1)
    print("Original depth " + str(ori_depth))
    print("best depth " + str(shortest_depth))
    print("Optimized", round + 1, " iterations depth: ", final_depth[-1][0])
    print("Individual widths are", final_single_depth[-1][0])
    print("Optimized reduction", optimized_reduction)
    print("Average shape", average)
    print("Original 1000 " + str(ori_depth*1000 + 999))
    print("Optimized 1000 " + str(average * 1000 - optimized_reduction*999))
    print("Original wire " + str(original_wire))
    print("Final wire " + str(average_wire))
    f = open(file_name, "w")
    f.write("Original depth " + str(ori_depth))
    f.write('\n')
    f.write("best depth " + str(shortest_depth))
    f.write('\n')
    f.write("Optimized " + str(round + 1) + " iterations depth: " + str(final_depth[-1][0]))
    f.write('\n')
    f.write("Individual widths are " + str(final_single_depth[-1][0]))
    f.write('\n')
    f.write("Optimized reduction " + str(optimized_reduction))
    f.write('\n')
    f.write("Average shape " + str(average))
    f.write('\n')
    f.write("Original 1000 " + str(ori_depth * 1000 + 999))
    f.write('\n')
    f.write("Optimized 1000 " + str(average * 1000 - optimized_reduction*999))
    f.write('\n')
    f.write("Original wire " + str(original_wire))
    f.write('\n')
    f.write("Final wire " + str(average_wire))
    f.close()


def place_next(shape, starts, ends, all_paths, max_first, first, last, all_leaves, previous_shape, flip, up_rows, down_rows, leaves_width, leaves_space, leaves_depth, keep, hwea):
    front_shapes = [[] for _ in range(len(starts) + 1)] #the first one is the original
    front_leaves = [[] for _ in range(len(starts) + 1)]
    front_locs = [[] for _ in range(len(starts) + 1)]
    back_shapes = [[] for _ in range(len(starts) + 1)]
    back_leaves = [[] for _ in range(len(starts) + 1)]
    back_locs = [[] for _ in range(len(starts) + 1)]
    start_rank, _, _ = rank_starts(starts, shape)
    if hwea:
        start_rank.remove(0)
        start_rank.append(0)
    end_rank, _, _ = rank_ends(ends, shape)
    to_keep = min(keep, longest)
    for i in range(len(starts)):
        starts[i][1] = starts[i][1] + max_first #change the x locs
        ends[i][1] = ends[i][1] + max_first
        starts[i][0] = starts[i][0] + up_rows  # change the y locs
        ends[i][0] = ends[i][0] + up_rows
    # starts.sort(reverse=True, key=lambda x: x[1])
    # ends.sort(key=lambda x: x[1])
    original_shape = copy.deepcopy(shape)
    for i in range(len(original_shape)):
        original_shape[i] = [0] * max_first + original_shape[i] + [0] * max(last)
    for i in range(up_rows):
        original_shape.insert(0, [0] * len(original_shape[0]))
    for i in range(down_rows):
        original_shape.append([0] * len(original_shape[0]))
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
                paths = rank_paths(leaves_width[first[start_index] - 1], leaves_space[first[start_index] - 1],
                                   leaves_depth[first[start_index] - 1],
                                   all_paths[first[start_index] - 1], keep)
                new_shapes, new_leaves = place_leaf_front(front_shapes[i][j], front_leaves[i][j], available_locs[k], paths, all_paths[first[start_index] - 1])
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
            return [], [], [], []
        front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1], depth_list = fit_front(front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1],
                                                                                                depth_list, previous_shape, flip, to_keep)
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
        if len(depth_list) > to_keep:
            back_shapes[i + 1], back_leaves[i + 1], back_locs[i + 1], depth_list = remove_short_end(back_shapes[i + 1],
                                                                                                    back_leaves[i + 1],
                                                                                                    back_locs[i + 1],
                                                                                                    depth_list, to_keep)
        if len(back_shapes[i + 1]) == 0:
            print('back fail')
            return [], [], [], []
    final_keeps = min(keep, final_keep)
    if len(depth_list) > final_keeps:
        back_shapes[i + 1], back_leaves[i + 1], back_locs[i + 1], depth_list, space_list = \
            remove_short_end_space(back_shapes[i + 1], back_leaves[i + 1], back_locs[i + 1], depth_list, final_keeps)
    new_front_leaves, new_front_locs, new_back_leaves, new_back_locs = shuffle_locs(start_rank, front_leaves[-1],
                                                                                    front_locs[-1], end_rank,
                                                                                    back_leaves[-1], back_locs[
                                                                                        -1])  # used to shuffle back the correct position
    shortest_depth, shortest_shapes = count_shortest2(original_shape, all_paths, front_shapes[-1], new_front_leaves,
                                                     new_front_locs, starts, first,
                                                     back_shapes[-1], new_back_leaves, new_back_locs, ends, last)
    final_shapes = []
    final_depth = []
    final_space = []
    single_depths = []
    for shape in shortest_shapes:
        single_depths.append(len(shape[0]))
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
    return final_shapes, final_depth, final_space, single_depths

def fit_front(shapes, leaves, locs, depth_list, previous_shape, flip, longest = longest): #choose the best front that fit the previous shape
    new_shapes = []
    if flip:
        temp_shapes = flip_shape(shapes)
    else:
        temp_shapes = shapes
    for shape in temp_shapes:
        temp_shape = copy.deepcopy(shape)
        new_shapes.append(remove_empty2(temp_shape))
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
                                                                temp_shape[i + 1][back_locs[i]] == 0)):
                    found_reduc = 0
                    break
                elif i == len(new_shape) - 1 and (new_shape[i][back_locs[i] + 1] != 0 or
                                                  (new_shape[i - 1][back_locs[i]] != 0 and
                                                   temp_shape[i - 1][back_locs[i]] == 0)):
                    found_reduc = 0
                    break
                elif i > 0 and i < len(new_shape) - 1 \
                        and (new_shape[i][back_locs[i] + 1] != 0 or
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

def sort_round_shape(shapes, new_depth, spaces, temp_single_depth, longest = final_keep):
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
            temp_single_depth.pop(i)
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
                    temp_single_depth.pop(j)
                    break
    return shapes, new_depth, spaces, temp_single_depth

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
        temp_shape = copy.deepcopy(shape)
        # upper = check_upper(temp_shape)
        # lower = check_lower(temp_shape)
        # remove_up_down(temp_shape, upper, lower)
        new_shape = []
        for row in reversed(temp_shape):
            new_shape.append(row)
        # for i in range(upper):
        #     new_shape.insert(0, [0]*len(new_shape[0]))
        # for i in range(lower):
        #     new_shape.append([0]*len(new_shape[0]))
        new_shapes.append(new_shape)
    return new_shapes

def check_upper(shape):
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j] != 0:
                return i

def check_lower(shape):
    for i in reversed(range(len(shape))):
        for j in range(len(shape[i])):
            if shape[i][j] != 0:
                return len(shape) - 1 - i
def remove_up_down(temp_shape, upper, lower):
    for i in range(upper):
        temp_shape.pop(0)
    for j in range(lower):
        temp_shape.pop(-1)
def fill_previous(previous_shape, rows, first_loc):
    if len(previous_shape) == rows:
        return previous_shape
    elif first_loc == 'd':
        extra_row = rows - len(previous_shape)
        for i in range(extra_row):
            previous_shape.insert(0, [0]*len(previous_shape[0]))
    elif first_loc == 'u':
        extra_row = rows - len(previous_shape)
        for i in range(extra_row):
            previous_shape.append([0]*len(previous_shape[0]))
    else:
        extra_row = rows - len(previous_shape)
        up_rows = 0
        down_rows = 0
        while extra_row != 0:
            if extra_row % 2 == 0:
                up_rows = up_rows + 1
            else:
                down_rows = down_rows + 1
            extra_row = extra_row - 1
        for i in range(up_rows):
            previous_shape.insert(0, [0] * len(previous_shape[0]))
        for i in range(down_rows):
            previous_shape.append([0]*len(previous_shape[0]))
    return previous_shape

def remove_empty2(shape): #only remove empty columns
    max_zeros = 100000
    original_len = len(shape[0])
    for row in shape:
        for j in range(len(shape[0])):
            if row[original_len - j - 1] != 0:
                if j < max_zeros:
                    max_zeros = j
                break
    for i in range(len(shape)):
        for j in range(max_zeros):
            shape[i].pop(-1)
    max_zeros = 100000
    original_len = len(shape[0])
    for row in shape:
        for j in range(len(shape[0])):
            if row[j] != 0:
                if j < max_zeros:
                    max_zeros = j
                break
    if max_zeros > 0:
        for i in range(len(shape)):
            for j in range(max_zeros):
                shape[i].pop(0)
    return shape

def count_shortest2(original_shape, all_paths, front_shapes, front_leaves, front_locs,
                   starts, first, back_shapes, back_leaves, back_locs, ends, last):
    shortest_front = 100000
    shortest_end = 100000
    shortest_depth = 1000000
    final_shapes = []
    front_indexes = []
    back_indexes = []
    for i in range(len(front_shapes)):
        if shortest_front > count_depth(front_shapes[i]):
            shortest_front = count_depth(front_shapes[i])
    for i in range(len(back_shapes)):
        if shortest_end > count_depth(back_shapes[i]):
            shortest_end = count_depth(back_shapes[i])
    for i in range(len(front_shapes)):
        if count_depth(front_shapes[i]) == shortest_front:
            front_indexes.append(i)
    for i in range(len(back_shapes)):
        if count_depth(back_shapes[i]) == shortest_end:
            back_indexes.append(i)
    for i in range(len(front_indexes)):
        for j in range(len(back_indexes)):
            temp_shape, temp_depth = fill_final2(original_shape, all_paths, front_leaves[front_indexes[i]], front_locs[front_indexes[i]], starts, first,
                                          back_leaves[back_indexes[j]], back_locs[back_indexes[j]], ends, last)
            if temp_depth < shortest_depth:
                shortest_depth = temp_depth
            final_shapes.append(temp_shape)
    return shortest_depth, final_shapes

def fill_final2(original_shape, all_paths, front_leave, front_loc,
               starts, first, back_leave, back_loc, ends, last):
    new_shape = copy.deepcopy(original_shape)
    new_front = copy.deepcopy(front_leave)
    new_back = copy.deepcopy(back_leave)
    for i in range(len(new_front)):
        front_paths = copy.deepcopy(all_paths[first[i] - 1][new_front[i]])
        if front_loc[i] == 'l':
            new_loc = [starts[i][0], starts[i][1] - 1]
        elif front_loc[i] == 'u':
            new_loc = [starts[i][0] - 1, starts[i][1]]
        elif front_loc[i] == 'd':
            new_loc = [starts[i][0] + 1, starts[i][1]]
        offset_y = front_paths[-1][0] - new_loc[0]
        offset_x = front_paths[-1][1] - new_loc[1]
        for j in range(len(front_paths)):
            front_paths[j][0] = front_paths[j][0] - offset_y
            front_paths[j][1] = front_paths[j][1] - offset_x
        for j in range(len(front_paths)):
            new_shape[front_paths[j][0]][front_paths[j][1]] = 1
    for i in range(len(new_back)):
        back_paths = copy.deepcopy(all_paths[last[i] - 1][new_back[i]])
        if back_loc[i] == 'r':
            new_loc = [ends[i][0], ends[i][1] + 1]
        elif back_loc[i] == 'u':
            new_loc = [ends[i][0] - 1, ends[i][1]]
        elif back_loc[i] == 'd':
            new_loc = [ends[i][0] + 1, ends[i][1]]
        offset_y = back_paths[0][0] - new_loc[0]
        offset_x = back_paths[0][1] - new_loc[1]
        for j in range(len(back_paths)):
            back_paths[j][0] = back_paths[j][0] - offset_y
            back_paths[j][1] = back_paths[j][1] - offset_x
        for j in range(len(back_paths)):
            new_shape[back_paths[j][0]][back_paths[j][1]] = 1
    new_shape = remove_empty2(new_shape)
    return new_shape, count_depth(new_shape)

def count_wire(final_shapes):
    wires = []
    for shape in final_shapes:
        count = 0
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] == 2:
                    count = count + 1
        wires.append(count)
    return wires