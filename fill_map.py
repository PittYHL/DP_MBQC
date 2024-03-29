from placement import *
import math

special_W = 1

def fill_A(shapes, fronts, spaces, locs, same_qubit, starts, ends, wire_targets, rows):
    valid = []  # valid shpae after fill A
    new_shapes = []
    new_Spaces = []
    new_fronts = []
    new_starts = []
    new_ends = []
    for i in range(len(shapes)):
        shape = shapes[i]
        front = fronts[i]
        start = starts[i]
        end = ends[i]
        first_base = front[locs[0]]
        second_base = front[locs[1]]
        wire_target = wire_targets[i]
        if first_base[0] > second_base[0]:
            temp = first_base
            first_base = second_base
            second_base = temp
        if first_base[0] + 2 == second_base[0] and first_base[1] == second_base[1]:  # rr
            if shapes[i][first_base[0] + 1][first_base[1]] == 0 or same_qubit:  # constraints for rr
                valid.append(i)
                extra_column = 0
                if first_base[1] == len(shape[0]) - 1:
                    extra_column = 1
                for j in range(len(shape)):
                    shape[j] = shape[j] + [0] * extra_column
                shape[first_base[0]][first_base[1] + 1] = 1
                shape[first_base[0] + 1][first_base[1] + 1] = 1
                shape[first_base[0] + 2][first_base[1] + 1] = 1
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0], first_base[1] + 1])
                front.append([second_base[0], second_base[1] + 1])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 3 == second_base[0] and first_base[1] + 1 == second_base[1]:  # ru
            if shapes[i][first_base[0] + 1][first_base[1]] == 0:  # constraints for ru
                valid.append(i)
                shape[first_base[0]][first_base[1] + 1] = 1
                shape[first_base[0] + 1][first_base[1] + 1] = 1
                shape[first_base[0] + 2][first_base[1] + 1] = 1
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0], first_base[1] + 1])
                front.append([second_base[0] - 1, second_base[1]])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 3 == second_base[0] and first_base[1] - 1 == second_base[1]:  # dr
            if shapes[i][first_base[0] + 2][first_base[1] - 1] == 0:  # constraints for ru
                valid.append(i)
                shape[first_base[0] + 1][first_base[1]] = 1
                shape[first_base[0] + 2][first_base[1]] = 1
                shape[first_base[0] + 3][first_base[1]] = 1
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                #front[locs[0]][1] = front[locs[0]][1] + 1
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0] + 1, first_base[1]])
                front.append([second_base[0], second_base[1] + 1])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 4 == second_base[0] and first_base[1] == second_base[1]:  # du
            if shapes[i][first_base[0] + 2][first_base[1] - 1] == 0:  # constraints for ru
                valid.append(i)
                shape[first_base[0] + 1][first_base[1]] = 1
                shape[first_base[0] + 2][first_base[1]] = 1
                shape[first_base[0] + 3][first_base[1]] = 1
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0] + 1, first_base[1]])
                front.append([second_base[0] - 1, second_base[1]])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif special_W and math.fabs(first_base[0] - second_base[0]) >= 2:
            if second_base[0] - first_base[0] == 2:
                if (first_base[1] - second_base[1]) > 0 and (first_base[1] - second_base[1]) % 2 == 0: #r,rw
                    valid.append(i)
                    extra_column = 0
                    if first_base[1] == len(shape[0]) - 1:
                        extra_column = 1
                    for j in range(len(shape)):
                        shape[j] = shape[j] + [0] * extra_column
                    shape[first_base[0]][first_base[1] + 1] = 1
                    shape[first_base[0] + 1][first_base[1] + 1] = 1
                    shape[first_base[0] + 2][first_base[1] + 1] = 1
                    for j in range(second_base[1] + 1, first_base[1] + 1):
                        shape[second_base[0]][j] = 2
                    shape, space = fill_shape(shape)
                    new_shapes.append(shape)
                    new_Spaces.append(space)
                    front.pop(max(locs))
                    front.pop(min(locs))
                    front.append([first_base[0], first_base[1] + 1])
                    front.append([second_base[0], first_base[1] + 1])
                    new_fronts.append(front)
                    new_starts.append(start)
                    new_ends.append(end)
                elif (second_base[1] - first_base[1]) > 0 and (second_base[1] - first_base[1]) % 2 == 0: #rw,r
                    valid.append(i)
                    extra_column = 0
                    if second_base[1] == len(shape[0]) - 1:
                        extra_column = 1
                    for j in range(len(shape)):
                        shape[j] = shape[j] + [0] * extra_column
                    shape[first_base[0]][second_base[1] + 1] = 1
                    shape[first_base[0] + 1][second_base[1] + 1] = 1
                    shape[first_base[0] + 2][second_base[1] + 1] = 1
                    for j in range(first_base[1] + 1, second_base[1] + 1):
                        shape[first_base[0]][j] = 2
                    shape, space = fill_shape(shape)
                    new_shapes.append(shape)
                    new_Spaces.append(space)
                    front.pop(max(locs))
                    front.pop(min(locs))
                    front.append([first_base[0], second_base[1] + 1])
                    front.append([second_base[0], second_base[1] + 1])
                    new_fronts.append(front)
                    new_starts.append(start)
                    new_ends.append(end)
            elif second_base[0] - first_base[0] > 2:
                if (first_base[1] - second_base[1]) > 0:
                    valid.append(i)
                    shape[first_base[0] + 1][first_base[1]] = 1
                    shape[first_base[0] + 2][first_base[1]] = 1
                    shape[first_base[0] + 3][first_base[1]] = 1
                    new_shape, new_front, _, _, _ = place_W(shape, second_base, rows, len(shape), front, [],
                                                                        [], [], [first_base[0] + 3, first_base[1]], 1000, wire_target,
                                                                        [], 0)
                    if new_shape != []:
                        shape = new_shape[0]
                        front = new_front[0]
                        shape, space = fill_shape(shape)
                        new_shapes.append(shape)
                        new_Spaces.append(space)
                        front.pop(max(locs))
                        front.pop(min(locs))
                        front.append([first_base[0] + 1, first_base[1]])
                        front.append([first_base[0] + 3, first_base[1]])
                        new_fronts.append(front)
                        new_starts.append(start)
                        new_ends.append(end)
                elif (second_base[1] - first_base[1]) > 0:
                    valid.append(i)
                    shape[second_base[0] - 1][second_base[1]] = 1
                    shape[second_base[0] - 2][second_base[1]] = 1
                    shape[second_base[0] - 3][second_base[1]] = 1
                    new_shape, new_front, _, _, _ = place_W(shape, first_base, rows, len(shape), front, [],
                                                                        [], [], [second_base[0] - 3, second_base[1]], 1000, wire_target,
                                                                        [], 0)
                    if new_shape != []:
                        shape = new_shape[0]
                        front = new_front[0]
                        shape, space = fill_shape(shape)
                        new_shapes.append(shape)
                        new_Spaces.append(space)
                        front.pop(max(locs))
                        front.pop(min(locs))
                        front.append([second_base[0] - 3, second_base[1]])
                        front.append([second_base[0] - 1, second_base[1]])
                        new_fronts.append(front)
                        new_starts.append(start)
                        new_ends.append(end)

    return new_shapes, new_fronts, new_Spaces, valid, new_starts, new_ends

