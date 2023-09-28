import copy
import random

longest = 200
final_keep = 15
def place_leaves(table, shapes, first, last, rows):
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
    front_leaves = [[] for _ in range(len(short_table))]
    front_locs = [[] for _ in range(len(short_table))]
    back_leaves = [[] for _ in range(len(short_table))]
    back_locs = [[] for _ in range(len(short_table))]
    start_locs = [[] for _ in range(len(short_table))]
    end_locs = [[] for _ in range(len(short_table))]
    depths = [0] * len(short_table)
    for i in range(len(short_table)):
        starts = copy.deepcopy(short_table[i]['starts'])
        ends = copy.deepcopy(short_table[i]['ends'])
        shape = short_shapes[i]
        depths[i], front_locs[i], front_leaves[i], start_locs[i], back_locs[i], back_leaves[i], end_locs[i], final_shapes = \
            place_final_shape(shape, starts, ends, all_paths, max_first, first, last, all_leaves, final_shapes)
    return final_shapes

def generate_leaves(available_length):
    max_length = max(available_length)
    leaves = [[] for _ in range(max_length)]
    paths = [[] for _ in range(max_length)]
    leaves[0] = [[1]]
    paths[0] = [[0,0]]
    queue = [[[1]]]
    queue_loc = [[0,0]] #location for the newest node
    queue_length = [1]
    queue_paths= [[[0,0]]]
    while queue != []:
        next = queue.pop(0)
        loc = queue_loc.pop(0)
        length = queue_length.pop(0)
        path = queue_paths.pop(0)
        new_leaves, locs, new_paths = generate_next(next, loc, path)
        for j in range(len(new_leaves)):
            if length + 1 < max_length:
                queue.append(new_leaves[j])
                queue_loc.append(locs[j])
                queue_paths.append(new_paths[j])
                queue_length.append(length + 1)
            if new_leaves[j] not in leaves[length] or new_paths[j] not in paths[length]:
                leaves[length].append(new_leaves[j])
                paths[length].append(new_paths[j])
    leaves[0] = [[[1]]]
    paths[0] = [[[0, 0]]]
    return leaves, paths

