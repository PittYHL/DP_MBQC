import numpy as np
import math
from gate_blocks import *
from new_swap import *
# from scheduling import *
# from elastic import *
from DP import *
import copy
from dense import *
import csv
def biuld_DAG(gates):
    DAG_list = gates.copy()
keep = 2
qubits = 5
rows = 9
flip = False
first_loc = 'm'
file_name = "results/hwea15_" + first_loc + "_" + str(rows) + "_" + str(keep) + ".txt"
# force_right = False#force the second c to the right
# special = 0#for special leaves
wire_remove = 1
remove_single = 1 #for removing the single qubit gate
remove_SWAP = 1
# restricted = 0 #restrict the qubit locate
remove_y = 0#for CNOT (QAOA)
# special_greedy = 0
physical_gate = []
tracker= []
map = []
direc = 'd'
for i in range(qubits*2-1):
    map.append([])
for i in range(qubits):
    tracker.append(i)
with open('Benchmarks/hwea5.txt') as f:
    lines = f.readlines()
circuit= lines.copy()
layer = []
tracker = [] #track physical location
for i in range(qubits):
    tracker.append(i)
next = 0
for current in circuit:
    gate, t1, t2, _, name = de_gate(current)
    if t1 != t2:
        if next == 1:
            break
        t3 = t1
        t4 = t2
        next = 1

while math.fabs(tracker[t3] - tracker[t4]) != 1:
    if tracker[t3] - tracker[t4] > 2:
        tracker[tracker.index(tracker[t3] - 1)] = tracker[tracker.index(tracker[t3] - 1)] + 1
        tracker[t3] = tracker[t3] - 1
        tracker[tracker.index(tracker[t4] + 1)] = tracker[tracker.index(tracker[t4] + 1)] - 1
        tracker[t4] = tracker[t4] + 1
    elif tracker[t4] - tracker[t3]> 2:
        tracker[tracker.index(tracker[t3] + 1)] = tracker[tracker.index(tracker[t3] + 1)] - 1
        tracker[t3] = tracker[t3] + 1
        tracker[tracker.index(tracker[t4] - 1)] = tracker[tracker.index(tracker[t4] - 1)] + 1
        tracker[t4] = tracker[t4] - 1
    elif tracker[t3] - tracker[t4] == 2:
        temp_t1 = copy.deepcopy(tracker)
        temp_t2 = copy.deepcopy(tracker)
        current_dis = math.fabs(tracker[t1] - tracker[t2])
        temp_t1[tracker.index(tracker[t3] - 1)] = temp_t1[tracker.index(tracker[t3] - 1)] + 1
        temp_t1[t3] = temp_t1[t3] - 1
        temp_t2[tracker.index(tracker[t4] + 1)] = temp_t2[tracker.index(tracker[t4] + 1)] - 1
        temp_t2[t4] = temp_t2[t4] + 1
        new_dist1 = math.fabs(temp_t1[t1] - temp_t1[t2])
        new_dist2 = math.fabs(temp_t2[t1] - temp_t2[t2])
        if new_dist1 < new_dist2:
            tracker = temp_t1
        else:
            tracker = temp_t2
    elif tracker[t4] - tracker[t3] == 2:
        temp_t1 = copy.deepcopy(tracker)
        temp_t2 = copy.deepcopy(tracker)
        current_dis = math.fabs(tracker[t1] - tracker[t2])
        temp_t1[tracker.index(tracker[t4] - 1)] = temp_t1[tracker.index(tracker[t4] - 1)] + 1
        temp_t1[t4] = temp_t1[t4] - 1
        temp_t2[tracker.index(tracker[t3] + 1)] = temp_t2[tracker.index(tracker[t3] + 1)] - 1
        temp_t2[t3] = temp_t2[t3] + 1
        new_dist1 = math.fabs(temp_t1[t1] - temp_t1[t2])
        new_dist2 = math.fabs(temp_t2[t1] - temp_t2[t2])
        if new_dist1 < new_dist2:
            tracker = temp_t1
        else:
            tracker = temp_t2