def fill_B(shapes, fronts, spaces, locs, same_qubit, starts, ends, wire_targets, rows): #may need to add more cases
    valid = [] #valid shpae after fill B
    new_shapes = []
    new_Spaces = []
    new_fronts = []
    new_starts = []
    new_ends = []
    for i in range(len(shapes)):
        shape = shapes[i]
        front = fronts[i]
        start = starts[i]
        end = ends[i]
        first_base = front[locs[0]]
        second_base = front[locs[1]]
        wire_target = wire_targets[i]
        if first_base[0] > second_base[0]:
            temp = first_base
            first_base = second_base
            second_base = temp
        if first_base[0] + 2 == second_base[0] and first_base[1] == second_base[1]: #rr
            if shapes[i][first_base[0] + 1][first_base[1]] == 0 or same_qubit: #constraints for rr
                valid.append(i)
                extra_column = first_base[1] + 3 - len(shape[0])
                for j in range(len(shape)):
                    shape[j] = shape[j] + [0]*extra_column
                shape[first_base[0]][first_base[1] + 1: first_base[1] + 3] = [1,1]
                shape[first_base[0] + 1][first_base[1] + 1: first_base[1] + 3] = [1, 1]
                shape[first_base[0] + 2][first_base[1] + 1: first_base[1] + 3] = [1, 1]
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0], first_base[1] + 2])
                front.append([second_base[0], second_base[1] + 2])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 3 == second_base[0] and first_base[1] + 1 == second_base[1]: #ru
            if shapes[i][first_base[0] + 1][first_base[1]] == 0: #constraints for ru
                valid.append(i)
                extra_column = first_base[1] + 3 - len(shape[0])
                for j in range(len(shape)):
                    shape[j] = shape[j] + [0] * extra_column
                shape[first_base[0]][first_base[1] + 1: first_base[1] + 3] = [1, 1]
                shape[first_base[0] + 1][first_base[1] + 1: first_base[1] + 3] = [1, 1]
                shape[first_base[0] + 2][first_base[1] + 1: first_base[1] + 3] = [1, 1]
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0], first_base[1] + 2])
                front.append([second_base[0] - 1, second_base[1] + 1])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 3 == second_base[0] and first_base[1] - 1 == second_base[1]: #dr
            if shapes[i][first_base[0] + 2][first_base[1] - 1] == 0: #constraints for ru
                valid.append(i)
                extra_column = first_base[1] + 2 - len(shape[0])
                for j in range(len(shape)):
                    shape[j] = shape[j] + [0] * extra_column
                shape[first_base[0] + 1][first_base[1]: first_base[1] + 2] = [1, 1]
                shape[first_base[0] + 2][first_base[1]: first_base[1] + 2] = [1, 1]
                shape[first_base[0] + 3][first_base[1]: first_base[1] + 2] = [1, 1]
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0] + 1, first_base[1] + 1])
                front.append([second_base[0], second_base[1] + 2])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 4 == second_base[0] and first_base[1] == second_base[1]: #du
            if shapes[i][first_base[0] + 2][first_base[1] - 1] == 0: #constraints for ru
                valid.append(i)
                extra_column = first_base[1] + 2 - len(shape[0])
                for j in range(len(shape)):
                    shape[j] = shape[j] + [0] * extra_column
                shape[first_base[0] + 1][first_base[1]: first_base[1] + 2] = [1, 1]
                shape[first_base[0] + 2][first_base[1]: first_base[1] + 2] = [1, 1]
                shape[first_base[0] + 3][first_base[1]: first_base[1] + 2] = [1, 1]
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0] + 1, first_base[1] + 1])
                front.append([second_base[0] - 1, second_base[1] + 1])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif special_W and math.fabs(first_base[0] - second_base[0]) >= 2:
            if second_base[0] - first_base[0] == 2:
                if (first_base[1] - second_base[1]) > 0 and (first_base[1] - second_base[1]) % 2 == 0: #r,rw
                    valid.append(i)
                    extra_column = first_base[1] + 3 - len(shape[0])
                    for j in range(len(shape)):
                        shape[j] = shape[j] + [0] * extra_column
                    shape[first_base[0]][first_base[1] + 1: first_base[1] + 3] = [1, 1]
                    shape[first_base[0] + 1][first_base[1] + 1: first_base[1] + 3] = [1, 1]
                    shape[first_base[0] + 2][first_base[1] + 1: first_base[1] + 3] = [1, 1]
                    for j in range(second_base[1] + 1, first_base[1] + 1):
                        shape[second_base[0]][j] = 2
                    shape, space = fill_shape(shape)
                    new_shapes.append(shape)
                    new_Spaces.append(space)
                    front.pop(max(locs))
                    front.pop(min(locs))
                    front.append([first_base[0], first_base[1] + 2])
                    front.append([second_base[0], first_base[1] + 2])
                    new_fronts.append(front)
                    new_starts.append(start)
                    new_ends.append(end)
                elif (second_base[1] - first_base[1]) > 0 and (second_base[1] - first_base[1]) % 2 == 0: #rw,r
                    valid.append(i)
                    extra_column = second_base[1] + 3 - len(shape[0])
                    for j in range(len(shape)):
                        shape[j] = shape[j] + [0] * extra_column
                    shape[first_base[0]][second_base[1] + 1: second_base[1] + 3] = [1, 1]
                    shape[first_base[0] + 1][second_base[1] + 1: second_base[1] + 3] = [1, 1]
                    shape[first_base[0] + 2][second_base[1] + 1: second_base[1] + 3] = [1, 1]
                    for j in range(first_base[1] + 1, second_base[1] + 1):
                        shape[first_base[0]][j] = 2
                    shape, space = fill_shape(shape)
                    new_shapes.append(shape)
                    new_Spaces.append(space)
                    front.pop(max(locs))
                    front.pop(min(locs))
                    front.append([first_base[0], second_base[1] + 2])
                    front.append([second_base[0], second_base[1] + 2])
                    new_fronts.append(front)
                    new_starts.append(start)
                    new_ends.append(end)
            elif second_base[0] - first_base[0] > 2:
                if (first_base[1] - second_base[1]) == 1 and (second_base[0] - first_base[0]) % 2 == 1: #vertical w
                    valid.append(i)
                    extra_column = first_base[1] + 2 - len(shape[0])
                    for j in range(len(shape)):
                        shape[j] = shape[j] + [0] * extra_column
                    shape[first_base[0] + 1][first_base[1]: first_base[1] + 2] = [1, 1]
                    shape[first_base[0] + 2][first_base[1]: first_base[1] + 2] = [1, 1]
                    shape[first_base[0] + 3][first_base[1]: first_base[1] + 2] = [1, 1]
                    if shape[second_base[0] - 1][second_base[1] - 1] == 0:
                        for j in range(first_base[0] + 3, second_base[0]):
                            shape[j][second_base[1]] = 2
                    else:
                        for j in range(first_base[0] + 4, second_base[0] + 1):
                            shape[j][second_base[1] + 1] = 2
                    shape, space = fill_shape(shape)
                    new_shapes.append(shape)
                    new_Spaces.append(space)
                    front.pop(max(locs))
                    front.pop(min(locs))
                    front.append([first_base[0] + 1, first_base[1] + 1])
                    front.append([first_base[0] + 3, first_base[1] + 1])
                    new_fronts.append(front)
                    new_starts.append(start)
                    new_ends.append(end)
                elif (second_base[1] - first_base[1]) == 1 and (second_base[0] - first_base[0]) % 2 == 1: #vertical w
                    valid.append(i)
                    extra_column = second_base[1] + 2 - len(shape[0])
                    for j in range(len(shape)):
                        shape[j] = shape[j] + [0] * extra_column
                    shape[second_base[0] - 1][second_base[1]: second_base[1] + 2] = [1, 1]
                    shape[second_base[0] - 2][second_base[1]: second_base[1] + 2] = [1, 1]
                    shape[second_base[0] - 3][second_base[1]: second_base[1] + 2] = [1, 1]
                    if shape[first_base[0] + 1][first_base[1] - 1] == 0:
                        for j in range(first_base[0] + 1, second_base[0] - 2):
                            shape[j][first_base[1]] = 2
                    else:
                        for j in range(first_base[0], second_base[0] - 3):
                            shape[j][first_base[1] + 1] = 2
                    shape, space = fill_shape(shape)
                    new_shapes.append(shape)
                    new_Spaces.append(space)
                    front.pop(max(locs))
                    front.pop(min(locs))
                    front.append([second_base[0] - 3, second_base[1] + 1])
                    front.append([second_base[0] - 1, second_base[1] + 1])
                    new_fronts.append(front)
                    new_starts.append(start)
                    new_ends.append(end)
                elif (first_base[1] - second_base[1]) > 1:
                    valid.append(i)
                    extra_column = first_base[1] + 2 - len(shape[0])
                    for j in range(len(shape)):
                        shape[j] = shape[j] + [0] * extra_column
                    shape[first_base[0] + 1][first_base[1]: first_base[1] + 2] = [1, 1]
                    shape[first_base[0] + 2][first_base[1]: first_base[1] + 2] = [1, 1]
                    shape[first_base[0] + 3][first_base[1]: first_base[1] + 2] = [1, 1]
                    new_shape, new_front, _, _, _ = place_W(shape, second_base, rows, len(shape), front, [],
                                                                        [], [], [first_base[0] + 3, first_base[1]], 1000, wire_target,
                                                                        [], 0)
                    if new_shape != []:
                        shape = new_shape[0]
                        front = new_front[0]
                        shape, space = fill_shape(shape)
                        new_shapes.append(shape)
                        new_Spaces.append(space)
                        front.pop(max(locs))
                        front.pop(min(locs))
                        front.append([first_base[0] + 1, first_base[1] + 1])
                        front.append([first_base[0] + 3, first_base[1] + 1])
                        new_fronts.append(front)
                        new_starts.append(start)
                        new_ends.append(end)
                elif (second_base[1] - first_base[1]) > 1:
                    valid.append(i)
                    extra_column = second_base[1] + 2 - len(shape[0])
                    for j in range(len(shape)):
                        shape[j] = shape[j] + [0] * extra_column
                    shape[second_base[0] - 1][second_base[1]: second_base[1] + 2] = [1, 1]
                    shape[second_base[0] - 2][second_base[1]: second_base[1] + 2] = [1, 1]
                    shape[second_base[0] - 3][second_base[1]: second_base[1] + 2] = [1, 1]
                    new_shape, new_front, _, _, _ = place_W(shape, first_base, rows, len(shape), front, [],
                                                                        [], [], [second_base[0] - 3, second_base[1]], 1000, wire_target,
                                                                        [], 0)
                    if new_shape != []:
                        shape = new_shape[0]
                        front = new_front[0]
                        shape, space = fill_shape(shape)
                        new_shapes.append(shape)
                        new_Spaces.append(space)
                        front.pop(max(locs))
                        front.pop(min(locs))
                        front.append([second_base[0] - 3, second_base[1] + 1])
                        front.append([second_base[0] - 1, second_base[1] + 1])
                        new_fronts.append(front)
                        new_starts.append(start)
                        new_ends.append(end)
    return new_shapes, new_fronts, new_Spaces, valid, new_starts, new_ends

