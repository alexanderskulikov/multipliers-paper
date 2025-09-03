from cirbo.core.circuit import Circuit
from cirbo.synthesis.generation.arithmetics.summation import add_sum_n_bits, add_sum_n_bits_easy

# rng = (7, 15, 31, 63, 127, 255, 511, 1023, 2047)
rng = [2 ** k - 1 for k in range(3, 18, 2)]
s1, s2 = [], []

print('\\toprule')
print('$n$ &', ' & '.join(map(str, rng)), '\\\\')
print('\\midrule')

print('FA ', end='')
for n in rng:
    ckt = Circuit.bare_circuit(input_size=n)
    add_sum_n_bits_easy(ckt, ckt.inputs)
    s1.append(ckt.gates_number())
    print('&', ckt.gates_number(), end=' ')
print('\\\\')

print('MDFA ', end='')
for n in rng:
    ckt = Circuit.bare_circuit(input_size=n)
    add_sum_n_bits(ckt, ckt.inputs)
    s2.append(ckt.gates_number())
    print('&', ckt.gates_number(), end=' ')
print('\\\\')

print('Improvement ', end='')
for k in range(len(s1)):
    i = (s1[k] - s2[k]) / s1[k] * 100
    print(f' & {i:.1f}\\%', end=' ')

print('\\\\ \n\\bottomrule')