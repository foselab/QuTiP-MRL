#optimization
import numpy as np
from qutip_mrl.qudit_circuit import QuditCircuit

d = 3

qc = QuditCircuit(3, d)

qc.shift("+2", 1)
qc.shift("+1", 2)

qc.barrier()

qc.shift("+1", 2)
qc.ms("+1", 1, 0, [2])
qc.toffoli("+2", 0, 1, 2, [1, 2])
qc.toffoli("+2", 0, 1, 2, [1, 2])

print("ASCII diagram (original):")
qc.draw()

print("\nMatplotlib diagram (original):")
qc.draw("mpl")

qc_opt = qc.optimize()

print("\nASCII diagram (optimized):")
qc_opt.draw()

print("\nMatplotlib diagram (optimized):")
qc_opt.draw("mpl")

print("\nState probabilities (original):")
qc.simulate_einsum()

print("\nState probabilities (optimized):")
qc_opt.simulate_einsum()


qc.simulate_statevector()