def fill_B1(shapes, fronts, spaces, locs, same_qubit, starts, ends, wire_targets, rows, nodes, nextnext): #may need to add more cases
    before = []
    for i in range(len(nodes)):
        for j in range(len(nodes[i])):
            if nodes[i][j] == nextnext:
                before.append(nodes[i][j - 1])
                break
        if len(before) == 2:
            break
    gate, _ = before[0].split('.')
    if gate == 'A': #decide which one is fill point
        fill_p = 'u'
    else:
        fill_p = 'd'
    valid = [] #valid shpae after fill B
    new_shapes = []
    new_Spaces = []
    new_fronts = []
    new_starts = []
    new_ends = []
    for i in range(len(shapes)):
        shape = shapes[i]
        front = fronts[i]
        start = starts[i]
        end = ends[i]
        first_base = front[locs[0]]
        second_base = front[locs[1]]
        wire_target = wire_targets[i]
        if first_base[0] > second_base[0]:
            temp = first_base
            first_base = second_base
            second_base = temp
        if fill_p == 'u' and first_base[0] + 2 == second_base[0] and first_base[1] == second_base[1] + 1: #rr
            if shapes[i][first_base[0] + 1][first_base[1]] == 0 or same_qubit: #constraints for rr
                valid.append(i)
                extra_column = first_base[1] + 2 - len(shape[0])
                for j in range(len(shape)):
                    shape[j] = shape[j] + [0]*extra_column
                shape[first_base[0]][first_base[1] + 1] = 1
                shape[first_base[0] + 1][first_base[1]: first_base[1] + 3] = [1, 1]
                shape[first_base[0] + 2][first_base[1]: first_base[1] + 3] = [1, 1]
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0], first_base[1] + 1])
                front.append([second_base[0], second_base[1] + 2])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif fill_p == 'd' and first_base[0] + 2 == second_base[0] and first_base[1] + 1 == second_base[1]: #rr
            if shapes[i][first_base[0] + 1][first_base[1] + 1] == 0 or same_qubit: #constraints for rr
                valid.append(i)
                extra_column = second_base[1] + 2 - len(shape[0])
                for j in range(len(shape)):
                    shape[j] = shape[j] + [0]*extra_column
                shape[first_base[0] + 2][first_base[1] + 2] = 1
                shape[first_base[0] + 1][first_base[1] + 1: first_base[1] + 3] = [1, 1]
                shape[first_base[0]][first_base[1] + 1: first_base[1] + 3] = [1, 1]
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0], first_base[1] + 2])
                front.append([second_base[0], second_base[1] + 1])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif fill_p == 'u' and first_base[0] + 3 == second_base[0] and first_base[1] == second_base[1]: #ru
            if shapes[i][first_base[0] + 1][first_base[1]] == 0: #constraints for ru
                valid.append(i)
                extra_column = first_base[1] + 2 - len(shape[0])
                for j in range(len(shape)):
                    shape[j] = shape[j] + [0] * extra_column
                shape[first_base[0]][first_base[1] + 1] = 1
                shape[first_base[0] + 1][first_base[1]: first_base[1] + 2] = [1, 1]
                shape[first_base[0] + 2][first_base[1]: first_base[1] + 2] = [1, 1]
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0], first_base[1] + 1])
                front.append([second_base[0] - 1, second_base[1] + 1])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif fill_p == 'd' and first_base[0] + 3 == second_base[0] and first_base[1] == second_base[1]: #ru
            if shapes[i][first_base[0] + 1][first_base[1]] == 0: #constraints for ru
                valid.append(i)
                extra_column = first_base[1] + 2 - len(shape[0])
                for j in range(len(shape)):
                    shape[j] = shape[j] + [0] * extra_column
                shape[first_base[0] + 3][first_base[1] + 1] = 1
                shape[first_base[0] + 2][first_base[1]: first_base[1] + 2] = [1, 1]
                shape[first_base[0] + 1][first_base[1]: first_base[1] + 2] = [1, 1]
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                front.pop(max(locs))
                front.pop(min(locs))
                front.append([first_base[0] + 1, first_base[1] + 1])
                front.append([second_base[0], second_base[1] + 1])
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        # elif special_W and math.fabs(first_base[0] - second_base[0]) >= 2:
        #     if second_base[0] - first_base[0] == 2:
        #         if (first_base[1] - second_base[1]) > 0 and (first_base[1] - second_base[1]) % 2 == 0: #r,rw
        #             valid.append(i)
        #             extra_column = first_base[1] + 3 - len(shape[0])
        #             for j in range(len(shape)):
        #                 shape[j] = shape[j] + [0] * extra_column
        #             shape[first_base[0]][first_base[1] + 1: first_base[1] + 3] = [1, 1]
        #             shape[first_base[0] + 1][first_base[1] + 1: first_base[1] + 3] = [1, 1]
        #             shape[first_base[0] + 2][first_base[1] + 1: first_base[1] + 3] = [1, 1]
        #             for j in range(second_base[1] + 1, first_base[1] + 1):
        #                 shape[second_base[0]][j] = 2
        #             shape, space = fill_shape(shape)
        #             new_shapes.append(shape)
        #             new_Spaces.append(space)
        #             front.pop(max(locs))
        #             front.pop(min(locs))
        #             front.append([first_base[0], first_base[1] + 2])
        #             front.append([second_base[0], first_base[1] + 2])
        #             new_fronts.append(front)
        #             new_starts.append(start)
        #             new_ends.append(end)
        #         elif (second_base[1] - first_base[1]) > 0 and (second_base[1] - first_base[1]) % 2 == 0: #rw,r
        #             valid.append(i)
        #             extra_column = second_base[1] + 3 - len(shape[0])
        #             for j in range(len(shape)):
        #                 shape[j] = shape[j] + [0] * extra_column
        #             shape[first_base[0]][second_base[1] + 1: second_base[1] + 3] = [1, 1]
        #             shape[first_base[0] + 1][second_base[1] + 1: second_base[1] + 3] = [1, 1]
        #             shape[first_base[0] + 2][second_base[1] + 1: second_base[1] + 3] = [1, 1]
        #             for j in range(first_base[1] + 1, second_base[1] + 1):
        #                 shape[first_base[0]][j] = 2
        #             shape, space = fill_shape(shape)
        #             new_shapes.append(shape)
        #             new_Spaces.append(space)
        #             front.pop(max(locs))
        #             front.pop(min(locs))
        #             front.append([first_base[0], second_base[1] + 2])
        #             front.append([second_base[0], second_base[1] + 2])
        #             new_fronts.append(front)
        #             new_starts.append(start)
        #             new_ends.append(end)
        #     elif second_base[0] - first_base[0] > 2:
        #         if (first_base[1] - second_base[1]) == 1 and (second_base[0] - first_base[0]) % 2 == 1: #vertical w
        #             valid.append(i)
        #             extra_column = first_base[1] + 2 - len(shape[0])
        #             for j in range(len(shape)):
        #                 shape[j] = shape[j] + [0] * extra_column
        #             shape[first_base[0] + 1][first_base[1]: first_base[1] + 2] = [1, 1]
        #             shape[first_base[0] + 2][first_base[1]: first_base[1] + 2] = [1, 1]
        #             shape[first_base[0] + 3][first_base[1]: first_base[1] + 2] = [1, 1]
        #             if shape[second_base[0] - 1][second_base[1] - 1] == 0:
        #                 for j in range(first_base[0] + 3, second_base[0]):
        #                     shape[j][second_base[1]] = 2
        #             else:
        #                 for j in range(first_base[0] + 4, second_base[0] + 1):
        #                     shape[j][second_base[1] + 1] = 2
        #             shape, space = fill_shape(shape)
        #             new_shapes.append(shape)
        #             new_Spaces.append(space)
        #             front.pop(max(locs))
        #             front.pop(min(locs))
        #             front.append([first_base[0] + 1, first_base[1] + 1])
        #             front.append([first_base[0] + 3, first_base[1] + 1])
        #             new_fronts.append(front)
        #             new_starts.append(start)
        #             new_ends.append(end)
        #         elif (second_base[1] - first_base[1]) == 1 and (second_base[0] - first_base[0]) % 2 == 1: #vertical w
        #             valid.append(i)
        #             extra_column = second_base[1] + 2 - len(shape[0])
        #             for j in range(len(shape)):
        #                 shape[j] = shape[j] + [0] * extra_column
        #             shape[second_base[0] - 1][second_base[1]: second_base[1] + 2] = [1, 1]
        #             shape[second_base[0] - 2][second_base[1]: second_base[1] + 2] = [1, 1]
        #             shape[second_base[0] - 3][second_base[1]: second_base[1] + 2] = [1, 1]
        #             if shape[first_base[0] + 1][first_base[1] - 1] == 0:
        #                 for j in range(first_base[0] + 1, second_base[0] - 2):
        #                     shape[j][first_base[1]] = 2
        #             else:
        #                 for j in range(first_base[0], second_base[0] - 3):
        #                     shape[j][first_base[1] + 1] = 2
        #             shape, space = fill_shape(shape)
        #             new_shapes.append(shape)
        #             new_Spaces.append(space)
        #             front.pop(max(locs))
        #             front.pop(min(locs))
        #             front.append([second_base[0] - 3, second_base[1] + 1])
        #             front.append([second_base[0] - 1, second_base[1] + 1])
        #             new_fronts.append(front)
        #             new_starts.append(start)
        #             new_ends.append(end)
        #         elif (first_base[1] - second_base[1]) > 1:
        #             valid.append(i)
        #             extra_column = first_base[1] + 2 - len(shape[0])
        #             for j in range(len(shape)):
        #                 shape[j] = shape[j] + [0] * extra_column
        #             shape[first_base[0] + 1][first_base[1]: first_base[1] + 2] = [1, 1]
        #             shape[first_base[0] + 2][first_base[1]: first_base[1] + 2] = [1, 1]
        #             shape[first_base[0] + 3][first_base[1]: first_base[1] + 2] = [1, 1]
        #             new_shape, new_front, _, _, _ = place_W(shape, second_base, rows, len(shape), front, [],
        #                                                                 [], [], [first_base[0] + 3, first_base[1]], 1000, wire_target,
        #                                                                 [], 0)
        #             if new_shape != []:
        #                 shape = new_shape[0]
        #                 front = new_front[0]
        #                 shape, space = fill_shape(shape)
        #                 new_shapes.append(shape)
        #                 new_Spaces.append(space)
        #                 front.pop(max(locs))
        #                 front.pop(min(locs))
        #                 front.append([first_base[0] + 1, first_base[1] + 1])
        #                 front.append([first_base[0] + 3, first_base[1] + 1])
        #                 new_fronts.append(front)
        #                 new_starts.append(start)
        #                 new_ends.append(end)
        #         elif (second_base[1] - first_base[1]) > 1:
        #             valid.append(i)
        #             extra_column = second_base[1] + 2 - len(shape[0])
        #             for j in range(len(shape)):
        #                 shape[j] = shape[j] + [0] * extra_column
        #             shape[second_base[0] - 1][second_base[1]: second_base[1] + 2] = [1, 1]
        #             shape[second_base[0] - 2][second_base[1]: second_base[1] + 2] = [1, 1]
        #             shape[second_base[0] - 3][second_base[1]: second_base[1] + 2] = [1, 1]
        #             new_shape, new_front, _, _, _ = place_W(shape, first_base, rows, len(shape), front, [],
        #                                                                 [], [], [second_base[0] - 3, second_base[1]], 1000, wire_target,
        #                                                                 [], 0)
        #             if new_shape != []:
        #                 shape = new_shape[0]
        #                 front = new_front[0]
        #                 shape, space = fill_shape(shape)
        #                 new_shapes.append(shape)
        #                 new_Spaces.append(space)
        #                 front.pop(max(locs))
        #                 front.pop(min(locs))
        #                 front.append([second_base[0] - 3, second_base[1] + 1])
        #                 front.append([second_base[0] - 1, second_base[1] + 1])
        #                 new_fronts.append(front)
        #                 new_starts.append(start)
        #                 new_ends.append(end)
    return new_shapes, new_fronts, new_Spaces, valid, new_starts, new_ends

