import sys
import matplotlib.pyplot as plt
from cirbo.core import Gate
from cirbo.core.circuit import Circuit, INPUT
from cirbo.synthesis.generation.arithmetics import add_mul_karatsuba
from cirbo.synthesis.generation.arithmetics.multiplication import add_simple_karatsuba, add_dadda_karatsuba, \
    add_mul_karatsuba_with_efficient_sum, add_mul_dadda
from cirbo.synthesis.generation.arithmetics.summation \
import add_sum_n_bits_easy, add_sum_n_bits, generate_sum_weighted_bits_efficient, generate_sum_weighted_bits_naive
sys.setrecursionlimit(150000)


# n = 15
#
# ckt_sum_naive = generate_add_weighted_bits_naive([0] * n)
# print(f'Naive circuit for SUM{n}: {ckt_sum_naive.gates_number()}')
#
#
# ckt_sum_efficient = generate_add_weighted_bits_efficient([0] * n)
# print(f'Efficient circuit for SUM{n}: {ckt_sum_efficient.gates_number()}')
#
#
# ckt_add = generate_add_weighted_bits_efficient(list(range(n)) + list(range(n)))
# print(f'(Optimal) addition of two {n}-bit numbers: {ckt_add.gates_number()}')
#
#
# ckt_mult_efficient = generate_add_weighted_bits_efficient([i + j for i in range(n) for j in range(n)])
# print(f'Efficient circuit for multiplication of two {n}-bit numbers: {ckt_mult_efficient.gates_number()}')
#
# # Misha TODO: rewrite the following line using the new naive method -> DONE
# ckt_mult_naive = generate_add_weighted_bits_naive([i + j for i in range(n) for j in range(n)])
# print(f'Naive circuit for multiplication of two {n}-bit numbers: {ckt_mult_naive.gates_number()}')


# r = list(range(40, 101, 10))
r = list(range(40, 301, 10))
dadda_sizes = []
mdfa_sizes = []
karatsuba_sizes = []
karatsuba_dadda_sizes = []
karatsuba_mdfa_sizes = []

for n in r:
    ckt_dadda = Circuit.bare_circuit(input_size=2 * n)
    add_mul_dadda(ckt_dadda, ckt_dadda.inputs[:n], ckt_dadda.inputs[:n])
    dadda_sizes.append(ckt_dadda.gates_number())

    ckt_mult_efficient = generate_sum_weighted_bits_efficient([i + j for i in range(n) for j in range(n)])
    mdfa_sizes.append(ckt_mult_efficient.gates_number())

    input_labels_a = [f"a{i}" for i in range(n)]
    input_labels_b = [f"b{i}" for i in range(n)]
    ckt_simple_karatsuba = Circuit()
    ckt_dadda_karatsuba = Circuit()
    ckt_pow2_m1_karatsuba = Circuit()
    ckt_our_karatsuba = Circuit()


    for i in input_labels_a:
        ckt_simple_karatsuba.add_gate(Gate(i, INPUT))
    for i in input_labels_b:
        ckt_simple_karatsuba.add_gate(Gate(i, INPUT))

    for i in input_labels_a:
        ckt_dadda_karatsuba.add_gate(Gate(i, INPUT))
    for i in input_labels_b:
        ckt_dadda_karatsuba.add_gate(Gate(i, INPUT))

    for i in input_labels_a:
        ckt_pow2_m1_karatsuba.add_gate(Gate(i, INPUT))
    for i in input_labels_b:
        ckt_pow2_m1_karatsuba.add_gate(Gate(i, INPUT))

    for i in input_labels_a:
        ckt_our_karatsuba.add_gate(Gate(i, INPUT))
    for i in input_labels_b:
        ckt_our_karatsuba.add_gate(Gate(i, INPUT))

    res = add_simple_karatsuba(ckt_simple_karatsuba, input_labels_a, input_labels_b)
    ckt_simple_karatsuba.set_outputs(res)

    res = add_dadda_karatsuba(ckt_dadda_karatsuba, input_labels_a, input_labels_b)
    ckt_dadda_karatsuba.set_outputs(res)

    res = add_mul_karatsuba(ckt_pow2_m1_karatsuba, input_labels_a, input_labels_b)
    ckt_pow2_m1_karatsuba.set_outputs(res)

    res = add_mul_karatsuba_with_efficient_sum(ckt_our_karatsuba, input_labels_a, input_labels_b)
    ckt_our_karatsuba.set_outputs(res)

    karatsuba_sizes.append(ckt_simple_karatsuba.gates_number())
    karatsuba_dadda_sizes.append(ckt_dadda_karatsuba.gates_number())
    karatsuba_mdfa_sizes.append(ckt_our_karatsuba.gates_number())

    print(f'n={n:3}: dadda={ckt_dadda.gates_number():8}, '
          f'mult_efficient={ckt_mult_efficient.gates_number() + n ** 2:8}, '
          f'karatsuba={ckt_simple_karatsuba.gates_number():8}, '
          f'karatsuba+dadda={ckt_dadda_karatsuba.gates_number():8}, '
          f'karatsuba+mdfa={ckt_our_karatsuba.gates_number():8}'
          )

plt.figure(figsize=(16, 10))

plt.plot(r, dadda_sizes, marker='.', linestyle='--', color='b', label='Dadda')
plt.plot(r, mdfa_sizes, marker='.', linestyle='--', color='g', label='MDFA')
plt.plot(r, karatsuba_sizes, marker='.', linestyle='--', color='r', label='Karatsuba')
plt.plot(r, karatsuba_dadda_sizes, marker='.', linestyle='--', color='c', label='Karatsuba+Dadda')
plt.plot(r, karatsuba_mdfa_sizes, marker='.', linestyle='--', color='m', label='Karatsuba+MDFA')


plt.grid(True, linestyle='--', alpha=0.7)
# plt.legend(prop={'size': 20})
plt.legend()
plt.tight_layout()
plt.show()
