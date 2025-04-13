import sys
from cirbo.core import Gate
from cirbo.core.circuit import Circuit, INPUT
from cirbo.synthesis.generation.arithmetics import add_mul_karatsuba
from cirbo.synthesis.generation.arithmetics.multiplication import add_simple_karatsuba, add_dadda_karatsuba, \
    add_mul_our_karatsuba
from cirbo.synthesis.generation.arithmetics.summation \
import add_sum_n_bits_easy, add_sum_n_bits, generate_add_weighted_bits_efficient, generate_add_weighted_bits_naive
sys.setrecursionlimit(150000)


for n in range(64, 65):
    ckt_dadda = Circuit.bare_circuit(input_size=2 * n)
    add_mul_dadda(ckt_dadda, ckt_dadda.inputs[:n], ckt_dadda.inputs[:n])

    ckt_mul_pow2 = Circuit.bare_circuit(input_size=2 * n)
    add_mul_pow2_m1(ckt_mul_pow2, ckt_mul_pow2.inputs[:n], ckt_mul_pow2.inputs[:n])

    ckt_mult_efficient = generate_add_weighted_bits_efficient([i + j for i in range(n) for j in range(n)])

    ckt_mul_kar = Circuit.bare_circuit(input_size=2 * n)
    add_mul_karatsuba(ckt_mul_kar, ckt_mul_kar.inputs[:n], ckt_mul_kar.inputs[:n])

    # print(n, ckt_dadda.gates_number(), ckt_mul_pow2.gates_number(), ckt_mult_efficient.gates_number() + n ** 2, ckt_mul_kar.gates_number())

    print(f'n={n:3}: dadda={ckt_dadda.gates_number():6}, '
          f'mul_pow2={ckt_mul_pow2.gates_number():6}, '
          f'mult_efficient={ckt_mult_efficient.gates_number() + n ** 2:6}, '
          f'karatsuba={ckt_mul_kar.gates_number():6}')
