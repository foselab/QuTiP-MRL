from qutip_mrl.qudit_circuit import QuditCircuit

demultiplexer = QuditCircuit(num_qudit=5)

demultiplexer.plus1(target=0)
demultiplexer.c_plus2(control=1, target=3)
demultiplexer.c_one_two(control=0, target=1)
demultiplexer.c_plus1(control=1, target=3)
demultiplexer.c_one_two(control=0, target=1)
demultiplexer.plus1(target=0)
demultiplexer.c_plus2(control=1, target=2)
demultiplexer.c_one_two(control=0, target=1)
demultiplexer.c_plus1(control=1, target=2)
demultiplexer.c_one_two(control=0, target=1)
demultiplexer.plus1(target=0)
demultiplexer.c_plus2(control=1, target=4)
demultiplexer.c_one_two(control=0, target=1)
demultiplexer.c_plus1(control=1, target=4)
demultiplexer.c_one_two(control=0, target=1)

demultiplexer.draw()

'''
OUTPUT:
           +----+                                            +----+                                            +----+                                          
Q0   ------| +1 |----------------O-------------------O-------| +1 |----------------O-------------------O-------| +1 |----------------O-------------------O-----
           +----+                |                   |       +----+                |                   |       +----+                |                   |     
                               +----+              +----+                        +----+              +----+                        +----+              +----+  
Q1   ------------------O-------| 12 |------O-------| 12 |----------------O-------| 12 |------O-------| 12 |----------------O-------| 12 |------O-------| 12 |--
                       |       +----+      |       +----+                |       +----+      |       +----+                |       +----+      |       +----+  
                       |                   |                           +----+              +----+                          |                   |               
Q2   ------------------|-------------------|---------------------------| +2 |--------------| +1 |--------------------------|-------------------|---------------
                       |                   |                           +----+              +----+                          |                   |               
                     +----+              +----+                                                                            |                   |               
Q3   ----------------| +2 |--------------| +1 |----------------------------------------------------------------------------|-------------------|---------------
                     +----+              +----+                                                                            |                   |               
                                                                                                                         +----+              +----+            
Q4   --------------------------------------------------------------------------------------------------------------------| +2 |--------------| +1 |------------
                                                                                                                         +----+              +----+            
'''

demultiplexer.simulate_einsum()

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

demultiplexer.simulate_fullmatrix()

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

