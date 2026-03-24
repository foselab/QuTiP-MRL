#quaternary Half adder
import numpy as np
from qutip_mrl.qudit_circuit import QuditCircuit

d = 4
qc = QuditCircuit(3, d)

qc.shift("+1", 0)
qc.shift("+2", 1)

qc.barrier()
qc.toffoli("+1", 0, 1, 2, [1, 3])
qc.toffoli("+1", 0, 1, 2, [2, 2])
qc.toffoli("+1", 0, 1, 2, [2, 3])
qc.toffoli("+1", 0, 1, 2, [3, 1])
qc.toffoli("+1", 0, 1, 2, [3, 2])
qc.toffoli("+1", 0, 1, 2, [3, 3])

qc.feynman(0, 1)

qc.draw()

print("\nMatplotlib diagram:")
qc.draw("mpl")

print("\nState probabilities for each qudit (starting from |000>):")
qc.simulate_einsum()

qc.simulate_fullmatrix()

