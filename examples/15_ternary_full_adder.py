#ternary full adder
import numpy as np
from qutip_mrl.qudit_circuit import QuditCircuit

d = 3
qc = QuditCircuit(5, d)

qc.shift("+1", 0)
qc.shift("+1", 1)
qc.shift("+1", 3)


qc.barrier()
qc.toffoli("+1", 0, 1, 2, [1, 2])
qc.toffoli("+1", 0, 1, 2, [2, 1])
qc.toffoli("+1", 0, 1, 2, [2, 2])
qc.feynman(0, 1)

qc.toffoli("+1", 1, 3, 4, [1, 2])
qc.toffoli("+1", 1, 3, 4, [2, 1])
qc.toffoli("+1", 1, 3, 4, [2, 2])
qc.feynman(2, 4)

qc.feynman(3, 1)


qc.draw()

print("\nMatplotlib diagram:")
qc.draw("mpl")

print("\nState probabilities for each qudit (starting from |000>):")
qc.simulate_einsum()

qc.simulate_fullmatrix()