def generate_next(next, loc, path):
    new_leaves = []
    new_loc = []
    new_path = []
    if len(next) == 1:
        new_leaf1 = copy.deepcopy(next)
        new_leaf2 = copy.deepcopy(next)
        new_leaf3 = copy.deepcopy(next)
        new_path1 = copy.deepcopy(path)
        new_path2 = copy.deepcopy(path)
        new_path3 = copy.deepcopy(path)
        new_leaf1.insert(0, [0]*len(next[0])) #on top
        new_path1 = update_path(new_path1)
        new_path1.append([loc[0], loc[1]])
        new_leaf1[loc[0]][loc[1]] = 1
        new_loc.append([loc[0], loc[1]])
        new_leaf2[0].append(1) #right
        new_path2.append([loc[0], loc[1] + 1])
        new_loc.append([loc[0], loc[1] + 1])
        new_leaf3.append([0]*len(next[0])) #on down
        new_leaf3[loc[0] + 1][loc[1]] = 1
        new_path3.append([loc[0] + 1, loc[1]])
        new_loc.append([loc[0] + 1, loc[1]])
        new_leaf1 = fill_leave(new_leaf1)
        new_leaf2 = fill_leave(new_leaf2)
        new_leaf3 = fill_leave(new_leaf3)
        new_leaves.append(new_leaf1)
        new_leaves.append(new_leaf2)
        new_leaves.append(new_leaf3)
        new_path.append(new_path1)
        new_path.append(new_path2)
        new_path.append(new_path3)
    elif loc[0] == 0:
        new_path1 = copy.deepcopy(path)
        new_path2 = copy.deepcopy(path)
        new_path3 = copy.deepcopy(path)
        new_leaf1 = copy.deepcopy(next)
        new_leaf2 = copy.deepcopy(next)
        new_leaf1.insert(0, [0] * len(next[0]))  # on top
        new_leaf1[loc[0]][loc[1]] = 1
        new_path1 = update_path(new_path1)
        new_path1.append([loc[0], loc[1]])
        new_path.append(new_path1)
        new_loc.append([loc[0], loc[1]])
        if len(new_leaf2[0]) == loc[1] + 1:
            new_leaf2[loc[0]].append(1) # right
            new_path2.append([loc[0], loc[1] + 1])
            new_loc.append([loc[0], loc[1] + 1])
            new_path.append(new_path2)
        elif new_leaf2[loc[0] + 1][loc[1]] != 1:
            new_leaf2[0][loc[1] + 1] = 1  # right
            new_path2.append([loc[0], loc[1] + 1])
            new_loc.append([loc[0], loc[1] + 1])
            new_path.append(new_path2)
        new_leaf1 = fill_leave(new_leaf1)
        new_leaf2 = fill_leave(new_leaf2)
        new_leaves.append(new_leaf1)
        new_leaves.append(new_leaf2)
        if next[loc[0] + 1][loc[1]] != 1 and (loc[1] == 0 or (loc[1] > 0 and next[loc[0] + 1][loc[1] - 1] != 1)):
            new_leaf3 = copy.deepcopy(next)
            new_leaf3[loc[0] + 1][loc[1]] = 1
            new_loc.append([loc[0] + 1, loc[1]])
            new_leaf3 = fill_leave(new_leaf3)
            new_path3.append([loc[0] + 1, loc[1]])
            new_leaves.append(new_leaf3)
            new_path.append(new_path3)
    elif loc[0] == len(next) - 1:
        new_path1 = copy.deepcopy(path)
        new_path2 = copy.deepcopy(path)
        new_path3 = copy.deepcopy(path)
        new_leaf1 = copy.deepcopy(next)
        new_leaf2 = copy.deepcopy(next)
        new_leaf1.append([0] * len(next[0]))  # on down
        new_leaf1[loc[0] + 1][loc[1]] = 1
        new_path1.append([loc[0] + 1, loc[1]])
        new_loc.append([loc[0] + 1, loc[1]])
        new_path.append(new_path1)
        if len(new_leaf2[0]) == loc[1] + 1:
            new_leaf2[loc[0]].append(1)  # right
            new_loc.append([loc[0], loc[1] + 1])
            new_path2.append([loc[0], loc[1] + 1])
            new_path.append(new_path2)
        elif new_leaf2[loc[0] - 1][loc[1]] != 1:
            new_leaf2[0][loc[1] + 1] = 1  # right
            new_loc.append([loc[0], loc[1] + 1])
            new_path2.append([loc[0], loc[1] + 1])
            new_path.append(new_path2)
        new_leaf1 = fill_leave(new_leaf1)
        new_leaf2 = fill_leave(new_leaf2)
        new_leaves.append(new_leaf1)
        new_leaves.append(new_leaf2)
        if next[loc[0] - 1][loc[1]] != 1 and (loc[1] == 0 or (loc[1] > 0 and next[loc[0] - 1][loc[1] - 1] != 1)):
            new_leaf3 = copy.deepcopy(next) # up
            new_leaf3[loc[0] - 1][loc[1]] = 1
            new_loc.append([loc[0] - 1, loc[1]])
            new_path3.append([loc[0] - 1, loc[1]])
            new_leaf3 = fill_leave(new_leaf3)
            new_leaves.append(new_leaf3)
            new_path.append(new_path3)
    else:
        new_path1 = copy.deepcopy(path)
        new_path2 = copy.deepcopy(path)
        new_path3 = copy.deepcopy(path)
        if next[loc[0] - 1][loc[1]] != 1 and (loc[1] == 0 or (loc[1] > 0 and next[loc[0] - 1][loc[1] - 1] != 1)):
            new_leaf1 = copy.deepcopy(next)  # up
            new_leaf1[loc[0] - 1][loc[1]] = 1
            new_loc.append([loc[0] - 1, loc[1]])
            new_path1.append([loc[0] - 1, loc[1]])
            new_path.append(new_path1)
            new_leaf3 = fill_leave(new_leaf1)
            new_leaves.append(new_leaf3)
        new_leaf2 = copy.deepcopy(next)
        if len(new_leaf2[0]) == loc[1] + 1:
            new_leaf2[loc[0]].append(1)  # right
            new_loc.append([loc[0], loc[1] + 1])
            new_path2.append([loc[0], loc[1] + 1])
            new_path.append(new_path2)
        elif new_leaf2[loc[0] - 1][loc[1]] != 1 and new_leaf2[loc[0] + 1][loc[1]] != 1:
            new_leaf2[0][loc[1] + 1] = 1  # right
            new_loc.append([loc[0], loc[1] + 1])
            new_path2.append([loc[0], loc[1] + 1])
            new_path.append(new_path2)
        if next[loc[0] + 1][loc[1]] != 1 and (loc[1] == 0 or (loc[1] > 0 and next[loc[0] + 1][loc[1] - 1] != 1)):
            new_leaf3 = copy.deepcopy(next)
            new_leaf3[loc[0] + 1][loc[1]] = 1
            new_loc.append([loc[0] + 1, loc[1]])
            new_path3.append([loc[0] + 1, loc[1]])
            new_path.append(new_path3)
            new_leaf3 = fill_leave(new_leaf3)
            new_leaves.append(new_leaf3)
    return new_leaves, new_loc, new_path

