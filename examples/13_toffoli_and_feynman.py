#visualization
import numpy as np
from qutip_mrl.qudit_circuit import QuditCircuit

d = 3
qc = QuditCircuit(3, d)


qc.shift("+2", 0)
qc.barrier()
qc.shift("+2", 1)
qc.ms("+2", 1, 2)
qc.feynman(1, 2)
qc.toffoli("+2", 0, 1, 2, [2, 2])


qc.draw()
qc.draw("mpl")

print("\nState probabilities (original):")
qc.simulate_einsum()

qc.simulate_fullmatrix()
