from gate_blocks import *

new_file = 'Benchmarks/qaoa42b.txt'
with open('Benchmarks/qaoa42.txt') as f:
    lines = f.readlines()
f.close()
circuit= lines.copy()
new_circuit = []
i=0
while i < len(circuit):
    X = circuit[i].split()
    if X[0] != 'RZ':
        new_circuit.append(circuit[i])
        i = i + 1
    elif X[0] == 'RZ':
        first = X[1]
        i = i + 1
        X = circuit[i].split()
        second = X[1]
        i = i + 4
        new_ZZ = 'ZZ ' + first + ' ' + second + '\n'
        new_circuit.append(new_ZZ)
f = open(new_file, "w")
for node in new_circuit:
    f.write(node)
f.close()