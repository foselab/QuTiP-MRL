#optimization
import numpy as np
import qutip as qt
from qutip_mrl.qudit_circuit import QuditCircuit

d = 3

qc = QuditCircuit(4, d)



qc.shift("+2", 1)
qc.shift("+1", 2)

qc.barrier()

qc.ms("+1", 1, 0)
qc.shift("+1", 1)

qc.ms("+1", 1, 0)
qc.shift("+1", 1)

qc.ms("+1", 1, 0)
qc.shift("+1", 1)

qc.ms("+1", 2, 0)
qc.shift("+1", 1)

qc.ms("+1", 2, 0)
qc.ms("+2", 2, 0)
qc.shift("+2", 1)

qc.ms("+2", 2, 0)
qc.toffoli("+2", 0, 2, 3, [1, 2])
qc.shift("+1", 1)
qc.toffoli("+2", 0, 2, 3, [1, 2])


print("\nMatplotlib diagram (original):")
qc.draw("mpl")

print("\nState probabilities (original):")
qc.simulate_einsum()

qc_opt = qc.optimize()

print("\nASCII diagram (optimized):")
qc_opt.draw()

print("\nMatplotlib diagram (optimized):")
qc_opt.draw("mpl")



print("\nState probabilities (optimized):")
qc_opt.simulate_einsum()
