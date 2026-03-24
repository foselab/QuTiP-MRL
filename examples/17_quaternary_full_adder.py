#quaternary full adder
import numpy as np
from qutip_mrl.qudit_circuit import QuditCircuit

d = 4
qc = QuditCircuit(4, d)

qc.shift("+1", 0)
qc.shift("+1", 1)
qc.shift("+1", 2)


qc.barrier()
qc.toffoli("+1", 0, 1, 3, [1, 3])
qc.toffoli("+1", 0, 1, 3, [2, 2])
qc.toffoli("+1", 0, 1, 3, [2, 3])
qc.toffoli("+1", 0, 1, 3, [3, 1])
qc.toffoli("+1", 0, 1, 3, [3, 2])
qc.toffoli("+1", 0, 1, 3, [3, 3])

qc.feynman(0, 1)


qc.toffoli("+1", 1, 2, 3, [1, 3])
qc.toffoli("+1", 1, 2, 3, [2, 2])
qc.toffoli("+1", 1, 2, 3, [2, 3])
qc.toffoli("+1", 1, 2, 3, [3, 1])
qc.toffoli("+1", 1, 2, 3, [3, 2])
qc.toffoli("+1", 1, 2, 3, [3, 3])

qc.feynman(1, 2)


print("\nMatplotlib diagram:")
qc.draw("mpl")

print("\nState probabilities for each qudit (starting from |00000>):")
qc.simulate_einsum()

qc.simulate_fullmatrix()