from qutip_mrl.qudit_circuit import QuditCircuit

multiplexer = QuditCircuit(num_qudit=5)

multiplexer.plus1(target=0)
multiplexer.c_plus2(control=2, target=4)
multiplexer.c_one_two(control=0, target=2)
multiplexer.c_plus1(control=2, target=4)
multiplexer.c_one_two(control=0, target=2)
multiplexer.plus1(target=0)
multiplexer.c_plus2(control=1, target=4)
multiplexer.c_one_two(control=0, target=1)
multiplexer.c_plus1(control=1, target=4)
multiplexer.c_one_two(control=0, target=1)
multiplexer.plus1(target=0)
multiplexer.c_plus2(control=3, target=4)
multiplexer.c_one_two(control=0, target=3)
multiplexer.c_plus1(control=3, target=4)
multiplexer.c_one_two(control=0, target=3)

multiplexer.draw()

'''
OUTPUT:
           +----+                                            +----+                                            +----+                                          
Q0   ------| +1 |----------------O-------------------O-------| +1 |----------------O-------------------O-------| +1 |----------------O-------------------O-----
           +----+                |                   |       +----+                |                   |       +----+                |                   |     
                                 |                   |                           +----+              +----+                          |                   |     
Q1   ----------------------------|-------------------|-------------------O-------| 12 |------O-------| 12 |--------------------------|-------------------|-----
                                 |                   |                   |       +----+      |       +----+                          |                   |     
                               +----+              +----+                |                   |                                       |                   |     
Q2   ------------------O-------| 12 |------O-------| 12 |----------------|-------------------|---------------------------------------|-------------------|-----
                       |       +----+      |       +----+                |                   |                                       |                   |     
                       |                   |                             |                   |                                     +----+              +----+  
Q3   ------------------|-------------------|-----------------------------|-------------------|-----------------------------O-------| 12 |------O-------| 12 |--
                       |                   |                             |                   |                             |       +----+      |       +----+  
                     +----+              +----+                        +----+              +----+                        +----+              +----+            
Q4   ----------------| +2 |--------------| +1 |------------------------| +2 |--------------| +1 |------------------------| +2 |--------------| +1 |------------
                     +----+              +----+                        +----+              +----+                        +----+              +----+            
'''

multiplexer.simulate_einsum()

'''
OUTPUT:

QUDIT 0 state probabilities:
  1
  0
  0
QUDIT 1 state probabilities:
  1
  0
  0
QUDIT 2 state probabilities:
  1
  0
  0
QUDIT 3 state probabilities:
  1
  0
  0
QUDIT 4 state probabilities:
  1
  0
  0
'''

multiplexer.simulate_fullmatrix()

'''
OUTPUT:

QUDIT 0 Density Matrix:
[[1.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j]]
QUDIT 1 Density Matrix:
[[1.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j]]
QUDIT 2 Density Matrix:
[[1.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j]]
QUDIT 3 Density Matrix:
[[1.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j]]
QUDIT 4 Density Matrix:
[[1.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j]
 [0.+0.j 0.+0.j 0.+0.j]]
'''

