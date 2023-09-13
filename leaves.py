import copy

def place_leaves(table, shapes, first, last, rows):
    last_table = table[-1]
    last_shapes = shapes[-1]
    final_shapes = []
    all_length = first + last
    available_length = list(set(all_length))
    available_length.sort()
    all_leaves = generate_leaves(available_length) #generate leaves of all the length
    front_leaves = []
    back_leaves = []
    for i in range(len(last_table)):
        starts = copy.deepcopy(last_table[i]['starts'])
        ends = copy.deepcopy(last_table[i]['ends'])
        shape = last_shapes[i]
    return final_shapes

def generate_leaves(available_length):
    max_length = max(available_length)
    leaves = [[] for _ in range(max_length)]
    leaves[0] = [[1]]
    queue = [[[1]]]
    length = 1
    queue_loc = [[0,0]] #location for the newest node
    queue_length = [1]
    while queue != []:
        next = queue.pop(0)
        loc = queue_loc.pop(0)
        length = queue_length.pop(0)
        new_leaves, locs = generate_next(next, loc)
        for j in range(len(new_leaves)):
            if length < max_length:
                queue.append(new_leaves[j])
                queue_loc.append(locs[j])
                queue_length.append(length + 1)
            if new_leaves[j] not in leaves[length]:
                leaves[length].append(new_leaves[j])
    return leaves

def generate_next(next, loc):
    new_leaves = []
    new_loc = []
    if len(next) == 1:
        new_leaf1 = copy.deepcopy(next)
        new_leaf2 = copy.deepcopy(next)
        new_leaf3 = copy.deepcopy(next)
        new_leaf1.insert(0, [0]*len(next[0])) #on top
        new_leaf1[loc[0]][loc[1]] = 1
        new_loc.append([loc[0], loc[1]]) #right
        new_leaf2[0].append(1)
        new_loc.append([loc[0], loc[1] + 1])
        new_leaf3.append([0]*len(next[0])) #on down
        new_leaf3[loc[0] + 1][loc[1]] = 1
        new_loc.append([loc[0] + 1, loc[1]])
        new_leaf1 = fill_leave(new_leaf1)
        new_leaf2 = fill_leave(new_leaf2)
        new_leaf3 = fill_leave(new_leaf3)
        new_leaves.append(new_leaf1)
        new_leaves.append(new_leaf2)
        new_leaves.append(new_leaf3)
    elif loc[0] == 0:
        new_leaf1 = copy.deepcopy(next)
        new_leaf2 = copy.deepcopy(next)
        new_leaf1.insert(0, [0] * len(next[0]))  # on top
        new_leaf1[loc[0]][loc[1]] = 1
        new_loc.append([loc[0], loc[1]])
        if len(new_leaf2[0]) == loc[1] + 1:
            new_leaf2[0].append(1) # right
            new_loc.append([loc[0], loc[1] + 1])
        elif new_leaf2[loc[0] + 1][loc[1]] != 1:
            new_leaf2[0][loc[1] + 1] = 1  # right
            new_loc.append([loc[0], loc[1] + 1])
        new_leaf1 = fill_leave(new_leaf1)
        new_leaf2 = fill_leave(new_leaf2)
        new_leaves.append(new_leaf1)
        new_leaves.append(new_leaf2)
        if next[loc[0] + 1][loc[1]] != 1 and (loc[1] == 0 or (loc[1] > 0 and next[loc[0] + 1][loc[1] + 1] != 1)):
            new_leaf3 = copy.deepcopy(next)
            new_leaf3[loc[0] + 1][loc[1]] = 1
            new_loc.append([loc[0] + 1, loc[1]])
            new_leaf3 = fill_leave(new_leaf3)
            new_leaves.append(new_leaf3)
    elif loc[0] == len(next) - 1:
        new_leaf1 = copy.deepcopy(next)
        new_leaf2 = copy.deepcopy(next)
        new_leaf1.append([0] * len(next[0]))  # on down
        new_leaf1[loc[0] + 1][loc[1]] = 1
        new_loc.append([loc[0], loc[1]])  # right
        if len(new_leaf2[0]) == loc[1] + 1:
            new_leaf2[0].append(1)  # right
            new_loc.append([loc[0], loc[1] + 1])
        elif new_leaf2[loc[0] - 1][loc[1]] != 1:
            new_leaf2[0][loc[1] + 1] = 1  # right
            new_loc.append([loc[0], loc[1] + 1])
        new_leaf1 = fill_leave(new_leaf1)
        new_leaf2 = fill_leave(new_leaf2)
        new_leaves.append(new_leaf1)
        new_leaves.append(new_leaf2)
        if next[loc[0] - 1][loc[1]] != 1 and (loc[1] == 0 or (loc[1] > 0 and next[loc[0] + 1][loc[1] - 1] != 1)):
            new_leaf3 = copy.deepcopy(next) # up
            new_leaf3[loc[0] - 1][loc[1]] = 1
            new_loc.append([loc[0] - 1, loc[1]])
            new_leaf3 = fill_leave(new_leaf3)
            new_leaves.append(new_leaf3)
    else:
        if next[loc[0] - 1][loc[1]] != 1 and (loc[1] == 0 or (loc[1] > 0 and next[loc[0] + 1][loc[1] - 1] != 1)):
            new_leaf1 = copy.deepcopy(next)  # up
            new_leaf1[loc[0] - 1][loc[1]] = 1
            new_loc.append([loc[0] - 1, loc[1]])
            new_leaf3 = fill_leave(new_leaf1)
            new_leaves.append(new_leaf3)
        new_leaf2 = copy.deepcopy(next)
        if len(new_leaf2[0]) == loc[1] + 1:
            new_leaf2[0].append(1)  # right
            new_loc.append([loc[0], loc[1] + 1])
        elif new_leaf2[loc[0] - 1][loc[1]] != 1 and new_leaf2[loc[0] + 1][loc[1]] != 1:
            new_leaf2[0][loc[1] + 1] = 1  # right
            new_loc.append([loc[0], loc[1] + 1])
        if next[loc[0] + 1][loc[1]] != 1 and (loc[1] == 0 or (loc[1] > 0 and next[loc[0] + 1][loc[1] + 1] != 1)):
            new_leaf3 = copy.deepcopy(next)
            new_leaf3[loc[0] + 1][loc[1]] = 1
            new_loc.append([loc[0] + 1, loc[1]])
            new_leaf3 = fill_leave(new_leaf3)
            new_leaves.append(new_leaf3)
    return new_leaves, new_loc

def fill_leave(leaf):
    max_length = 0
    for row in leaf:
        if len(row) > max_length:
            max_length = len(row)
    for i in range(len(leaf)):
        if len(leaf[i]) < max_length:
            leaf[i] = leaf[i] + (max_length - len(leaf[i])) * [0]
    return leaf