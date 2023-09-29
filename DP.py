import copy
import networkx as nx
from matplotlib import pyplot as plt
from placement import *
from To_graph import *
from fill_map import *
from leaves import *
from last_step import *

keep = 3
long = 4
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

    table, shapes = place_core(graph, nodes, W_len, rows, qubits, A_loc, B_loc, C_loc)
    print("finish placing core")
    print("number of core: ", len(shapes))
    middle_shapes = shapes[-1]
    final_shapes = place_leaves(table, shapes, first, last, rows)
    print("number of final shapes: ", len(shapes))
    combination(final_shapes, new_map)
    print('g')

def place_core(graph, nodes, W_len, rows, qubits, A_loc, B_loc, C_loc):
    # n_nodes = np.array(nodes)
    # np.savetxt("example/iqp20_nodes.csv", n_nodes, fmt = '%s',delimiter=",")
    order = list(nx.topological_sort(graph))
    order, W_len, graph, nodes = update_all_wires(order, W_len, graph, nodes)#switch wire to the right
    independet_node = find_independent(graph, order)
    onle_one_pre = [[] for _ in range(len(independet_node) + 1)] #the first one is empty
    table = [[]]
    shape = [[]]
    valid = [[]]  # for chosen patterns
    two_wire = []  # record the node with two wire predecessors
    placed = [] #nodes have been placed
    nodes_left = copy.deepcopy(order)
    #place each independent node until two-qubit pattern
    inde_table = [[] for _ in range(len(independet_node))]
    inde_shape = [[] for _ in range(len(independet_node))]
    inde_placed = [[] for _ in range(len(independet_node))]
    inde_qubit_record = [[] for _ in range(len(independet_node))]
    current_independent_node = copy.deepcopy(independet_node)
    current = current_independent_node.pop(0)
    nodes_left.remove(current)
    inde_qubit_record[0] = get_qubit_record(current, nodes, [])
    inde_table[0], inde_shape[0], inde_placed[0], onle_one_pre[1], nodes_left, inde_qubit_record[0] = \
        place_independent(current, graph, inde_qubit_record[0], rows, qubits, nodes, nodes_left, A_loc, B_loc, C_loc, W_len,
                        current_independent_node, placed)
    if len(independet_node) == 1:
        return inde_table[-1], inde_shape[-1]
    i = 0
    for i in range(1, len(independet_node)):
        current = current_independent_node.pop(0)
        new_independent_node = copy.deepcopy(independet_node)
        new_independent_node.remove(current)
        nodes_left.remove(current)
        inde_qubit_record[i] = get_qubit_record(current, nodes, [])
        inde_table[i], inde_shape[i], new_placed, onle_one_pre[i + 1], nodes_left, inde_qubit_record[i] = \
            place_independent(current, graph, inde_qubit_record[i], rows, qubits, nodes, nodes_left, A_loc, B_loc, C_loc, W_len,
                              new_independent_node, [])
        inde_placed[i] = new_placed
    rest_independent_node = copy.deepcopy(independet_node)
    while nodes_left!= []:
        combination = find_combine(onle_one_pre)
        inde_table.append([])
        inde_shape.append([])
        onle_one_pre.append([])
        inde_placed.append([])
        inde_qubit_record.append([])
        if combination[0] - 1 < len(independet_node) and independet_node[combination[0] - 1] in rest_independent_node:
            rest_independent_node.remove(independet_node[combination[0] - 1])
        if combination[1] - 1 < len(independet_node) and independet_node[combination[1] - 1] in rest_independent_node:
            rest_independent_node.remove(independet_node[combination[1] - 1])
        placed = inde_placed[combination[0] - 1] + inde_placed[combination[1] - 1]
        placed.append(onle_one_pre[combination[0]][0])
        nodes_left.remove(onle_one_pre[combination[0]][0])
        temp_table, temp_shape, placed, nodes_left = combine(onle_one_pre[combination[0]][0], inde_table[combination[0] - 1], inde_shape[combination[0] - 1], inde_table[combination[1] - 1],
                                         inde_shape[combination[1] - 1], rows, nodes, inde_placed[combination[0] - 1], inde_placed[combination[1] - 1], graph, qubits, placed, nodes_left)
        onle_one_pre[combination[0]] = []
        onle_one_pre[combination[1]] = []
        i = i + 1
        inde_qubit_record[i] = inde_qubit_record[combination[0] - 1] + inde_qubit_record[combination[1] - 1]
        inde_table[i], inde_shape[i], inde_placed[i], onle_one_pre[i + 1], nodes_left, inde_qubit_record[i] = \
            place_combine([temp_table], [temp_shape], inde_qubit_record[i], graph, rows, qubits, nodes, nodes_left, A_loc, B_loc, C_loc, W_len,
                              rest_independent_node, placed)
    return inde_table[-1], inde_shape[-1]


