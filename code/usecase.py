from cirbo.synthesis.generation.arithmetics.summation import generate_add_weighted_bits_efficient as generate

for n in range(2, 100):
    ckt = generate(list(range(n)) + list(range(n)))
    assert ckt.gates_number() == 5 * n - 3