def fill_leave(leaf):
    max_length = 0
    for row in leaf:
        if len(row) > max_length:
            max_length = len(row)
    for i in range(len(leaf)):
        if len(leaf[i]) < max_length:
            leaf[i] = leaf[i] + (max_length - len(leaf[i])) * [0]
    return leaf

def update_path(path): #update path whem upper row is inserted
    for i in range(len(path)):
        path[i][0] = path[i][0] + 1
    return path

def sort_shape(last_table, last_shapes):
    depth_list = []
    valid_table = []
    valid_shapes = []
    for table in last_table:
        depth_list.append(table['D'])
    min_dep = min(depth_list)
    for i in range(len(last_table)):
        if last_table[i]['D'] == min_dep:
            valid_table.append(last_table[i])
            valid_shapes.append(last_shapes[i])
    return valid_table, valid_shapes

def place_final_shape(shape, starts, ends, all_paths, max_first, first, last, all_leaves, final_shapes):
    front_shapes = [[] for _ in range(len(starts) + 1)] #the first one is the original
    front_leaves = [[] for _ in range(len(starts) + 1)]
    front_locs = [[] for _ in range(len(starts) + 1)]
    back_shapes = [[] for _ in range(len(starts) + 1)]
    back_leaves = [[] for _ in range(len(starts) + 1)]
    back_locs = [[] for _ in range(len(starts) + 1)]
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
    for i in range(len(starts)):
        shortest = 100000
        depth_list = []
        for j in range(len(front_shapes[i])):
            available_locs, available_dirs = check_start(front_shapes[i][j], starts[i])
            for k in range(len(available_locs)):
                new_shapes, new_leaves = place_leaf_front(front_shapes[i][j], front_leaves[i][j], available_locs[k], all_paths[first[i] - 1])
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
            front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1], depth_list = remove_short_front(front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1], depth_list)
    if len(depth_list) > final_keep:
        front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1], depth_list = remove_short_front(
            front_shapes[i + 1], front_leaves[i + 1], front_locs[i + 1], depth_list, final_keep)
    #for back
    back_shapes[0].append(copy.deepcopy(original_shape))
    back_leaves[0].append([])
    back_locs[0].append([])
    for i in range(len(ends)):
        shortest = 100000
        depth_list = []
        for j in range(len(back_shapes[i])):
            available_locs, available_dirs = check_end(back_shapes[i][j], ends[i])
            for k in range(len(available_locs)):
                new_shapes, new_leaves = place_leaf_end(back_shapes[i][j], back_leaves[i][j], available_locs[k], all_paths[last[i] - 1])
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
            back_shapes[i + 1], back_leaves[i + 1], back_locs[i + 1], depth_list = remove_short_end(back_shapes[i + 1], back_leaves[i + 1], back_locs[i + 1], depth_list)
        if len(back_shapes[i + 1]) == 0:
            print('back_shapes is empty')
    if len(depth_list) > final_keep:
        back_shapes[i + 1], back_leaves[i + 1], back_locs[i + 1], depth_list = \
            remove_short_end(back_shapes[i + 1], back_leaves[i + 1], back_locs[i + 1], depth_list, final_keep)
    shortest_depth, shortest_shapes = count_shortest(original_shape, all_paths, front_shapes[-1], front_leaves[-1], front_locs[-1], starts, first,
                                    back_shapes[-1], back_leaves[-1], back_locs[-1], ends, last)
    final_shapes = final_shapes + shortest_shapes
    return shortest_depth, front_locs[-1], front_leaves[-1], starts, back_locs[-1], back_leaves[-1], ends, final_shapes

