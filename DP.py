import copy
import networkx as nx
from matplotlib import pyplot as plt
from placement import *
from To_graph import *

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

    table, shapes, index = place_core(graph, nodes, W_len, rows, qubits, A_loc, B_loc, C_loc)
    # middle_shapes = shapes[-1]
    # final_shapes = place_leaves(table, shapes, first, last, rows, special)
    # show_min(middle_shapes, final_shapes)
    # save_shapes(shapes)
    # combination(final_shapes, new_map)
    # combination2(table[-1], middle_shapes, first, last, rows)
    # save_shapes(shapes)
    print('g')

def place_core(graph, nodes, W_len, rows, qubits, A_loc, B_loc, C_loc):
    # n_nodes = np.array(nodes)
    # np.savetxt("example/iqp20_nodes.csv", n_nodes, fmt = '%s',delimiter=",")
    order = list(nx.topological_sort(graph))
    order, W_len, graph, nodes = update_all_wires(order, W_len, graph, nodes)#switch wire to the right
    independet_node = find_independent(graph, order)
    table = [[]]
    shape = [[]]
    valid = [[]]  # for chosen patterns
    two_wire = []  # record the node with two wire predecessors
    qubit_record = []
    placed = []
    nodes_left = copy.deepcopy(order)
    #place each independent node until two-qubit pattern
    inde_table = []
    inde_shape = []
    for i in range(len(independet_node)):
        inde_table.append([])
        inde_shape.append([])
        current = independet_node.pop(0)
        nodes_left.remove(current)
        qubit_record = get_qubit_record(current, nodes, qubit_record)
        inde_table[0], inde_shape[0], new_placed = place_independent(current, graph, qubit_record, rows, qubits, nodes, nodes_left, A_loc, B_loc, C_loc)
    print('g')