def fill_A_P(shapes, fronts, wire_targets, locs, same_qubit, starts, ends):
    valid = []  # valid shpae after fill A
    new_shapes = []
    new_Spaces = []
    new_preds = []
    new_fronts = []
    new_starts= []
    new_ends = []
    for i in range(len(shapes)):
        shape = shapes[i]
        front = fronts[i]
        pred = wire_targets[i]
        start = starts[i]
        end = ends[i]
        first_base = pred[locs[0]]
        second_base = pred[locs[1]]
        if first_base[0] > second_base[0]:
            temp = first_base
            first_base = second_base
            second_base = temp
        if first_base[0] + 2 == second_base[0] and first_base[1] == second_base[1]:  # ll
            if shapes[i][first_base[0] + 1][first_base[1]] == 0 or same_qubit:  # constraints for rr
                valid.append(i)
                if first_base[1] == 0:
                    extra_column = 1
                else:
                    extra_column = 0
                for j in range(len(shape)):
                    shape[j] = [0] * extra_column + shape[j]
                if extra_column == 0:
                    shape[first_base[0]][first_base[1] - 1] = 1
                    shape[first_base[0] + 1][first_base[1] - 1] = 1
                    shape[first_base[0] + 2][first_base[1] - 1] = 1
                else:
                    for element in pred:
                        element[1] = element[1] + extra_column
                    for element in front:
                        element[1] = element[1] + extra_column
                    for element in start:
                        element[1] = element[1] + extra_column
                    for element in end:
                        element[1] = element[1] + extra_column
                    shape[first_base[0]][first_base[1]] = 1
                    shape[first_base[0] + 1][first_base[1]] = 1
                    shape[first_base[0] + 2][first_base[1]] = 1
                    first_base[1] = first_base[1] + extra_column
                    second_base[1] = second_base[1] + extra_column
                pred.pop(max(locs))
                pred.pop(min(locs))
                pred.append([first_base[0], first_base[1] - 1])
                pred.append([second_base[0], second_base[1] - 1])
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                new_fronts.append(front)
                new_preds.append(pred)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 3 == second_base[0] and first_base[1] - 1 == second_base[1]:  # lu
            if shapes[i][first_base[0] + 1][first_base[1]] == 0:  # constraints for ru
                valid.append(i)
                shape[first_base[0]][first_base[1] - 1] = 1
                shape[first_base[0] + 1][first_base[1] - 1] = 1
                shape[first_base[0] + 2][first_base[1] - 1] = 1
                pred.pop(max(locs))
                pred.pop(min(locs))
                pred.append([first_base[0], first_base[1] - 1])
                pred.append([second_base[0] - 1, second_base[1]])
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                new_preds.append(pred)
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 3 == second_base[0] and first_base[1] + 1 == second_base[1]:  # dl
            if shapes[i][first_base[0] + 2][first_base[1] + 1] == 0:  # constraints for ru
                valid.append(i)
                shape[first_base[0] + 1][first_base[1]] = 1
                shape[first_base[0] + 2][first_base[1]] = 1
                shape[first_base[0] + 3][first_base[1]] = 1
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                pred.pop(max(locs))
                pred.pop(min(locs))
                pred.append([first_base[0] + 1, first_base[1]])
                pred.append([second_base[0], second_base[1] - 1])
                new_fronts.append(front)
                new_preds.append(pred)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 4 == second_base[0] and first_base[1] == second_base[1]:  # du
            if shapes[i][first_base[0] + 2][first_base[1] - 1] == 0:  # constraints for ru
                valid.append(i)
                shape[first_base[0] + 1][first_base[1]] = 1
                shape[first_base[0] + 2][first_base[1]] = 1
                shape[first_base[0] + 3][first_base[1]:] = 1
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                pred.pop(max(locs))
                pred.pop(min(locs))
                pred.append([first_base[0] + 1, first_base[1]])
                pred.append([second_base[0] - 1, second_base[1]])
                pred[locs[0]][0] = pred[locs[0]][0] + 1
                pred[locs[1]][0] = pred[locs[1]][0] - 1
                new_fronts.append(front)
                new_preds.append(pred)
                new_starts.append(start)
                new_ends.append(end)
    return new_shapes, new_fronts, new_Spaces, valid, new_preds, new_starts, new_ends