def check_start(temp_shape, start):
    available_locs = []
    available_dir = []
    if start[0] == 0: #only left and down
        if temp_shape[start[0]][start[1] - 1] == 0 and temp_shape[start[0]+1][start[1] - 1] == 0 \
                and (start[1] <= 1 or (start[1] > 1 and temp_shape[start[0]][start[1] - 2]) == 0):
            available_locs.append([start[0], start[1] - 1])
            available_dir.append('l')
        if temp_shape[start[0] + 1][start[1]] == 0 and temp_shape[start[0]+1][start[1] + 1] == 0 \
                and temp_shape[start[0] + 2][start[1]] == 0 and (start[1] == 0 or (temp_shape[start[0] + 1][start[1] - 1]) == 0):
            available_locs.append([start[0] + 1, start[1]])
            available_dir.append('d')
    elif start[0] == len(temp_shape) - 1:
        if temp_shape[start[0]][start[1] - 1] == 0 and temp_shape[start[0]-1][start[1] - 1] == 0 \
                and (start[1] <= 1 or (start[1] > 1 and temp_shape[start[0]][start[1] - 2]) == 0):
            available_locs.append([start[0], start[1] - 1])
            available_dir.append('l')
        if temp_shape[start[0] - 1][start[1]] == 0 and temp_shape[start[0]-1][start[1] + 1] == 0 \
                and temp_shape[start[0] - 2][start[1]] == 0 and (start[1] == 0 or (temp_shape[start[0] - 1][start[1] - 1]) == 0):
            available_locs.append([start[0] - 1, start[1]])
            available_dir.append('u')
    else:
        if temp_shape[start[0]][start[1] - 1] == 0 and temp_shape[start[0]+1][start[1] - 1] == 0 \
                and temp_shape[start[0]-1][start[1] - 1] == 0 and (start[1] <= 1 or (start[1] > 1 and temp_shape[start[0]][start[1] - 2]) == 0):#for left
            available_locs.append([start[0], start[1] - 1])
            available_dir.append('l')
        if temp_shape[start[0] - 1][start[1]] == 0 and temp_shape[start[0] - 1][start[1] + 1] == 0 \
                and (start[1] == 0 or temp_shape[start[0] - 1][start[1] - 1] == 0) and (
                start[0] == 1 or (temp_shape[start[0] - 2][start[1]]) == 0): #for up
            available_locs.append([start[0] - 1, start[1]])
            available_dir.append('u')
        if temp_shape[start[0] + 1][start[1]] == 0 and temp_shape[start[0] + 1][start[1] + 1] == 0 \
                and (start[1] == 0 or temp_shape[start[0] + 1][start[1] - 1] == 0) and (
                start[0] == len(temp_shape) - 2 or (temp_shape[start[0] + 2][start[1]]) == 0): #for down
            available_locs.append([start[0] + 1, start[1]])
            available_dir.append('d')
    return available_locs, available_dir