def place_independent(current, graph, qubit_record, rows, qubits, nodes, nodes_left, A_loc, B_loc, C_loc):
    placed = []
    placed.append(current)
    gate, _ = current.split('.')
    succ = list(graph.successors(current))
    temp_shape = []
    table = [[]]
    shape = [[]]
    if gate == 'A':
        dep = 1
        temp_shape.append([1])
        temp_shape.append([1])
        temp_shape.append([1])
        if len(succ) == 2:
            table[0].append({'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[0, 0], [2, 0]], 'successor':[succ[0], succ[1]], 'targets':[], 'starts':[[0, 0], [2, 0]], 'ends':[]})
        elif len(succ) == 1:
            end = detec_end(current, succ[0], nodes)
            if end == 'u':
                table[0].append({'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[2, 0]], 'successor':[succ[0]], 'targets':[], 'starts':[[0, 0], [2, 0]], 'ends':[[0, 0]]})
            else:
                table[0].append({'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[0, 0]], 'successor':[succ[0]], 'targets':[], 'starts':[[0, 0], [2, 0]], 'ends':[[2, 0]]})
    else:
        dep = 2
        temp_shape.append([1,1])
        temp_shape.append([1,1])
        temp_shape.append([1,1])
        if len(succ) == 2:
            table[0].append({'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[0, 1], [2, 1]], 'successor':[succ[0], succ[1]], 'targets':[], 'starts':[[0, 0], [2, 0]], 'ends':[]})
        elif len(succ) == 1:
            end = detec_end(current, succ[0], nodes)
            if end == 'u':
                table[0].append(
                    {'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[2, 1]],
                     'successor': [succ[0]], 'targets': [], 'starts': [[0, 0], [2, 0]], 'ends': [[0,1]]})
            else:
                table[0].append(
                    {'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[0, 1]],
                     'successor': [succ[0]], 'targets': [], 'starts': [[0, 0], [2, 0]], 'ends': [[2,1]]})
    shape[0].append(temp_shape)
    till_end = 1
    for node in succ:
        preds = list(graph.predecessors(node))
        for pred in preds:
            if pred not in placed:
                till_end = 0
    while till_end:
        next = choose_next(nodes_left, placed, graph, nodes, A_loc, B_loc, C_loc)  # chose the next
        c_qubit = find_qubits(nodes, placed, next)
        new_sucessors = list(graph.successors(next))
        loc = check_loc(nodes, placed, next, graph)

    return table, shape, placed

def choose_next(nodes_left, placed, graph, nodes, A_loc, B_loc, C_loc, two_wire):
    next = []
    parent_index = [] #the parent of the chosen
    parent_row = [] #record the row number of the qubit
    found_wire = 0 #choose the wire
    found_C = 0 #choose the C
    only_one = [] #the node that only one preds have been placed
    succ_placed = [] #the node that succs have been placed
    for node in nodes_left: #found all the nodes that predecessors have been resolved
        succs = list(graph.successors(node))
        before = list(graph.predecessors(node))
        p_index = 100000
        wires = 0
        gate, _ = node.split('.')
        solved = 1
        if before == []:
            solved = 0
        pred_placed = []
        for pred in before:
            gate1, _ = pred.split('.')
            if pred in placed:
                index = placed.index(pred)
                pred_placed.append(pred)
            elif pred not in placed and gate1 != 'W': #if one of the predecessor is wire
                solved = 0
            elif gate1 == 'W':
                wires = wires + 1
            if pred in placed and p_index > index:
                p_index = index
        if len(before) == 2 and pred_placed != [] and (before[0] in two_wire or before[1] in two_wire): #for two wire
            solved = 1
        if len(pred_placed) == 1 and len(before) == 2:
            only_one.append(node)
            solved = 1
        elif len(pred_placed) == 0 and gate != 'W':#if none of the predecessors have been placed, look for succesor
            for succ in succs:
                if succ in placed:
                    solved = 1
                    succ_placed.append(node)
        if wires == len(before) and before != []: #both predecessors are wires and one of the sucessors is placed
            solved = 0
            if node not in two_wire:
                two_wire.append(node)
            elif len(succs) == 1:
                if wires == len(before) and succs[0] in placed:
                    found_wire = 1
                    next_node = node
                    break
            elif len(succs) == 2:
                if wires == len(before) and (succs[0] in placed or succs[1] in placed):
                    found_wire = 1
                    next_node = node
                    break
        elif solved:
            gate1, num = node.split('.')
            pred = list(graph.predecessors(node))
            if pred != []:
                gate2, _ = pred[0].split('.')
            if succs != []:
                gate3, _ = succs[0].split('.')
            if gate1 == 'B' or gate1 == 'B1':
                loc = B_loc[int(num)]
            elif gate1 == 'A':
                loc = A_loc[int(num)]
            elif gate1 == 'C':
                loc = C_loc[int(num)]
            if gate1 == 'W':
                succ = list(graph.successors(node)) #choose the wire whose succesor has been placed
                if succ[0] in placed:
                    found_wire = 1
                    next_node = node
                    # break
            elif gate1 == 'C' and ((pred[0] in placed and gate2 == 'C') or (succs[0] in placed and gate3 == 'C')): #choose C if the previous is also C
                found_C = 1
                next_node = node
                break
            else:
                next.append(node)
                parent_index.append(loc)
                for i in range(len(nodes)): #record the row
                    if node in nodes[i]:
                        parent_row.append(i)
                        break
    if found_wire != 1 and found_C != 1:
        if succ_placed != []:
            next_node = find_higher_node(parent_index, succ_placed, next, parent_row)
        elif parent_index != []:
            next_node = available_node(parent_index, next, parent_row)
        elif only_one != []: # cannot find node with both predecessors resolved or wires or
            next_node = only_one[-1]
    return next_node

def find_higher_node(parent_index, succ_placed, next, parent_row):
    if len(succ_placed) == 1:
        return succ_placed[0]
    else:
        indexes = []
        for node in succ_placed:
            indexes.append(next.index(node))
        new_parent_index = []
        new_parent_row = []
        for i in indexes:
            new_parent_index.append(parent_index[i])
            new_parent_row.append(parent_row)
        max_index = max(new_parent_index)
        temp_parent = []
        max_indexes = []
        for i in range(len(new_parent_index)):
            if new_parent_index[i] == max_index:
                max_indexes.append(i)
        for i in max_indexes:
            temp_parent.append(new_parent_row[i])
        return succ_placed[max_indexes[temp_parent.index(min(temp_parent))]]

def available_node(parent_index, next, parent_row):
    two_qubit = []
    two_qubit_index = []
    two_qubit_row= []
    for i in range(len(next)):
        gate1, _ = next[i].split('.')
        if gate1 == 'A' or gate1 == 'B' or gate1 == 'B1':
            two_qubit.append(next[i])
            two_qubit_index.append(parent_index[i])
            two_qubit_row.append(parent_row[i])
    min_index = min(parent_index)
    temp_parent = []
    indexes = []
    for i in range(len(parent_index)):
        if parent_index[i] == min_index:
            indexes.append(i)
    for i in indexes:
        temp_parent.append(parent_row[i])
    return next[indexes[temp_parent.index(min(temp_parent))]]