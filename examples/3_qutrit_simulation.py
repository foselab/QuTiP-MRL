from qudit_circuit import QuditCircuit

example = QuditCircuit(num_qudit=3)

example.plus1(target=1)
example.plus2(target=0)
example.c_zero_two(control=0,target=2)
example.plus1(target=0)

example.draw()

'''
OUTPUT:
                      +-----+               +-----+  
Q0   -----------------| + 2 |-------O-------| + 1 |--
                      +-----+       |       +-----+  
           +-----+                  |                
Q1   ------| + 1 |------------------|----------------
           +-----+                  |                
                                 +-----+             
Q2   ----------------------------| 0 2 |-------------
                                 +-----+             
'''

example.simulate_einsum()

'''
OUTPUT:

QUDIT 0 state probabilities:
  1
  0
  0
QUDIT 1 state probabilities:
  0
  1
  0
QUDIT 2 state probabilities:
  0
  0
  1
'''

example.simulate_fullmatrix()

'''
OUTPUT:

QUDIT 0 Density Matrix:
Quantum object: dims=[[3], [3]], shape=(3, 3), type='oper', dtype=Dense, isherm=True
Qobj data =
[[1. 0. 0.]
 [0. 0. 0.]
 [0. 0. 0.]]
QUDIT 1 Density Matrix:
Quantum object: dims=[[3], [3]], shape=(3, 3), type='oper', dtype=Dense, isherm=True
Qobj data =
[[0. 0. 0.]
 [0. 1. 0.]
 [0. 0. 0.]]
QUDIT 2 Density Matrix:
Quantum object: dims=[[3], [3]], shape=(3, 3), type='oper', dtype=Dense, isherm=True
Qobj data =
[[0. 0. 0.]
 [0. 0. 0.]
 [0. 0. 1.]]
'''

