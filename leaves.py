import copy
import random

longest = 1000
def place_leaves(table, shapes, first, last, rows):
    last_table = table[-1]
    last_shapes = shapes[-1]
    final_shapes = []
    max_first = max(first)
    all_length = first + last
    available_length = list(set(all_length))
    available_length.sort()
    all_leaves, all_paths = generate_leaves(available_length) #generate leaves of all the length
    for i in range(len(last_table)):
        starts = copy.deepcopy(last_table[i]['starts'])
        ends = copy.deepcopy(last_table[i]['ends'])
        shape = last_shapes[i]
        new_shape = place_final_shape(shape, starts, ends, all_paths, max_first, first, last)
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

def place_final_shape(shape, starts, ends, all_paths, max_first, first, last):
    front_shapes = [[] for _ in range(len(starts) + 1)] #the first one is the original
    back_shapes = [[] for _ in range(len(starts) + 1)]
    for i in range(len(starts)):
        starts[i][1] = starts[i][1] + max_first
        ends[i][1] = ends[i][1] + max_first
    # starts.sort(reverse=True, key=lambda x: x[1])
    # ends.sort(key=lambda x: x[1])
    original_shape = copy.deepcopy(shape)
    for i in range(len(original_shape)):
        original_shape[i] = [0] * max_first + original_shape[i] + [0] * max(last)
    front_shapes[0].append(copy.deepcopy(original_shape))
    for i in range(len(starts)):
        print('g')
        shortest = 100000
        depth_list = []
        for temp_shape in front_shapes[i]:
            available_locs = check_start(temp_shape, starts[i])
            for loc in available_locs:
                new_shapes = place_leaf_front(temp_shape, loc, all_paths[first[i] - 1])
                for new_shape in new_shapes:
                    front_shapes[i + 1].append(new_shape)
                    depth = count_depth(new_shape)
                    depth_list.append(depth)
                    if depth < shortest:
                        shortest = depth
        if len(depth_list) > longest:
            front_shapes[i + 1] = remove_short(front_shapes[i + 1], depth_list)

    print('g')

def check_start(temp_shape, start):
    available_locs = []
    if start[0] == 0: #only left and down
        if temp_shape[start[0]][start[1] - 1] == 0 and temp_shape[start[0]+1][start[1] - 1] == 0 \
                and (start[1] <= 1 or (start[1] > 1 and temp_shape[start[0]][start[1] - 2]) == 0):
            available_locs.append([start[0], start[1] - 1])
        if temp_shape[start[0] + 1][start[1]] == 0 and temp_shape[start[0]+1][start[1] + 1] == 0 \
                and temp_shape[start[0] + 2][start[1]] == 0 and (start[1] == 0 or (temp_shape[start[0] + 1][start[1] - 1]) == 0):
            available_locs.append([start[0] + 1, start[1]])
    elif start[0] == len(temp_shape) - 1:
        if temp_shape[start[0]][start[1] - 1] == 0 and temp_shape[start[0]-1][start[1] - 1] == 0 \
                and (start[1] <= 1 or (start[1] > 1 and temp_shape[start[0]][start[1] - 2]) == 0):
            available_locs.append([start[0], start[1] - 1])
        if temp_shape[start[0] - 1][start[1]] == 0 and temp_shape[start[0]-1][start[1] + 1] == 0 \
                and temp_shape[start[0] - 2][start[1]] == 0 and (start[1] == 0 or (temp_shape[start[0] - 1][start[1] - 1]) == 0):
            available_locs.append([start[0] - 1, start[1]])
    else:
        if temp_shape[start[0]][start[1] - 1] == 0 and temp_shape[start[0]+1][start[1] - 1] == 0 \
                and temp_shape[start[0]-1][start[1] - 1] == 0 and (start[1] <= 1 or (start[1] > 1 and temp_shape[start[0]][start[1] - 2]) == 0):#for left
            available_locs.append([start[0], start[1] - 1])
        if temp_shape[start[0] - 1][start[1]] == 0 and temp_shape[start[0] - 1][start[1] + 1] == 0 \
                and (start[1] == 0 or temp_shape[start[0] - 1][start[1] - 1] == 0) and (
                start[0] == 1 or (temp_shape[start[0] - 2][start[1]]) == 0): #for up
            available_locs.append([start[0] - 1, start[1]])
        if temp_shape[start[0] + 1][start[1]] == 0 and temp_shape[start[0] + 1][start[1] + 1] == 0 \
                and (start[1] == 0 or temp_shape[start[0] + 1][start[1] - 1] == 0) and (
                start[0] == len(temp_shape) - 2 or (temp_shape[start[0] + 2][start[1]]) == 0): #for down
            available_locs.append([start[0] + 1, start[1]])
    return available_locs

def place_leaf_front(temp_shape, loc, paths):
    new_shapes = []
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
            valid_paths.append(new_paths[i])
    for path in valid_paths:
        flag = 0
        new_shape = copy.deepcopy(temp_shape)
        new_shape[loc[0]][loc[1]] = 1
        for i in range(len(path) - 1, 0, -1):
            available_locs = check_start(new_shape, path[i])
            if path[i - 1] not in available_locs:
                flag = 1
                break
            else:
                new_shape[path[i - 1][0]][path[i - 1][1]] = 1
        if flag == 0:
            new_shapes.append(new_shape)
    return new_shapes

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

def remove_short(shapes, depth_list):
    if len(list(set(depth_list))) == 1:
        indexes = []
        for i in range(len(depth_list)):
            indexes.append(i)
        chosen = random.sample(indexes, len(depth_list) - longest)
        chosen.sort()
        for i in reversed(chosen):
            shapes.pop(i)
            depth_list.pop(i)
        return shapes
    while(len(shapes) > longest and len(list(set(depth_list))) != 1):
        max_depth = max(depth_list)
        max_list = []
        for i in range(len(depth_list)):
            if depth_list[i] == max_depth:
                max_list.append(i)
        for i in reversed(max_list):
            shapes.pop(i)
            depth_list.pop(i)
    if len(list(set(depth_list))) == 1 and len(shapes) > longest:
        indexes = []
        for i in range(len(depth_list)):
            indexes.append(i)
        indexes.sort()
        for i in reversed(indexes):
            shapes.pop(i)
            depth_list.pop(i)
    return shapes

