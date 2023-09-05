import copy
import networkx as nx
from matplotlib import pyplot as plt
from placement import *

def DP(ori_map, qubits, rows):
    new_map = []
    for row in ori_map:
        new_map.append([])
        for item in row:
            if item != 'Z' and item != 'X':
                new_map[-1].append(1)
            elif item == 'X':
                new_map[-1].append(2)
            else:
                new_map[-1].append(0)
    graph, nodes, W_len, first, last, A_loc, B_loc, C_loc = gen_index(new_map)

    # table, shapes, index = place_core(graph, nodes, W_len, rows, qubits, A_loc, B_loc, C_loc, force_right, restricted, special_greedy)
    # middle_shapes = shapes[-1]
    # final_shapes = place_leaves(table, shapes, first, last, rows, special)
    # show_min(middle_shapes, final_shapes)
    # save_shapes(shapes)
    # combination(final_shapes, new_map)
    # combination2(table[-1], middle_shapes, first, last, rows)
    # save_shapes(shapes)
    print('g')

def gen_index(map):
    cut = []
    s_row = []
    for i in range(1, len(map)-1, 2):
        rowcut = []
        j = 0
        while j < len(map[0]):
            if map[i][j] != 0:
                rowcut.append(j)
                # if j + 1 < len(map[0]):
                #     if map[i][j+1] == 1:
                #         j = j + 1
            j = j + 1
        cut.append(rowcut)

    for i in range(0, len(cut) - 1):
        temp_row = cut[i] + cut[i + 1]
        temp_row.sort()
        s_row.append(copy.deepcopy(temp_row))
    s_row.insert(0, cut[0])
    s_row.append(cut[-1]) #the two qubit gate location for each row
    first = []
    last = []
    qubit = 0
    for i in range(0, len(map), 2):
        for j in range(len(map[i])):
            if map[i][j] != 0:
                front = s_row[qubit][0] - j
                break
        for j in reversed(range(len(map[i]))):
            if map[i][j] != 0:
                back = j - s_row[qubit][-1]
                break
        qubit = qubit + 1
        first.append(front) #length for the patterns in the front
        last.append(back) #length for the patterns in the back
    nodes, W_len, A_loc, B_loc, C_loc = gen_DAG(map,s_row)
    graph = nx.DiGraph()
    for node in nodes:
        for i in range(len(node) - 1):
            graph.add_edge(node[i], node[i+1])
    #order = list(nx.topological_sort(graph))
    #next = list(graph.successors('A.0'))
    return graph, nodes, W_len, first, last, A_loc, B_loc, C_loc

def gen_DAG(map, s_row):
    indexes = []
    for index in s_row:
        indexes = indexes + index
    indexes = [*set(indexes)]
    indexes.sort()
    nodes = [] #graph nodes
    node_loc = []
    for i in range(len(s_row)):
        nodes.append([])
        node_loc.append([])
    A = 0
    B = 0
    C = 0
    W = 0
    A_loc = []
    B_loc = []
    C_loc = [] #none wire single row length
    W_loc = []
    W_len = [] #wire single row length
    index = 0
    while index < len(indexes):
        for i in range(1, len(map)-1, 2):
            next_0 = check_next_0(map, i, indexes[index])
            if map[i][indexes[index]] != 0:
                if map[i][indexes[index] + 1] != 0 and next_0 % 2 == 0 and ((i == 1 and map[i+2][indexes[index]] == 0) or
                (i == len(map)-2 and map[i-2][indexes[index]] == 0)
                or (1 < i < len(map)-2 and map[i+2][indexes[index]] == 0 and map[i-2][indexes[index]] == 0)):
                    node = 'B.' + str(B)
                    loc = int((i-1)/2)
                    nodes[loc].append(node)
                    nodes[loc + 1].append(node)
                    node_loc[loc].append(indexes[index] + 1)
                    node_loc[loc + 1].append(indexes[index] + 1)
                    B_loc.append(indexes[index])
                    B = B + 1
                elif map[i][indexes[index] - 1] == 0 and map[i][indexes[index] + 1] == 0:
                    node = 'A.' + str(A)
                    loc = int((i - 1) / 2)
                    nodes[loc].append(node)
                    nodes[loc + 1].append(node)
                    node_loc[loc].append(indexes[index])
                    node_loc[loc + 1].append(indexes[index])
                    A_loc.append(indexes[index])
                    A =  A + 1
        for i in range(1, len(map)-1, 2):
            next_0 = check_next_0(map, i, indexes[index])
            if map[i][indexes[index]] != 0:
                if map[i][indexes[index] + 1] != 0 and next_0 % 2 == 0 and ((i == 1 and map[i+2][indexes[index]] != 0) or
                (i == len(map)-2 and map[i-2][indexes[index]] != 0) or (1 < i < len(map)-2 and (map[i+2][indexes[index]] != 0 or map[i-2][indexes[index]] != 0))):
                    node = 'B1.' + str(B)
                    loc = int((i - 1) / 2)
                    nodes[loc].append(node)
                    nodes[loc + 1].append(node)
                    node_loc[loc].append(indexes[index] + 1)
                    node_loc[loc + 1].append(indexes[index] + 1)
                    B_loc.append(indexes[index])
                    B = B + 1
        index = index + 1
    for i in range(len(s_row)):
        add = 1
        for j in range(len(s_row[i]) - 1):
            if s_row[i][j + 1] - s_row[i][j] > 1:
                if map[i * 2][s_row[i][j] + 1] == 2 and s_row[i][j + 1] - s_row[i][j] > 3:
                    node = 'W.' + str(W)
                    W = W + 1
                    loc = node_loc[i].index(s_row[i][j])
                    nodes[i].insert(loc + add, node)
                    add = add + 1
                    W_len.append(s_row[i][j + 1] - s_row[i][j] - 1)
                #elif map[i * 2][s_row[i][j] + 1] != 2:
                else:
                    for k in range(s_row[i][j + 1] - s_row[i][j] - 1):
                        C_loc.append(k + s_row[i][j] + 1)
                        node = 'C.' + str(C)
                        C = C + 1
                        loc = node_loc[i].index(s_row[i][j])
                        nodes[i].insert(loc + add, node)
                        add = add + 1
                    #C_len.append(s_row[i][j + 1] -  s_row[i][j] - 1)
    return nodes, W_len, A_loc, B_loc, C_loc

def check_next_0(map, i, start):
    index = copy.deepcopy(start)
    while(map[i][index] != 0):
        index = index + 1
    return index - start