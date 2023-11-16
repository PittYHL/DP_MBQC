import copy
import networkx as nx
from matplotlib import pyplot as plt

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
                if map[i * 2][s_row[i][j] + 1] == 2 and map[i * 2][s_row[i][j] + 2] == 2 and s_row[i][j + 1] - s_row[i][j] > 3:
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

def update_all_wires(order, W_len, graph, nodes):
    to_be_removed= []
    for node in order:
        gate, _ = node.split('.')
        if gate != 'A' and gate != 'B':
            continue
        else:
            all_wire = 1
            pre = list(graph.predecessors(node))
            suc = list(graph.successors(node))
            if pre == [] or suc == []:
                continue
            for p in pre:
                gate, _ = p.split('.')
                if gate != 'W':
                    all_wire = 0
                    break
            for s in suc:
                gate, _ = s.split('.')
                if gate != 'W':
                    all_wire = 0
                    break
            if all_wire == 1:
                min_len = 100000
                for p in pre:
                    gate, index = p.split('.')
                    if W_len[int(index)] < min_len:
                        min_len = W_len[int(index)]
                for p in pre:
                    gate, index = p.split('.')
                    W_len[int(index)] = W_len[int(index)] - min_len
                    if W_len[int(index)] == 0:
                        to_be_removed.append('W.' + index)
                for s in suc:
                    gate, index = s.split('.')
                    W_len[int(index)] = W_len[int(index)] + min_len
    if to_be_removed != []:
        for node in to_be_removed:
            for j in range(len(nodes)):
                if node in nodes[j]:
                    nodes[j].remove(node)
        new_graph = nx.DiGraph()
        for node in nodes:
            for i in range(len(node) - 1):
                new_graph.add_edge(node[i], node[i + 1])
        order = list(nx.topological_sort(new_graph))
        return order, W_len, new_graph, nodes
    return order, W_len, graph, nodes

def find_independent(graph, order):
    independent_node = []
    for node in order:
        pre = list(graph.predecessors(node))
        if pre == []:
            independent_node.append(node)
        else:
            break
    return independent_node

def get_qubit_record(current, nodes, qubit_record):
    for i in range(len(nodes)):
        if current in nodes[i]:
            if i + 1 not in qubit_record:
                qubit_record.append(i + 1)
    return qubit_record

def detec_end(next, succ, nodes):
    first_qubit = 0
    second_qubit = 0
    gate, _ = succ.split('.')
    for i in range(len(nodes)):
        if next in nodes[i]:
            first_qubit = first_qubit + i
        if succ in nodes[i]:
            second_qubit = second_qubit + i
    if gate == 'A' or gate == 'B':
        if second_qubit - first_qubit < 0:
            end = 'd'
        elif second_qubit - first_qubit > 0:
            end = 'u'
        else:
            end = 0
    else:
        if first_qubit == second_qubit * 2 + 1:
            end = 'd'
        else:
            end = 'u'
    return end

def check_loc(nodes, placed, next, graph, two_wire):
    newnext = 0
    preds = list(graph.predecessors(next))
    previous = 0
    no_pred = 0
    if next in two_wire:    #put back
        previous = next
        succs = list(graph.successors(next))
        for succ in succs:
            if succ in placed:
                newnext = succ
                break
    else:
        newnext = next
        for pred in preds:
            if pred in placed:
                previous = pred
                break
    if previous == 0: #no preds have been placed
        no_pred = 1 #no previous indication
        previous = next
        succs = list(graph.successors(next))
        for succ in succs:
            if succ in placed:
                newnext = succ
                break
    p_gate, _ = previous.split('.')
    c_gate, _ = newnext.split('.')
    if p_gate == 'A' or p_gate == 'B' or p_gate == 'B1':
        qubit1 = 0
        for i in range(len(nodes)):
            if previous in nodes[i]:
                qubit1 = i
                break
        if newnext in nodes[qubit1]:
            loc = 'u'
        else:
            loc = 'd'
    elif c_gate == 'A' or p_gate == 'B' or p_gate == 'B1':
        qubit1 = 0
        for i in range(len(nodes)):
            if newnext in nodes[i]:
                qubit1 = i
                break
        if previous in nodes[qubit1]:
            loc = 'd'
        else:
            loc = 'u'
    elif p_gate == 'C' and (c_gate == 'B' or c_gate == 'A' or p_gate == 'B1'):
        qubit1 = 0
        for i in range(len(nodes)):
            if previous in nodes[i]:
                qubit1 = i
                break
        if qubit1 == len(nodes) - 1 or newnext in nodes[qubit1 - 1]:
            loc = 'u'
        else:
            loc = 'd'
    else:
        loc = 'r'
    if (next in two_wire or no_pred) and loc == 'd':
        loc = 'u'
    elif (next in two_wire or no_pred) and loc == 'u':
        loc = 'd'
    return loc

def find_qubits(nodes, placed, next):
    qubit = []
    new_placed = placed + [next]
    for i in range(len(nodes)):
        for node in new_placed:
            if node in nodes[i]:
                qubit.append(i)
                break
    return len(qubit)