new_circuit = []
for gate in circuit:
    X = gate.split()
    if X[0] == 'H' or X[0] == 'P' or X[0] == 'S' or X[0] == 'Z' or X[0] == 'RX' or X[0] == 'RZ' or X[0] == 'X' or X[0] == 'T' or X[0] == 'A':
        t1 = str(tracker[int(X[1])])
        new_circuit.append(X[0] + ' ' + t1)
    else:
        t1 = str(tracker[int(X[1])])
        t2 = str(tracker[int(X[2])])
        new_circuit.append(X[0] + ' ' + t1 + ' ' + t2)

tracker= []
for i in range(qubits):
    tracker.append(i)
while(new_circuit!=[]):
    current = new_circuit.pop(0)
    gate, t1, t2, _, name = de_gate(current)
    if (gate == H or gate == P or gate == S or gate == T or gate == Z or gate == RX or gate == A or gate == RZ):
        if t1 in layer:
            layer = []
            layer.append(t1)
            fill_map(qubits,map)
        else:
            layer.append(t1)
        map[tracker[t1]*2] = map[tracker[t1]*2] + gate
        #physical_gate.append(name + str(tracker[t1]))
        physical_gate.append({'gate':name, 'type':'S', 't1':tracker[t1]})
    elif(gate==CNOT):
        if t1 in layer or t2 in layer:
            layer = []
            layer.append(t1)
            layer.append(t2)
            fill_map(qubits,map)
        else:
            layer.append(t1)
            layer.append(t2)
        if tracker[t1] - tracker[t2] == 1:
            map[tracker[t1] * 2].extend(CNOT[0])
            map[tracker[t2] * 2 + 1].extend(CNOT[1])
            map[tracker[t2] * 2].extend(CNOT[2])
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
        elif tracker[t1] - tracker[t2] == -1:
            map[tracker[t1] * 2].extend(CNOT[0])
            map[tracker[t1] * 2 + 1].extend(CNOT[1])
            map[tracker[t2] * 2].extend(CNOT[2])
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
        elif tracker[t1] - tracker[t2] > 1:
            #worst case
            intel_swap(map, t2, t1, tracker, new_circuit, physical_gate)
            map[tracker[t1] * 2].extend(CNOT[0])
            map[tracker[t2] * 2 + 1].extend(CNOT[1])
            map[tracker[t2] * 2].extend(CNOT[2])
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
        else:
            intel_swap(map, t1, t2, tracker, new_circuit, physical_gate)
            map[tracker[t1] * 2].extend(CNOT[0])
            map[tracker[t1] * 2 + 1].extend(CNOT[1])
            map[tracker[t2] * 2].extend(CNOT[2])
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
    elif(gate==CZS):
        if t1 in layer or t2 in layer:
            layer = []
            layer.append(t1)
            layer.append(t2)
            fill_map(qubits,map)
        else:
            layer.append(t1)
            layer.append(t2)
        if tracker[t1] - tracker[t2] == 1:
            map[tracker[t1] * 2].extend(CZS[0])
            map[tracker[t2] * 2 + 1].extend(CZS[1])
            map[tracker[t2] * 2].extend(CZS[2])
            temp = tracker[t1]
            tracker[t1] = tracker[t2]
            tracker[t2] = temp
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
        elif tracker[t1] - tracker[t2] == -1:
            map[tracker[t1] * 2].extend(CZS[0])
            map[tracker[t1] * 2 + 1].extend(CZS[1])
            map[tracker[t2] * 2].extend(CZS[2])
            temp = tracker[t1]
            tracker[t1] = tracker[t2]
            tracker[t2] = temp
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
        elif tracker[t1] - tracker[t2] > 1:
            intel_swap(map, t2, t1, tracker, new_circuit, physical_gate)
            map[tracker[t1] * 2].extend(CZS[0])
            map[tracker[t2] * 2 + 1].extend(CZS[1])
            map[tracker[t2] * 2].extend(CZS[2])
            temp = tracker[t1]
            tracker[t1] = tracker[t2]
            tracker[t2] = temp
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
        else:
            intel_swap(map, t1, t2, tracker, new_circuit, physical_gate)
            map[tracker[t1] * 2].extend(CZS[0])
            map[tracker[t1] * 2 + 1].extend(CZS[1])
            map[tracker[t2] * 2].extend(CZS[2])
            temp = tracker[t1]
            tracker[t1] = tracker[t2]
            tracker[t2] = temp
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
    elif (gate == CPS):
        if t1 in layer or t2 in layer:
            layer = []
            layer.append(t1)
            layer.append(t2)
            fill_map(qubits, map)
        else:
            layer.append(t1)
            layer.append(t2)
        if tracker[t1] - tracker[t2] == 1:
            map[tracker[t1] * 2].extend(CPS[0])
            map[tracker[t2] * 2 + 1].extend(CPS[1])
            map[tracker[t2] * 2].extend(CPS[2])
            temp = tracker[t1]
            tracker[t1] = tracker[t2]
            tracker[t2] = temp
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
        elif tracker[t1] - tracker[t2] == -1:
            map[tracker[t1] * 2].extend(CPS[0])
            map[tracker[t1] * 2 + 1].extend(CPS[1])
            map[tracker[t2] * 2].extend(CPS[2])
            temp = tracker[t1]
            tracker[t1] = tracker[t2]
            tracker[t2] = temp
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
        elif tracker[t1] - tracker[t2] > 1:
            intel_swap(map, t2, t1, tracker, new_circuit, physical_gate)
            map[tracker[t1] * 2].extend(CPS[0])
            map[tracker[t2] * 2 + 1].extend(CPS[1])
            map[tracker[t2] * 2].extend(CPS[2])
            temp = tracker[t1]
            tracker[t1] = tracker[t2]
            tracker[t2] = temp
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
        else:
            intel_swap(map, t1, t2, tracker, new_circuit, physical_gate)
            map[tracker[t1] * 2].extend(CPS[0])
            map[tracker[t1] * 2 + 1].extend(CPS[1])
            map[tracker[t2] * 2].extend(CPS[2])
            temp = tracker[t1]
            tracker[t1] = tracker[t2]
            tracker[t2] = temp
            physical_gate.append({'gate':name, 'type':'D', 't1':tracker[t1], 't2':tracker[t2]})
