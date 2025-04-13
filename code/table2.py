from cirbo.core.circuit import Circuit
from cirbo.synthesis.generation.arithmetics.summation import add_sum_n_bits, add_sum_n_bits_easy
import sys
import matplotlib.pyplot as plt
from cirbo.core import Gate
from cirbo.core.circuit import Circuit, INPUT
from cirbo.synthesis.generation.arithmetics import add_mul_karatsuba
from cirbo.synthesis.generation.arithmetics.multiplication import add_simple_karatsuba, add_dadda_karatsuba, \
    add_mul_our_karatsuba, add_mul_dadda
from cirbo.synthesis.generation.arithmetics.summation \
import add_sum_n_bits_easy, add_sum_n_bits, generate_add_weighted_bits_efficient, generate_add_weighted_bits_naive

rng = [20 * k for k in range(2, 16)]

print('\\toprule')
print('$n$ &', ' & '.join(map(str, rng)), '\\\\')
print('\\midrule')

print('Dadda ', end='')
for n in rng:
    ckt_dadda = Circuit.bare_circuit(input_size=2 * n)
    add_mul_dadda(ckt_dadda, ckt_dadda.inputs[:n], ckt_dadda.inputs[:n])
    print('&', ckt_dadda.gates_number(), end=' ')
print('\\\\')

print('MDFA ', end='')
for n in rng:
    ckt_mult_efficient = generate_add_weighted_bits_efficient([i + j for i in range(n) for j in range(n)])
    print('&', ckt_mult_efficient.gates_number() + n ** 2, end=' ')
print('\\\\')

print('Karatsuba ', end='')
for n in rng:
    input_labels_a = [f"a{i}" for i in range(n)]
    input_labels_b = [f"b{i}" for i in range(n)]
    ckt_simple_karatsuba = Circuit()
    for i in input_labels_a:
        ckt_simple_karatsuba.add_gate(Gate(i, INPUT))
    for i in input_labels_b:
        ckt_simple_karatsuba.add_gate(Gate(i, INPUT))
    res = add_simple_karatsuba(ckt_simple_karatsuba, input_labels_a, input_labels_b)
    ckt_simple_karatsuba.set_outputs(res)
    print('&', ckt_simple_karatsuba.gates_number(), end=' ')
print('\\\\')

print('Karatsuba, Dadda', end='')
for n in rng:
    input_labels_a = [f"a{i}" for i in range(n)]
    input_labels_b = [f"b{i}" for i in range(n)]
    ckt_dadda_karatsuba = Circuit()
    for i in input_labels_a:
        ckt_dadda_karatsuba.add_gate(Gate(i, INPUT))
    for i in input_labels_b:
        ckt_dadda_karatsuba.add_gate(Gate(i, INPUT))
    res = add_dadda_karatsuba(ckt_dadda_karatsuba, input_labels_a, input_labels_b)
    print('&', ckt_dadda_karatsuba.gates_number(), end=' ')
print('\\\\')

print('Karatsuba, MDFA', end='')
for n in rng:
    input_labels_a = [f"a{i}" for i in range(n)]
    input_labels_b = [f"b{i}" for i in range(n)]
    ckt_our_karatsuba = Circuit()
    for i in input_labels_a:
        ckt_our_karatsuba.add_gate(Gate(i, INPUT))
    for i in input_labels_b:
        ckt_our_karatsuba.add_gate(Gate(i, INPUT))
    res = add_mul_our_karatsuba(ckt_our_karatsuba, input_labels_a, input_labels_b)
    print('&', ckt_our_karatsuba.gates_number(), end=' ')
print('\\\\')

print('\\bottomrule')