def fill_B_P(shapes, fronts, wire_targets, locs, same_qubit, starts, ends):
    valid = []  # valid shpae after fill B
    new_shapes = []
    new_Spaces = []
    new_preds = []
    new_fronts = []
    new_starts = []
    new_ends = []
    for i in range(len(shapes)):
        shape = shapes[i]
        front = fronts[i]
        pred = wire_targets[i]
        first_base = pred[locs[0]]
        second_base = pred[locs[1]]
        start = starts[i]
        end = ends[i]
        if first_base[0] > second_base[0]:
            temp = first_base
            first_base = second_base
            second_base = temp
        if first_base[0] + 2 == second_base[0] and first_base[1] == second_base[1]:  # ll
            if shapes[i][first_base[0] + 1][first_base[1]] == 0 or same_qubit:  # constraints for rr
                valid.append(i)
                if first_base[1] == 0:
                    extra_column = 2
                elif first_base[1] == 1:
                    extra_column = 1
                else:
                    extra_column = 0
                for j in range(len(shape)):
                    shape[j] = [0] * extra_column + shape[j]
                if extra_column == 0:
                    shape[first_base[0]][first_base[1] - 2: first_base[1]] = [1,1]
                    shape[first_base[0] + 1][first_base[1] - 2: first_base[1]] = [1,1]
                    shape[first_base[0] + 2][first_base[1] - 2: first_base[1]] = [1,1]
                else:
                    for element in pred:
                        element[1] = element[1] + extra_column
                    for element in front:
                        element[1] = element[1] + extra_column
                    for element in start:
                        element[1] = element[1] + extra_column
                    for element in end:
                        element[1] = element[1] + extra_column
                    shape[first_base[0]][0:2] = [1,1]
                    shape[first_base[0] + 1][0:2] = [1,1]
                    shape[first_base[0] + 2][0:2] = [1,1]
                    first_base[1] = first_base[1] + extra_column
                    second_base[1] = second_base[1] + extra_column
                pred.pop(max(locs))
                pred.pop(min(locs))
                pred.append([first_base[0], first_base[1] - 2])
                pred.append([second_base[0], second_base[1] - 2])
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                new_fronts.append(front)
                new_preds.append(pred)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 3 == second_base[0] and first_base[1] - 1 == second_base[1]:  # lu
            if shapes[i][first_base[0] + 1][first_base[1]] == 0:  # constraints for ru
                valid.append(i)
                if second_base[1] == 0:
                    extra_column = 1
                else:
                    extra_column = 0
                for j in range(len(shape)):
                    shape[j] = [0] * extra_column + shape[j]
                if extra_column == 0:
                    shape[first_base[0]][first_base[1] - 2: first_base[1]] = [1,1]
                    shape[first_base[0] + 1][first_base[1] - 2: first_base[1]] = [1,1]
                    shape[first_base[0] + 2][first_base[1] - 2: first_base[1]] = [1,1]
                else:
                    for element in pred:
                        element[1] = element[1] + extra_column
                    for element in front:
                        element[1] = element[1] + extra_column
                    for element in start:
                        element[1] = element[1] + extra_column
                    for element in end:
                        element[1] = element[1] + extra_column
                    shape[first_base[0]][0:2] = [1,1]
                    shape[first_base[0] + 1][0:2] = [1,1]
                    shape[first_base[0] + 2][0:2] = [1,1]
                    first_base[1] = first_base[1] + extra_column
                    second_base[1] = second_base[1] + extra_column
                pred.pop(max(locs))
                pred.pop(min(locs))
                pred.append([first_base[0], first_base[1] - 2])
                pred.append([second_base[0] - 1, second_base[1] - 1])
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                new_preds.append(pred)
                new_fronts.append(front)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 3 == second_base[0] and first_base[1] + 1 == second_base[1]:  # dl
            if shapes[i][first_base[0] + 2][first_base[1] + 1] == 0:  # constraints for ru
                valid.append(i)
                if first_base[1] == 0:
                    extra_column = 1
                else:
                    extra_column = 0
                for j in range(len(shape)):
                    shape[j] = [0] * extra_column + shape[j]
                if extra_column == 0:
                    shape[first_base[0] + 1][second_base[1] - 2: second_base[1]] = [1,1]
                    shape[first_base[0] + 2][second_base[1] - 2: second_base[1]] = [1,1]
                    shape[first_base[0] + 3][second_base[1] - 2: second_base[1]] = [1,1]
                else:
                    for element in pred:
                        element[1] = element[1] + extra_column
                    for element in front:
                        element[1] = element[1] + extra_column
                    for element in start:
                        element[1] = element[1] + extra_column
                    for element in end:
                        element[1] = element[1] + extra_column
                    shape[first_base[0] + 1][0:2] = [1,1]
                    shape[first_base[0] + 2][0:2] = [1,1]
                    shape[first_base[0] + 3][0:2] = [1,1]
                    first_base[1] = first_base[1] + extra_column
                    second_base[1] = second_base[1] + extra_column
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                pred.pop(max(locs))
                pred.pop(min(locs))
                pred.append([first_base[0] + 1, first_base[1] - 1])
                pred.append([second_base[0], second_base[1] - 2])
                new_fronts.append(front)
                new_preds.append(pred)
                new_starts.append(start)
                new_ends.append(end)
        elif first_base[0] + 4 == second_base[0] and first_base[1] == second_base[1]:  # du
            if shapes[i][first_base[0] + 2][first_base[1] - 1] == 0:  # constraints for ru
                valid.append(i)
                if first_base[1] == 0:
                    extra_column = 1
                else:
                    extra_column = 0
                for j in range(len(shape)):
                    shape[j] = [0] * extra_column + shape[j]
                if extra_column == 0:
                    shape[first_base[0] + 1][second_base[1] - 1: second_base[1] + 1] = [1,1]
                    shape[first_base[0] + 2][second_base[1] - 1: second_base[1] + 1] = [1,1]
                    shape[first_base[0] + 3][second_base[1] - 1: second_base[1] + 1] = [1,1]
                else:
                    for element in pred:
                        element[1] = element[1] + extra_column
                    for element in front:
                        element[1] = element[1] + extra_column
                    for element in start:
                        element[1] = element[1] + extra_column
                    for element in end:
                        element[1] = element[1] + extra_column
                    shape[first_base[0] + 1][0:2] = [1,1]
                    shape[first_base[0] + 2][0:2] = [1,1]
                    shape[first_base[0] + 3][0:2] = [1,1]
                    first_base[1] = first_base[1] + extra_column
                    second_base[1] = second_base[1] + extra_column
                shape, space = fill_shape(shape)
                new_shapes.append(shape)
                new_Spaces.append(space)
                pred.pop(max(locs))
                pred.pop(min(locs))
                pred.append([first_base[0] + 1, first_base[1] - 1])
                pred.append([second_base[0] - 1, second_base[1] - 1])
                pred[locs[0]][0] = pred[locs[0]][0] + 1
                pred[locs[1]][0] = pred[locs[1]][0] - 1
                new_fronts.append(front)
                new_preds.append(pred)
                new_starts.append(start)
                new_ends.append(end)
    return new_shapes, new_fronts, new_Spaces, valid, new_preds, new_starts, new_ends