fill_map(qubits,map)
if remove_SWAP:
    physical_gate = remove_SW(qubits, physical_gate)
DAG = dense(qubits, physical_gate)
dense_map = cons_new_map(qubits,DAG)
uti0, use0 = cal_utilization2(dense_map, rows)
de_map = np.array(dense_map)
# np.savetxt("iqp27_de.csv", de_map, fmt = '%s',delimiter=",")
#schedule = scheduling(qubits, DAG, rows)
#sche_ela = sche_ela(qubits,DAG, rows)
#ela_no = only_elastic(qubits,DAG, rows)
#sc_map = np.array(schedule)
#np.savetxt("qft4_sche.csv", sc_map, fmt = '%s',delimiter=",")
#de_map = np.array(dense_map)

# if wire_remove:
#     new_map = remove_wire(dense_map, qubits, remove_single, remove_y)
#     remove_leaves_wire(qubits, new_map)
new_map = new_eliminate_redundant(dense_map, qubits)
if wire_remove:
    new_map = remove_wire(new_map, qubits, remove_single, remove_y)
    new_map = new_eliminate_redundant(new_map, qubits)
newnew_map = convert_new_map(new_map)
n_map = np.array(newnew_map)
np.savetxt("example/hwea5el_111.csv", n_map, fmt = '%s',delimiter=",")
# file = open("example/hlf27el.csv", "r")
# new_map = list(csv.reader(file, delimiter=","))
# file.close()
hwea = True
for i in range(6, 7):
    file_name = "./results/hwea15_" + first_loc + "_" + str(rows) + "_" + str(i) + ".txt"
    DP(new_map, qubits, rows, flip, first_loc, file_name, i, hwea)