def check_end(temp_shape, end):
    available_locs = []
    available_dir = []
    if end[0] == 0: #only right and down
        if temp_shape[end[0]][end[1] + 1] == 0 and temp_shape[end[0]+1][end[1] + 1] == 0 \
                and (end[1] >= len(temp_shape[0]) - 2 or (end[1] < len(temp_shape[0]) - 2 and temp_shape[end[0]][end[1] + 2]) == 0):
            available_locs.append([end[0], end[1] + 1])
            available_dir.append('r')
        if temp_shape[end[0] + 1][end[1]] == 0 and temp_shape[end[0]+1][end[1] - 1] == 0 \
                and temp_shape[end[0] + 2][end[1]] == 0 and (end[1] == len(temp_shape[0]) - 1 or (temp_shape[end[0] + 1][end[1] + 1]) == 0):
            available_locs.append([end[0] + 1, end[1]])
            available_dir.append('d')
    elif end[0] == len(temp_shape) - 1:
        if temp_shape[end[0]][end[1] + 1] == 0 and temp_shape[end[0]-1][end[1] + 1] == 0 \
                and (end[1] >= len(temp_shape[0]) - 2 or (end[1] < len(temp_shape[0]) - 2 and temp_shape[end[0]][end[1] + 2]) == 0):
            available_locs.append([end[0], end[1] + 1])
            available_dir.append('r')
        if temp_shape[end[0] - 1][end[1]] == 0 and temp_shape[end[0]-1][end[1] - 1] == 0 \
                and temp_shape[end[0] - 2][end[1]] == 0 and (end[1] == len(temp_shape[0]) - 1 or (temp_shape[end[0] - 1][end[1] + 1]) == 0):
            available_locs.append([end[0] - 1, end[1]])
            available_dir.append('u')
    else:
        if temp_shape[end[0]][end[1] + 1] == 0 and temp_shape[end[0]+1][end[1] + 1] == 0 \
                and temp_shape[end[0]-1][end[1] + 1] == 0 and (end[1] >= len(temp_shape[0]) - 2 or (end[1] < len(temp_shape[0]) - 2 and temp_shape[end[0]][end[1] + 2]) == 0):#for left
            available_locs.append([end[0], end[1] + 1])
            available_dir.append('r')
        if temp_shape[end[0] - 1][end[1]] == 0 and temp_shape[end[0] - 1][end[1] - 1] == 0 \
                and (end[1] == len(temp_shape[0]) - 1 or temp_shape[end[0] - 1][end[1] + 1] == 0) and (
                end[0] == 1 or (temp_shape[end[0] - 2][end[1]]) == 0): #for up
            available_locs.append([end[0] - 1, end[1]])
            available_dir.append('u')
        if temp_shape[end[0] + 1][end[1]] == 0 and temp_shape[end[0] + 1][end[1] - 1] == 0 \
                and (end[1] == len(temp_shape[0]) - 1 or temp_shape[end[0] + 1][end[1] + 1] == 0) and (
                end[0] == len(temp_shape) - 2 or (temp_shape[end[0] + 2][end[1]]) == 0): #for down
            available_locs.append([end[0] + 1, end[1]])
            available_dir.append('d')
    return available_locs, available_dir

def place_leaf_front(temp_shape, temp_leave, loc, paths):
    new_shapes = []
    new_leaves = []
    new_paths = copy.deepcopy(paths)
    valid_paths = [] #any point not exceed range of cluster state
    for i in range(len(new_paths)):
        flag = 0
        offset_y = new_paths[i][-1][0] - loc[0]
        offset_x = new_paths[i][-1][1] - loc[1]
        for j in range(len(new_paths[i])):
            new_paths[i][j][0] = new_paths[i][j][0] - offset_y
            new_paths[i][j][1] = new_paths[i][j][1] - offset_x
            if new_paths[i][j][0] < 0 or new_paths[i][j][1] < 0:
                flag = 1
        if flag == 0:
            valid_paths.append(i)
    for j in valid_paths:
        flag = 0
        new_shape = copy.deepcopy(temp_shape)
        new_shape[loc[0]][loc[1]] = 1
        new_leave = copy.deepcopy(temp_leave)
        for i in range(len(new_paths[j]) - 1, 0, -1):
            available_locs, _ = check_start(new_shape, new_paths[j][i])
            if new_paths[j][i - 1] not in available_locs:
                flag = 1
                break
            else:
                new_shape[new_paths[j][i - 1][0]][new_paths[j][i - 1][1]] = 1
        if flag == 0:
            new_leave.append(j)
            new_shapes.append(new_shape)
            new_leaves.append(new_leave)
    return new_shapes, new_leaves

def place_leaf_end(temp_shape, temp_leave, loc, paths):
    new_shapes = []
    new_leaves = []
    new_paths = copy.deepcopy(paths)
    valid_paths = [] #any point not exceed range of cluster state
    for i in range(len(new_paths)):
        flag = 0
        offset_y = new_paths[i][0][0] - loc[0]
        offset_x = new_paths[i][0][1] - loc[1]
        for j in range(len(new_paths[i])):
            new_paths[i][j][0] = new_paths[i][j][0] - offset_y
            new_paths[i][j][1] = new_paths[i][j][1] - offset_x
            if new_paths[i][j][0] < 0 or new_paths[i][j][1] < 0 or new_paths[i][j][0] > len(temp_shape) -1 or new_paths[i][j][1] > len(temp_shape[0]) -1: #need debug
                flag = 1
        if flag == 0:
            valid_paths.append(i)
    for j in valid_paths:
        flag = 0
        new_shape = copy.deepcopy(temp_shape)
        new_shape[loc[0]][loc[1]] = 1
        new_leave = copy.deepcopy(temp_leave)
        for i in range(len(new_paths[j]) - 1):
            available_locs, _ = check_end(new_shape, new_paths[j][i])
            if new_paths[j][i + 1] not in available_locs:
                flag = 1
                break
            else:
                new_shape[new_paths[j][i + 1][0]][new_paths[j][i + 1][1]] = 1
        if flag == 0:
            new_leave.append(j)
            new_shapes.append(new_shape)
            new_leaves.append(new_leave)
    return new_shapes, new_leaves

