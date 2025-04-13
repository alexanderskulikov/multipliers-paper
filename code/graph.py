import matplotlib.pyplot as plt
from cirbo.core.circuit.circuit import Circuit
from cirbo.minimization.simplification.remove_redundant_gates import RemoveRedundantGates
from cirbo.synthesis.generation.arithmetics.multiplication import add_mul_pow2_m1, add_mul_dadda
from cirbo.core.circuit.gate import Gate, INPUT
from cirbo.core.circuit import Circuit
from cirbo.synthesis.generation.arithmetics.summation import add_sum_n_bits_easy, add_sum_n_bits

def plot_two_lines(sizes1, sizes2):
    x1 = range(1, len(sizes1) + 1)
    x2 = range(1, len(sizes2) + 1)

    plt.figure(figsize=(16, 10))

    plt.plot(x1, sizes1, marker='o', linestyle='--', color='b', label='Dadda')
    plt.plot(x2, sizes2, marker='s', linestyle='--', color='r', label='Dynamic')

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

def get_sizes(l, r, ckt, funct):
    sizes = []
    for q in range(l, r):
        ckt = Circuit()
        input_labels = [f'x{i}' for i in range(2*q)]
        for i in range(2*q):
            ckt.add_gate(Gate(input_labels[i], INPUT))
        res = funct(ckt, input_labels[:q], input_labels[q:])
        for k in range(len(res)):
            ckt.mark_as_output(res[k])

        simplified = RemoveRedundantGates().transform(ckt)
        sizes.append(len(simplified.gates) - 2*q)
    return sizes

# sizes1 = get_sizes(1, 64, Circuit(), add_mul_dadda)
# sizes2 = get_sizes(1, 64, Circuit(), add_mul_pow2_m1)
# plot_two_lines(sizes1, sizes2)

n = 17
ckt = Circuit()
for i in range(n):
    ckt.add_gate(Gate(f'x{i}', INPUT))
add_sum_n_bits_easy(ckt, ckt.inputs)
print(len(ckt.gates))