def place_independent(current, graph, qubit_record, rows, qubits, nodes, nodes_left, A_loc, B_loc, C_loc, W_len, independent_node, placed):
    index = 0
    onle_one_pre = [] #record node with only one predecessor placed
    placed.append(current)
    gate, _ = current.split('.')
    succ = list(graph.successors(current))
    temp_shape = []
    table = [[]]
    shape = [[]]
    valid = [[]]
    two_wire = [] #for node both predecessors are wires
    if gate == 'A':
        dep = 1
        temp_shape.append([1])
        temp_shape.append([1])
        temp_shape.append([1])
        if len(succ) == 2:
            table[0].append({'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[0, 0], [2, 0]], 'successor':[succ[0], succ[1]], 'targets':[], 'preds':[], 'starts':[[0, 0], [2, 0]], 'ends':[]})
        elif len(succ) == 1:
            end = detec_end(current, succ[0], nodes)
            if end == 'u':
                table[0].append({'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[2, 0]], 'successor':[succ[0]], 'targets':[], 'preds':[], 'starts':[[0, 0], [2, 0]], 'ends':[[0, 0]]})
            else:
                table[0].append({'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[0, 0]], 'successor':[succ[0]], 'targets':[], 'preds':[], 'starts':[[0, 0], [2, 0]], 'ends':[[2, 0]]})
    else:
        dep = 2
        temp_shape.append([1,1])
        temp_shape.append([1,1])
        temp_shape.append([1,1])
        if len(succ) == 2:
            table[0].append({'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[0, 1], [2, 1]], 'successor':[succ[0], succ[1]], 'targets':[], 'preds':[], 'starts':[[0, 0], [2, 0]], 'ends':[]})
        elif len(succ) == 1:
            end = detec_end(current, succ[0], nodes)
            if end == 'u':
                table[0].append(
                    {'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[2, 1]],
                     'successor': [succ[0]], 'targets': [], 'preds':[], 'starts': [[0, 0], [2, 0]], 'ends': [[0,1]]})
            else:
                table[0].append(
                    {'New': current, 'P': 'NA', 'row': 3, 'S': 0, 'D': dep, 'Q': 2, 'front': [[0, 1]],
                     'successor': [succ[0]], 'targets': [], 'preds':[], 'starts': [[0, 0], [2, 0]], 'ends': [[2,1]]})
    shape[0].append(temp_shape)
    valid[0].append(0)
    next, onle_one_pre, match_next_node = choose_next(nodes_left, placed, graph, nodes, A_loc, B_loc, C_loc, two_wire, onle_one_pre, independent_node)
    if match_next_node:
        return table[-1], shape[-1], placed, onle_one_pre, nodes_left, qubit_record
    only_right = []  # record the C that only can go right (if previous two-qubit gate and later are on the same qubits)
    while next != "":
        c_qubit = find_qubits(nodes, placed, next)
        new_sucessors = list(graph.successors(next))
        loc = check_loc(nodes, placed, next, graph, two_wire)
        print(next)
        next_list = place_next(next, table, shape, valid, index, rows, new_sucessors, qubits, c_qubit, loc, graph, nodes,
                               W_len, placed, two_wire, only_right, qubit_record)  # place the next node
        qubit_record = get_qubit_record(next, nodes, qubit_record)
        index = index + 1
        for j in next_list:
            nodes_left.remove(j)
            placed.append(j)
        next, onle_one_pre, match_next_node = choose_next(nodes_left, placed, graph, nodes, A_loc, B_loc, C_loc, two_wire, onle_one_pre, independent_node)  # chose the next
        if match_next_node:
            return table[-1], shape[-1], placed, onle_one_pre, nodes_left, qubit_record
    return table[-1], shape[-1], placed, onle_one_pre, nodes_left, qubit_record

def place_combine(table, shape, qubit_record, graph, rows, qubits, nodes, nodes_left, A_loc, B_loc, C_loc, W_len,
                              independent_node, placed):
    index = 0
    onle_one_pre = []  # record node with only one predecessor placed
    valid = [[]]
    for i in range(len(shape)):
        valid[0].append(i)
    two_wire = []  # for node both predecessors are wires
    next, onle_one_pre, match_next_node = choose_next(nodes_left, placed, graph, nodes, A_loc, B_loc, C_loc, two_wire,
                                                      onle_one_pre, independent_node)
    if match_next_node:
        return table[-1], shape[-1], placed, onle_one_pre, nodes_left, qubit_record
    only_right = []  # record the C that only can go right (if previous two-qubit gate and later are on the same qubits)
    while next != "":
        c_qubit = find_qubits(nodes, placed, next)
        new_sucessors = list(graph.successors(next))
        loc = check_loc(nodes, placed, next, graph, two_wire)
        print(next)
        next_list = place_next(next, table, shape, valid, index, rows, new_sucessors, qubits, c_qubit, loc, graph, nodes,
                               W_len, placed, two_wire, only_right, qubit_record)  # place the next node
        qubit_record = get_qubit_record(next, nodes, qubit_record)
        index = index + 1
        for j in next_list:
            nodes_left.remove(j)
            placed.append(j)
        next, onle_one_pre, match_next_node = choose_next(nodes_left, placed, graph, nodes, A_loc, B_loc, C_loc, two_wire, onle_one_pre, independent_node)  # chose the next
        if match_next_node:
            return table[-1], shape[-1], placed, onle_one_pre, nodes_left, qubit_record
    return table[-1], shape[-1], placed, onle_one_pre, nodes_left, qubit_record

def choose_next(nodes_left, placed, graph, nodes, A_loc, B_loc, C_loc, two_wire, onle_one_pre, independent_node):
    next = []
    parent_index = [] #the parent of the chosen
    parent_row = [] #record the row number of the qubit
    found_wire = 0 #choose the wire
    found_C = 0 #choose the C
    only_one = [] #the node that only one preds have been placed
    succ_placed = [] #the node that succs have been placed
    next_node = ""
    match_next_node = 0 #record if one of the predecessors of next node have been placed
    for node in nodes_left: #found all the nodes that predecessors have been resolved
        # if node in last_only_one_pre:
        #     onle_one_pre.append(node)
        #     return next_node, onle_one_pre, 1
        succs = list(graph.successors(node))
        before = list(graph.predecessors(node))
        copy_before = copy.deepcopy(before)
        # p_index = 100000 #？？
        wires = 0
        gate, _ = node.split('.')
        solved = 1
        if before == []:
            solved = 0
        pred_placed = []
        for pred in before:
            gate1, _ = pred.split('.')
            if pred in placed:
                # index = placed.index(pred)
                pred_placed.append(pred)
                copy_before.remove(pred)
            elif pred not in placed and gate1 != 'W': #if one of the predecessor is wire
                solved = 0
            elif gate1 == 'W':
                wires = wires + 1
            # if pred in placed and p_index > index:
            #     p_index = index
        if len(before) == 2 and pred_placed != [] and (before[0] in two_wire or before[1] in two_wire): #for two wire
            solved = 1
        if len(pred_placed) == 1 and len(before) == 2: #check if another predecessors have been placed
            ancestor_placed = check_ancestor(copy_before[0], graph, placed, independent_node)
            if ancestor_placed:
                only_one.append(node)
                solved = 1
            else:
                onle_one_pre.append(node)
                match_next_node = 1
                return next_node, onle_one_pre, match_next_node
        # elif len(pred_placed) == 0 and gate != 'W':#if none of the predecessors have been placed, look for succesor
        #     for succ in succs:
        #         if succ in placed:
        #             solved = 1
        #             succ_placed.append(node)
        if wires == len(before) and before != []: #both predecessors are wires and one of the sucessors is placed
            if node not in two_wire:
                two_wire.append(node)
            elif len(succs) == 1: #both predecessors are wires and one sucessor is placed
                if wires == len(before) and succs[0] in placed:
                    found_wire = 1
                    next_node = node
                    break
            elif len(succs) == 2: #both predecessors are wires and one of sucessors is placed
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
    # print('g')
    if found_wire != 1 and found_C != 1:
        # if succ_placed != []:
        #     next_node = find_higher_node(parent_index, succ_placed, next, parent_row)
        if parent_index != []:
            next_node = available_node(parent_index, next, parent_row)
        elif only_one != []: # cannot find node with both predecessors resolved or wires or
            next_node = only_one[-1]
    return next_node, onle_one_pre, match_next_node

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

#(next, table, shape, valid, index, rows, new_sucessors, qubits, c_qubit, loc, graph, nodes, W_len, placed, two_wire, only_right, qubit_record)
def place_next(next, table, shape, valid, p_index, rows, new_sucessors, qubits, c_qubit, loc, graph, nodes, W_len, placed, two_wire, only_right, qubit_record):
    special_greedy = 0
    next_list = [next]
    c_gate, gate_index = next.split('.')
    parents = [] #record parents
    fronts = []#record the new fronts
    spaces = []#record the new spaces
    shapes = [] #record the new shapes
    wire_targets = [] #for the target of wires
    not_placed_preds = [] #for current unplaced predecessors
    placed_preds = []
    starts = []  # for recording the start points
    ends = []  # for recording the end points
    end = 0
    b_end = 0
    not_placed = False #check if there is wire for the previous
    n_preds = list(graph.predecessors(next))
    same_qubit = 0
    nextnext = 0
    for pred in n_preds:
        if pred not in placed:
            not_placed = True
            not_placed_preds.append(pred)
        else:
            p_gate, _ = pred.split('.')
            placed_preds.append(p_gate)
    if (c_gate == 'A' or c_gate == 'B' or c_gate == 'B1') and len(new_sucessors) == 1:
        end = detec_end(next, new_sucessors[0], nodes)
        if end == 0:
            nextnext = new_sucessors[0]
            same_qubit = 1
    if (c_gate == 'A' or c_gate == 'B' or c_gate == 'B1') and len(new_sucessors) == 2: #detect only right(all second C will be forward)
        p_gate1, _ = new_sucessors[0].split('.')
        p_gate2, _ = new_sucessors[1].split('.')
        if p_gate1 == 'C' or p_gate2 == 'C':
            only_right = detect_only_right(next, graph, only_right)
    if (c_gate == 'A' or c_gate == 'B' or c_gate == 'B1') and len(n_preds) == 1 and new_sucessors != []: #detect end point for backward
        b_end = detec_end_b(next, new_sucessors[0], nodes)
    parent = copy.deepcopy(table[p_index][0])
    successors = parent['successor']
    preds = parent['preds']
    new_qubit = 0 #track new qubit appear
    if c_qubit - parent['Q'] == 1:
        new_qubit = 1
    if not_placed_preds != n_preds:
        c_index = successors.index(next)  # remove the next node from the table
        successors.pop(c_index)
    prepre = 0
    if c_gate != 'W':
        for succ in new_sucessors:
            if succ in successors:
                nextnext = succ
            if succ not in placed:
                successors.append(succ)
                if same_qubit == 1:
                    successors.append(succ)
        for pred in n_preds:
            if pred in preds:
                prepre = pred
    # if c_gate != 'W' and nextnext == 0 and prepre == 0 and ((c_gate != 'C' and (placed_preds == [] or placed_preds[0] != 'C')) or restricted == 0):
    if c_gate != 'W' and nextnext == 0 and prepre == 0 and (c_gate != 'C'):
        parent_node = valid[p_index]
    # elif c_gate == 'W' or nextnext != 0 or prepre != 0 or (c_gate == 'C' and restricted) or (
            # restricted and placed_preds != [] and placed_preds[0] == 'C'):
    elif c_gate == 'W' or nextnext != 0 or prepre != 0 or (c_gate == 'C'): #three cases: fill wire and fill the nextnext
        parent_node = list(range(len(shape[p_index])))
    if c_gate == 'C' and next in only_right:  # check if only right
        right = 1
        only_right.remove(next)
    else:
        right = 0
    for j in parent_node: #iterate all the feasible node of the parents and create new table
        parent = copy.deepcopy(table[p_index][j])
        start_p = parent['starts']
        end_p = parent['ends']
        front = parent['front']
        p_shape = shape[p_index][j]  # parent shape
        p_table = table[p_index][j]
        p_row = p_table['row']
        wire_target = parent['targets']  # for recording the current wire target
        preds = parent['preds']  # recording the current preds
        if next not in two_wire and not_placed_preds != n_preds: #forward
            base = front.pop(c_index) #start base
            next_qubit = get_next_qubit(nodes, next)
            if c_gate == 'C': #check if only right
                avoild_points = check_avoid(front, p_shape)
                p_gate1, _ = new_sucessors[0].split('.')
                avoid_dir = 0
                if p_gate1 == 'A' or p_gate1 == 'B':
                    new_loc = check_loc(nodes, placed + next_list, new_sucessors[0], graph, two_wire)
                    if new_loc == 'u':
                        avoid_dir = 'd'
                    elif new_loc == 'd':
                        avoid_dir = 'u'
                shapes, fronts, spaces, new, wire_targets, starts, ends = place_C(p_shape, base, loc, rows, p_row, front, shapes, fronts, spaces,
                qubits - c_qubit, wire_target, wire_targets, right, next_qubit, qubit_record, start_p, end_p, starts, ends, avoild_points, avoid_dir)
            elif c_gate == 'A':
                shapes, fronts, spaces, new, wire_targets, starts, ends = place_A(p_shape, base, loc, rows, p_row, front, shapes, fronts, spaces,
                qubits - c_qubit, new_sucessors, end, not_placed, wire_targets, wire_target, next_qubit, qubit_record, start_p, end_p, starts, ends, new_qubit)
            elif c_gate == 'B':
                shapes, fronts, spaces, new, wire_targets, starts, ends = place_B(p_shape, base, loc, rows, p_row, front, shapes, fronts, spaces,
                qubits - c_qubit, new_sucessors, end, not_placed, wire_targets, wire_target, next_qubit, qubit_record, start_p, end_p, starts, ends, new_qubit)
            elif c_gate == 'B1':
                shapes, fronts, spaces, new, wire_targets, starts, ends = place_B1(p_shape, base, loc, rows, p_row,
                                                                                  front, shapes, fronts, spaces,
                                                                                  qubits - c_qubit, new_sucessors, end,
                                                                                  not_placed, wire_targets, wire_target,
                                                                                  next_qubit, qubit_record, start_p,
                                                                                  end_p, starts, ends, new_qubit)
            elif c_gate == 'W':
                wire_len = W_len[int(gate_index)] + 3 #for the special combination gate
                t_index = preds.index(next)
                preds.remove(next)
                target = wire_target.pop(t_index)
                shapes, fronts, spaces, new, wire_targets = place_W(p_shape, base, rows, p_row, front, shapes, fronts, spaces, target, wire_len, wire_target, wire_targets, special_greedy)
                if new:
                    starts.append(start_p)
                    ends.append(end_p)
        else: #backward
            wire_target = parent['targets']
            preds = parent['preds']
            t_index = preds.index(next)
            preds.remove(next)
            base = wire_target.pop(t_index)
            if c_gate == 'A':
                shapes, fronts, spaces, new, wire_targets, starts, ends = reversed_place_A(p_shape, base, loc, rows, p_row, front,
                                                                    shapes, fronts, spaces, qubits - c_qubit,new_sucessors,
                                                                    wire_targets, wire_target, b_end, start_p, end_p, starts, ends, n_preds)
            elif c_gate == 'B':
                shapes, fronts, spaces, new, wire_targets, starts, ends = reversed_place_B(p_shape, base, loc, rows, p_row, front,
                                                                    shapes, fronts, spaces, qubits - c_qubit, new_sucessors,
                                                                    wire_targets, wire_target, b_end, start_p, end_p, starts, ends, n_preds)
            elif c_gate == 'C':
                shapes, fronts, spaces, new, wire_targets, starts, ends = reversed_place_C(p_shape, base, loc, rows,
                                                                                               p_row, front,
                                                                                               shapes, fronts, spaces,
                                                                                               qubits - c_qubit,
                                                                                               wire_targets,
                                                                                               wire_target, start_p, end_p, starts, ends)
        for i in range(new):
            parents.append([p_index, j])

    new_preds = preds + not_placed_preds
    while nextnext != 0:
        next = nextnext
        print(next)
        newnew_sucessors = list(graph.successors(nextnext))
        shapes, fronts, spaces, successors, nextnext, parents, same_qubit, wire_targets, starts, ends = fill_nextnext(shapes, fronts, spaces, successors, nextnext, newnew_sucessors, parents,
            nodes, same_qubit, wire_targets, starts, ends)
        if len(newnew_sucessors) == 1:  # detect end point for forward
            p_gate1, _ = newnew_sucessors[0].split('.')
            if p_gate1 == 'C':
                only_right = detect_only_right(next, graph, only_right)
        if len(newnew_sucessors) == 2:  # detect only right(all second C will be forward)
            p_gate1, _ = newnew_sucessors[0].split('.')
            p_gate2, _ = newnew_sucessors[1].split('.')
            if p_gate1 == 'C' or p_gate2 == 'C':
                only_right = detect_only_right(next, graph, only_right)
        next_list.append(next)
    while prepre != 0:
        next = prepre
        print(next)
        newnew_preds = list(graph.predecessors(prepre))
        shapes, fronts, spaces, new_preds, prepre, parents, same_qubit, wire_targets, starts, ends = fill_prepre(
            shapes, fronts, spaces, new_preds, not_placed_preds, prepre, newnew_preds, parents,
            nodes, same_qubit, wire_targets, starts, ends)
        next_list.append(next)
    update(next, c_qubit, shapes, fronts, spaces, parents, table, shape, valid, successors,
           p_index, rows, wire_targets, new_preds, qubits, starts, ends)
    return next_list

def update(current, c_qubit, shapes, fronts, spaces, parents, table, shape, valid, successors,
           p_index, row_limit, wire_targets, new_preds, qubits, starts, ends):
    rows = []
    depths = []
    table.append([])
    shape.append([])
    invalid_list = []
    for i in range(len(shapes)):
        rows.append(len(shapes[i]))
        depths.append(len(shapes[i][0]))
        start = starts[i]
        end = ends[i]
        start.sort()
        end.sort()
        valid_starts_end = check_valid_start_end(start, end)
        if valid_starts_end == 0:
            invalid_list.append(i)
            continue
        table[p_index + 1].append({'New': current, 'P': parents[i], 'row': len(shapes[i]), 'S': spaces[i], 'D': depths[i], 'Q': c_qubit,
        'front': fronts[i], 'successor': successors, 'targets':wire_targets[i], 'preds': new_preds, 'starts':start, 'ends':end})
        shape[p_index + 1].append(shapes[i])
    invalid_list.sort(reverse=True)
    for index in invalid_list:
        rows.pop(index)
        depths.pop(index)
        spaces.pop(index)
    new_valid = check_valid(rows, depths, spaces, row_limit, c_qubit, qubits)
    valid.append(new_valid)

def detect_only_right(next, graph, only_right):
    sucessors = list(graph.successors(next))
    if len(sucessors) == 2:
        s1 = list(graph.successors(sucessors[0]))[0]
        s2 = list(graph.successors(sucessors[1]))[0]
        gs1, _ = s1.split('.')
        if s1 == s2 and (gs1 == 'B' or gs1 == 'C'):
            only_right.append(sucessors[0])
            only_right.append(sucessors[1])
    s1 = sucessors[0]
    gs1, _ = s1.split('.')
    while gs1 == 'C':
        s1 = list(graph.successors(s1))[0]
        gs1, _ = s1.split('.')
        if gs1 == 'C':
            only_right.append(s1)
    if len(sucessors) == 2:
        s2 = sucessors[1]
        gs2, _ = s2.split('.')
        while gs2 == 'C':
            s2 = list(graph.successors(s2))[0]
            gs2, _ = s2.split('.')
            if gs2 == 'C':
                only_right.append(s2)
    return only_right

def detec_end_b(next, pred, nodes):
    first_qubit = 0
    second_qubit = 0
    gate, _ = pred.split('.')
    for i in range(len(nodes)):
        if next in nodes[i]:
            first_qubit = first_qubit + i
        if pred in nodes[i]:
            second_qubit = second_qubit + i
    if gate == 'A' or gate == 'B':
        if second_qubit - first_qubit < 0:
            end = 'd'
        elif second_qubit - first_qubit > 0:
            end = 'u'
    else:
        if first_qubit == second_qubit * 2 + 1:
            end = 'd'
        else:
            end = 'u'
    return end

def check_valid(rows, depths, spaces, row_limit, c_qubit, qubits):
    row_collect = copy.deepcopy(rows)
    row_collect = list(set(row_collect))
    row_collect.sort() #row collection
    row_index = [] #indexes of rows
    valid = []
    min_dep = min(depths)
    row_collect_num = [[] for _ in range(len(row_collect))]
    for i in range(len(rows)):
        index = row_collect.index(rows[i])
        row_index.append(index)
        row_collect_num[index].append(i)
    for i in range(len(row_collect_num)):
        # if row_collect[i] == row_limit:
        #     keep_more = 2 * keep
        if c_qubit == qubits:
            keep_more = 2 * keep
        else:
            keep_more = keep
        if len(row_collect_num[i]) > keep_more:
            c_depths = []
            c_spaces = []
            for j in row_collect_num[i]:
                c_depths.append(depths[j])
                c_spaces.append(spaces[j])
            valid = valid + rank_result(row_collect_num[i], c_depths, c_spaces, keep_more)
        else:
            valid = valid + row_collect_num[i]
    valid.sort()
    long_index = []
    for index in valid: #remove too long
        if depths[index] - min_dep >= long:
            long_index.append(index)
    for index in reversed(long_index):
        valid.remove(index)
    return valid

def rank_result(row_collect_num, c_depths, c_spaces, keep_more):
    temp_depth = copy.deepcopy(c_depths) #rank the depth
    temp_depth = list(set(temp_depth))
    temp_depth.sort()
    selected = []
    dep_group = [] #store the index of each depth
    for dep in temp_depth:
        temp_dep_group = []
        c_dep_group = []
        c_spaces_group = []
        offset = 0.01
        for i in range(len(c_depths)):
            if c_depths[i] == dep:
                c_dep_group.append(i)
                if c_spaces[i] in c_spaces_group:
                    c_spaces_group.append(c_spaces[i] + offset)
                    offset = offset + 0.01
                else:
                    c_spaces_group.append(c_spaces[i])
        temp_spaces_group = copy.deepcopy(c_spaces_group)
        temp_spaces_group.sort(reverse=True)
        for i in range(len(temp_spaces_group)):
            temp_dep_group.append(c_dep_group[c_spaces_group.index(temp_spaces_group[i])])
        dep_group = dep_group + temp_dep_group
    while(len(selected)!=keep_more):
        selected.append(row_collect_num[dep_group.pop(0)])
    selected.sort()
    return selected

def fill_nextnext(shapes, fronts, spaces, successors, nextnext, newnew_sucessors, parents, nodes, same_qubit, wire_targets, starts, ends):
    locs = []
    new_parents = []
    new_wire_target = []
    new_old_wire_target = []
    gate, _ = nextnext.split('.')
    #same_qubit = 0 #found node on the same qbits
    for i in range(len(successors)):
        if successors[i] == nextnext:
            locs.append(i)
    if gate == 'A':
        shapes, fronts, spaces, valid, starts, ends = fill_A(shapes, fronts, spaces, locs, same_qubit, starts, ends)
    elif gate == 'B':
        shapes, fronts, spaces, valid, starts, ends = fill_B(shapes, fronts, spaces, locs, same_qubit, starts, ends)
    same_qubit = 0 #if the next two-qubit gate has the same qubits
    if len(newnew_sucessors) == 1: #remove one front
        first_qubit = 0
        second_qubit = 0
        gate, _ = newnew_sucessors[0].split('.')
        for i in range(len(nodes)):
            if nextnext in nodes[i]:
                first_qubit = first_qubit + i
            if newnew_sucessors[0] in nodes[i]:
                second_qubit = second_qubit + i
        if gate == 'A' or gate == 'B':
            if second_qubit - first_qubit > 0:
                for i in range(len(fronts)):
                    ends[i].append(fronts[i][-2])
                    fronts[i].pop(-2)
            elif second_qubit - first_qubit < 0:
                for i in range(len(fronts)):
                    ends[i].append(fronts[i][-1])
                    fronts[i].pop(-1)
            else:
                same_qubit = 1
        else:
            if first_qubit == second_qubit * 2 + 1:
                for i in range(len(fronts)):
                    ends[i].append(fronts[i][-1])
                    fronts[i].pop(-1)
            else:
                for i in range(len(fronts)):
                    ends[i].append(fronts[i][-2])
                    fronts[i].pop(-2)

    elif len(newnew_sucessors) == 0:
        for i in range(len(fronts)):
            ends[i].append(fronts[i][-2])
            ends[i].append(fronts[i][-1])
            fronts[i].pop(-1)
            fronts[i].pop(-1)
    successors.remove(nextnext)
    successors.remove(nextnext)
    nextnext = 0
    for succ in newnew_sucessors:
        if succ in successors:
            nextnext = succ
        elif same_qubit:
            nextnext = succ
            successors.append(succ)
        successors.append(succ)
    for index in valid:
        new_parents.append(parents[index])
        if wire_targets != []:
            new_wire_target.append(wire_targets[index])
    return shapes, fronts, spaces, successors, nextnext, new_parents, same_qubit, new_wire_target, starts, ends

def fill_prepre(shapes, fronts, spaces, new_preds, not_placed_preds, prepre, newnew_preds, parents,
            nodes, same_qubit, wire_targets, starts, ends):
    locs = []
    new_parents = []
    gate, _ = prepre.split('.')
    # same_qubit = 0 #found node on the same qbits
    for i in range(len(new_preds)):
        if new_preds[i] == prepre:
            locs.append(i)
    if gate == 'A':
        shapes, fronts, spaces, valid, wire_targets, starts, ends = fill_A_P(shapes, fronts, wire_targets, locs, same_qubit, starts, ends)
    elif gate == 'B':
        shapes, fronts, spaces, valid, wire_targets, starts, ends = fill_B_P(shapes, fronts, wire_targets, locs, same_qubit, starts, ends)
    same_qubit = 0
    if len(newnew_preds) == 1:  # remove one front
        first_qubit = 0
        second_qubit = 0
        gate, _ = newnew_preds[0].split('.')
        for i in range(len(nodes)):
            if prepre in nodes[i]:
                first_qubit = first_qubit + i
            if newnew_preds[0] in nodes[i]:
                second_qubit = second_qubit + i
        if gate == 'A' or gate == 'B':
            if second_qubit - first_qubit > 0:
                for i in range(len(wire_targets)):
                    starts[i].append(wire_targets[i][-2])
                    wire_targets[i].pop(-2)
            elif second_qubit - first_qubit < 0:
                for i in range(len(wire_targets)):
                    starts[i].append(wire_targets[i][-1])
                    wire_targets[i].pop(-1)
            else:
                same_qubit = 1
        else:
            if first_qubit == second_qubit * 2 + 1:
                for i in range(len(wire_targets)):
                    starts[i].append(wire_targets[i][-1])
                    wire_targets[i].pop(-1)
            else:
                for i in range(len(wire_targets)):
                    starts[i].append(wire_targets[i][-2])
                    wire_targets[i].pop(-2)
    elif len(newnew_preds) == 0:
        for i in range(len(wire_targets)):
            starts[i].append(wire_targets[i][-2])
            starts[i].append(wire_targets[i][-1])
            wire_targets[i].pop(-1)
            wire_targets[i].pop(-1)
    new_preds.remove(prepre)
    new_preds.remove(prepre)
    prepre = 0
    for succ in newnew_preds:
        if succ in new_preds:
            prepre = succ
        elif same_qubit:
            prepre = succ
            new_preds.append(succ)
        new_preds.append(succ)
    for index in valid:
        new_parents.append(parents[index])
    return shapes, fronts, spaces, new_preds, prepre, new_parents, same_qubit, wire_targets, starts, ends

def check_avoid(front, shape):
    points = []
    for point in front:
        if point[0] == 0:
            points.append([point[0], point[1] + 2])
            points.append([point[0] + 1, point[1] + 1])
            points.append([point[0] + 2, point[1]])
        elif point[0] != len(shape) - 1 and shape[point[0] - 1][point[1]] != 0 and shape[point[0] + 1][point[1]] != 0:
            points.append([point[0] - 2, point[1]])
            points.append([point[0] - 1, point[1] + 1])
            points.append([point[0] - 1, point[1] + 2])
            points.append([point[0], point[1] + 2])
            points.append([point[0], point[1] + 3])
            points.append([point[0] + 1, point[1] + 2])
            points.append([point[0] + 1, point[1] + 1])
            points.append([point[0] + 2, point[1]])
        else:
            points.append([point[0] - 2, point[1]])
            points.append([point[0] - 1, point[1] + 1])
            points.append([point[0], point[1] + 2])
            points.append([point[0] + 1, point[1] + 1])
            points.append([point[0] + 2, point[1]])
    return points

def get_next_qubit(nodes, next):
    c_qubit = []
    for i in range(len(nodes)):
        if next in nodes[i]:
            c_qubit.append(i + 1)
    return c_qubit

def check_ancestor(node, graph, placed, independent_node):
    current_node = node
    queue = list(graph.predecessors(current_node))
    found_placed = 0
    while queue != []:
        current_node = queue.pop(0)
        if current_node in placed:
            return 1
        elif current_node in independent_node:
            return 0
        else:
            queue = queue + list(graph.predecessors(current_node))
    return found_placed

def find_combine(onle_one_pre):
    for i in range(len(onle_one_pre)):
        for j in range(len(onle_one_pre)):
            if i != j and onle_one_pre[i] == onle_one_pre[j] and onle_one_pre[i] != []:
                return [i, j]

def combine(next, table0, shape0, table1, shape1, rows, nodes, placed0, placed1, graph, qubit_num, placed, nodes_left):
    new_tables = []
    new_shapes = []
    c_gate = next.split('.')
    parent0 = copy.deepcopy(table0[0])
    successors0 = parent0['successor']
    successors0.remove(next)
    preds0 = parent0['preds']
    parent1 = copy.deepcopy(table1[0])
    successors1 = parent1['successor']
    successors1.remove(next)
    preds1 = parent1['preds']
    qubits = parent0['Q'] + parent1['Q']
    loc0 = check_loc(nodes, placed0, next, graph, [])
    loc1 = check_loc(nodes, placed1, next, graph, [])
    next_sucessors = list(graph.successors(next))
    if len(next_sucessors) == 1:
        end = detec_end(next, next_sucessors[0], nodes)
    else:
        end = ''
    if loc0 == loc1:
        print('Wrong!')
    if loc0 == 'd':
        new_sucessor = successors0 + successors1
        new_preds = preds0 + preds1
    elif loc0 == 'u':
        new_sucessor = successors1 + successors0
        new_preds = preds1 + preds0
    nextnext = 0
    same_qubit = 0
    if (c_gate == 'A' or c_gate == 'B' or c_gate == 'B1') and len(next_sucessors) == 1:
        end = detec_end(next, next_sucessors[0], nodes)
        if end == 0:
            nextnext = next_sucessors[0]
            same_qubit = 1
    for succ in next_sucessors:
        if succ in new_sucessor:
            nextnext = succ
        if succ not in placed:
            new_sucessor.append(succ)
            if same_qubit == 1:
                new_sucessor.append(succ)
    # new_sucessor = new_sucessor + next_sucessors
    for i in range(len(table0)):
        for j in range(len(table1)):
            parent0 = copy.deepcopy(table0[i])
            parent1 = copy.deepcopy(table1[j])
            front0 = parent0['front']
            starts0 = parent0['starts']
            ends0 = parent0['ends']
            targets0 = parent0['targets']
            front1 = parent1['front']
            starts1 = parent1['starts']
            ends1 = parent1['ends']
            targets1 = parent1['targets']
            index0 = table0[i]['successor'].index(next)
            index1 = table1[j]['successor'].index(next)
            front0.pop(index0)
            front1.pop(index1)
            point0 = table0[i]['front'][index0]
            point1 = table1[j]['front'][index1]
            gate, _ = next.split('.')
            new_shape, new_table = check_combine_possible(shape0[i], shape1[j], point0, point1, next, rows, loc0, front0,
                                        front1, starts0, starts1, ends0, ends1, targets0, targets1, new_sucessor, new_preds, next_sucessors, end, qubits)
            new_tables = new_tables + new_table
            new_shapes = new_shapes + new_shape
    rows_collect, depths_collect, space_collect, qubit_collect, front_collect, targets_collect, starts_collect, ends_collect = get_collection(new_tables)
    while nextnext != 0:
        placed.append(nextnext)
        next = nextnext
        nodes_left.remove(next)
        print(next)
        newnew_sucessors = list(graph.successors(nextnext))
        parents = ['NA']*len(new_shapes)
        new_shapes, front_collect, space_collect, new_sucessor, nextnext, parents, same_qubit, targets_collect, starts_collect, ends_collect = fill_nextnext(new_shapes, front_collect, space_collect, new_sucessor, nextnext, newnew_sucessors, parents,
            nodes, same_qubit, targets_collect, starts_collect, ends_collect)
        new_tables, rows_collect, depths_collect, qubit_collect = update_table(next, qubit_collect[0], new_shapes, front_collect, space_collect, new_sucessor, targets_collect, new_preds, starts_collect, ends_collect)
    new_valid = check_valid(rows_collect, depths_collect, space_collect, rows, qubit_collect, qubit_num)
    final_shapes = []
    final_tables = []
    for valid in new_valid:
        final_tables.append(new_tables[valid])
        final_shapes.append(new_shapes[valid])
    return final_tables, final_shapes, placed, nodes_left

def check_combine_possible(shape0, shape1, loc0, loc1, next, rows, pos0, front0, front1,
                           starts0, starts1, ends0, ends1, targets0, targets1, new_sucessor, new_preds, next_sucessors, end, qubits):
    new_table = []
    new_shape = []
    if pos0 == 'd': #shape0 on top
        #first situation
        new_loc1 = [loc0[0] + 2, loc0[1]]
        shape, table = check_valid_combine(shape0, shape1, loc0, loc1, new_loc1, next, rows, front0, front1,
                                           starts0, starts1, ends0, ends1, targets0, targets1, new_sucessor, new_preds, next_sucessors, end, qubits)
        new_shape.append(shape)
        new_table.append(table)
        new_loc1 = [loc0[0] + 3, loc0[1] + 1]
        shape, table = check_valid_combine(shape0, shape1, loc0, loc1, new_loc1, next, rows, front0, front1,
                                           starts0, starts1, ends0, ends1, targets0, targets1, new_sucessor, new_preds, next_sucessors, end, qubits)
        new_shape.append(shape)
        new_table.append(table)
        new_loc1 = [loc0[0] + 3, loc0[1] - 1]
        shape, table = check_valid_combine(shape0, shape1, loc0, loc1, new_loc1, next, rows, front0, front1,
                                           starts0, starts1, ends0, ends1, targets0, targets1, new_sucessor, new_preds, next_sucessors, end, qubits)
        new_shape.append(shape)
        new_table.append(table)
        new_loc1 = [loc0[0] + 4, loc0[1]]
        shape, table = check_valid_combine(shape0, shape1, loc0, loc1, new_loc1, next, rows, front0, front1,
                                           starts0, starts1, ends0, ends1, targets0, targets1, new_sucessor, new_preds,
                                           next_sucessors, end, qubits)
        new_shape.append(shape)
        new_table.append(table)
    elif pos0 == 'u': #shape0 down
        new_loc0 = [loc1[0] + 2, loc1[1]]
        shape, table = check_valid_combine(shape1, shape0, loc1, loc0, new_loc0, next, rows, front1, front0,
                                           starts1, starts0, ends1, ends0, targets1, targets0, new_sucessor, new_preds, next_sucessors, end, qubits)
        new_shape.append(shape)
        new_table.append(table)
        new_loc0 = [loc1[0] + 3, loc1[1] + 1]
        shape, table = check_valid_combine(shape1, shape0, loc1, loc0, new_loc0, next, rows, front1, front0,
                                           starts1, starts0, ends1, ends0, targets1, targets0, new_sucessor, new_preds, next_sucessors, end, qubits)
        new_shape.append(shape)
        new_table.append(table)
        new_loc0 = [loc1[0] + 3, loc1[1] - 1]
        shape, table = check_valid_combine(shape1, shape0, loc1, loc0, new_loc0, next, rows, front1, front0,
                                           starts1, starts0, ends1, ends0, targets1, targets0, new_sucessor, new_preds, next_sucessors, end, qubits)
        new_shape.append(shape)
        new_table.append(table)
        new_loc0 = [loc1[0] + 4, loc1[1]]
        shape, table = check_valid_combine(shape1, shape0, loc1, loc0, new_loc0, next, rows, front1, front0,
                                           starts1, starts0, ends1, ends0, targets1, targets0, new_sucessor, new_preds, next_sucessors, end, qubits)
        new_shape.append(shape)
        new_table.append(table)
    return new_shape, new_table

def check_valid_combine(shape0, shape1, loc0, loc1, new_loc1, next, rows, front0, front1,
                        starts0, starts1, ends0, ends1, targets0, targets1, new_sucessor, new_preds, next_sucessors, end, qubits): #loc0 is the upper shape
    gate, _ = next.split('.')
    new_shape = copy.deepcopy(shape0)
    new_table = []
    total_row = new_loc1[0] + len(shape1) - loc1[0]
    temp_loc0 = copy.deepcopy(loc0)
    temp_loc1 = copy.deepcopy(loc1)
    if total_row > rows:
        return [], new_table
    if total_row > len(new_shape):
        for i in range(total_row - len(new_shape)):
            new_shape.append([0]*len(new_shape[0]))
    length_difference = loc1[1] - new_loc1[1] #used to update the table
    if length_difference > 0:
        for i in range(len(new_shape)):
            new_shape[i] = [0]*length_difference + new_shape[i]
        temp_loc0[1] = temp_loc0[1] + length_difference
        new_loc1[1] = new_loc1[1] + length_difference
    new_length = max(len(shape1[0]) - loc1[1] + new_loc1[1], temp_loc0[1] + len(shape0[0]) - loc0[1])
    if new_loc1[1] == temp_loc0[1] and abs(new_loc1[0] - temp_loc0[0]) == 2:
        new_length = max(new_length, new_loc1[1] + 3)
        place_pt = [temp_loc0[0], temp_loc0[1] + 1]
    elif new_loc1[1] - temp_loc0[1] == 1:
        new_length = max(new_length, new_loc1[1] + 2)
        place_pt = [temp_loc0[0], temp_loc0[1] + 1]
    elif temp_loc0[1] - new_loc1[1] == 1 or abs(new_loc1[0] - temp_loc0[0]) == 4:
        new_length = max(new_length, temp_loc0[1] + 2)
        place_pt = [temp_loc0[0] + 1, temp_loc0[1]]
    if new_length > len(new_shape[0]):
        extra_len = new_length - len(new_shape[0])
        for i in range(len(new_shape)):
            new_shape[i] = new_shape[i] + extra_len*[0]
    start_pt = [new_loc1[0] - temp_loc1[0], new_loc1[1] - temp_loc1[1]]
    for i in range(len(shape1)):
        for j in range(len(shape1[0])):
            if new_shape[i + start_pt[0]][j + start_pt[1]] != 0:
                return []
            new_shape[i + start_pt[0]][j + start_pt[1]] = shape1[i][j]
    if gate == 'A':
        for i in range(3):
            new_shape[place_pt[0] + i][place_pt[1]] = 1
        new_pts = [[place_pt[0], place_pt[1]],[place_pt[0] + 2, place_pt[1]]]
    elif gate == 'B':
        for i in range(3):
            for j in range(2):
                new_shape[place_pt[0] + i][place_pt[1] + j] = 1
        new_pts = [[place_pt[0], place_pt[1] + 1], [place_pt[0] + 2, place_pt[1] + 1]]
    #create table
    new_shape, space = fill_shape(new_shape)
    X_offset0 = temp_loc0[0] - loc0[0]
    Y_offset0 = temp_loc0[1] - loc0[1]
    X_offset1 = new_loc1[0] - loc1[0]
    Y_offset1 = new_loc1[1] - loc1[1]
    front0 = copy.deepcopy(front0)
    front1 = copy.deepcopy(front1)
    targets0 = copy.deepcopy(targets0)
    targets1 = copy.deepcopy(targets1)
    starts0 = copy.deepcopy(starts0)
    starts1 = copy.deepcopy(starts1)
    ends0 = copy.deepcopy(ends0)
    ends1 = copy.deepcopy(ends1)
    for i in range(len(front0)):
        front0[i][0] = front0[i][0] + X_offset0
        front0[i][1] = front0[i][1] + Y_offset0
    for i in range(len(front1)):
        front1[i][0] = front1[i][0] + X_offset1
        front1[i][1] = front1[i][1] + Y_offset1
    for i in range(len(targets0)):
        targets0[i][0] = targets0[i][0] + X_offset0
        targets0[i][1] = targets0[i][1] + Y_offset0
    for i in range(len(targets1)):
        targets1[i][0] = targets1[i][0] + X_offset1
        targets1[i][1] = targets1[i][1] + Y_offset1
    for i in range(len(starts0)):
        starts0[i][0] = starts0[i][0] + X_offset0
        starts0[i][1] = starts0[i][1] + Y_offset0
    for i in range(len(starts1)):
        starts1[i][0] = starts1[i][0] + X_offset1
        starts1[i][1] = starts1[i][1] + Y_offset1
    for i in range(len(ends0)):
        ends0[i][0] = ends0[i][0] + X_offset0
        ends0[i][1] = ends0[i][1] + Y_offset0
    for i in range(len(ends1)):
        ends1[i][0] = ends1[i][0] + X_offset1
        ends1[i][1] = ends1[i][1] + Y_offset1
    new_starts = starts0 + starts1
    new_target = targets0 + targets1
    new_ends = ends0 + ends1
    if len(next_sucessors) == 2:
        new_front = front0 + front1 + new_pts
    elif end == 'u':
        new_front = front0 + front1 + [new_pts[1]]
        new_ends.append(new_pts[0])
    elif end == 'd':
        new_front = front0 + front1 + [new_pts[0]]
        new_ends.append(new_pts[1])
    elif len(next_sucessors) == 1:
        new_ends = new_ends + new_pts
    new_table = {'New': next, 'P': 'NA', 'row': len(new_shape), 'S': space, 'D': len(new_shape[0]), 'Q': qubits,
        'front': new_front, 'successor': new_sucessor, 'targets':new_target, 'preds': new_preds, 'starts':new_starts, 'ends':new_ends}
    return new_shape, new_table

def get_collection(new_table):
    rows_collect = []
    depths_collect = []
    space_collect = []
    qubit_collect = []
    front_collect = []
    ends_collect = []
    starts_collect = []
    targets_collect = []
    for table in new_table:
        rows_collect.append(table['row'])
        depths_collect.append(table['D'])
        space_collect.append(table['S'])
        qubit_collect.append(table['Q'])
        front_collect.append(table['front'])
        ends_collect.append(table['ends'])
        starts_collect.append(table['starts'])
        targets_collect.append(table['targets'])
    return rows_collect, depths_collect, space_collect, qubit_collect, front_collect, targets_collect, starts_collect, ends_collect

def update_table(next, qubits, new_shapes, front_collect, space_collect, successors, targets_collect, new_preds, starts_collect, ends_collect):
    new_tables = []
    rows_collect = []
    depths_collect = []
    qubit_collects = []
    for i in range(len(new_shapes)):
        rows_collect.append(len(new_shapes[i]))
        depths_collect.append(len(new_shapes[i][0]))
        qubit_collects.append(qubits)
        new_table = {'New': next, 'P': 'NA', 'row': len(new_shapes[i]), 'S': space_collect[i], 'D': len(new_shapes[i][0]), 'Q': qubits,
                     'front': front_collect[i], 'successor': successors, 'targets': targets_collect[i], 'preds': new_preds,
                     'starts': starts_collect[i], 'ends': ends_collect[i]}
        new_tables.append(new_table)
    return new_tables, rows_collect, depths_collect, qubit_collects

def check_valid_start_end(start, end):
    valid = 1
    if len(start) != 0:
        for i in range(len(start) - 1):
            if abs(start[i + 1][0] - start[i][0]) < 2:
                return 0
    if len(end) != 0:
        for i in range(len(end) - 1):
            if abs(end[i + 1][0] - end[i][0]) < 2:
                return 0
    return 1