def count_depth(new_shape):
    first = 0
    last = 0
    flag_first = 0
    flag_last = 0
    for j in range(len(new_shape[0])):
        for i in range(len(new_shape)):
            if new_shape[i][j] != 0:
                first = j
                flag_first = 1
                break
        if flag_first:
            break
    for j in reversed(range(len(new_shape[0]))):
        for i in range(len(new_shape)):
            if new_shape[i][j] != 0:
                last = j
                flag_last = 1
                break
        if flag_last:
            break
    return last + 1 -first

def remove_short_front(shapes, leaves, locs, depth_list, longest = longest):
    if len(list(set(depth_list))) == 1:
        indexes = []
        for i in range(len(depth_list)):
            indexes.append(i)
        chosen = random.sample(indexes, len(depth_list) - longest)
        chosen.sort()
        for i in reversed(chosen):
            shapes.pop(i)
            leaves.pop(i)
            locs.pop(i)
            depth_list.pop(i)
        return shapes, leaves, locs, depth_list
    while(len(shapes) > longest and len(list(set(depth_list))) != 1):
        max_depth = max(depth_list)
        max_list = []
        for i in range(len(depth_list)):
            if depth_list[i] == max_depth:
                max_list.append(i)
        for i in reversed(max_list):
            shapes.pop(i)
            leaves.pop(i)
            locs.pop(i)
            depth_list.pop(i)
    if len(list(set(depth_list))) == 1 and len(shapes) > longest:
        indexes = []
        for i in range(len(depth_list)):
            indexes.append(i)
        chosen = random.sample(indexes, len(depth_list) - longest)
        chosen.sort()
        for i in reversed(chosen):
            shapes.pop(i)
            leaves.pop(i)
            locs.pop(i)
            depth_list.pop(i)
    return shapes, leaves, locs, depth_list

def remove_short_end(shapes, leaves, locs, depth_list, longest = longest):
    if len(list(set(depth_list))) == 1:
        indexes = []
        for i in range(len(depth_list)):
            indexes.append(i)
        chosen = random.sample(indexes, len(depth_list) - longest)
        chosen.sort()
        for i in reversed(chosen):
            shapes.pop(i)
            leaves.pop(i)
            locs.pop(i)
            depth_list.pop(i)
        return shapes, leaves, locs, depth_list
    while(len(shapes) > longest and len(list(set(depth_list))) != 1):
        max_depth = max(depth_list)
        max_list = []
        for i in range(len(depth_list)):
            if depth_list[i] == max_depth:
                max_list.append(i)
        for i in reversed(max_list):
            shapes.pop(i)
            leaves.pop(i)
            locs.pop(i)
            depth_list.pop(i)
    if len(list(set(depth_list))) == 1 and len(shapes) > longest:
        indexes = []
        for i in range(len(depth_list)):
            indexes.append(i)
        chosen = random.sample(indexes, len(depth_list) - longest)
        chosen.sort()
        for i in reversed(chosen):
            shapes.pop(i)
            leaves.pop(i)
            locs.pop(i)
            depth_list.pop(i)
    return shapes, leaves, locs, depth_list

def count_shortest(original_shape, all_paths, front_shapes, front_leaves, front_locs,
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
            temp_shape, temp_depth = fill_final(original_shape, all_paths, front_leaves[front_indexes[i]], front_locs[front_indexes[i]], starts, first,
                                          back_leaves[back_indexes[j]], back_locs[back_indexes[j]], ends, last)
            if temp_depth < shortest_depth:
                shortest_depth = temp_depth
            final_shapes.append(temp_shape)
    return shortest_depth, final_shapes

def fill_final(original_shape, all_paths, front_leave, front_loc,
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
    new_shape = remove_empty(new_shape)
    return new_shape, count_depth(new_shape)

def remove_empty(shape):
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
