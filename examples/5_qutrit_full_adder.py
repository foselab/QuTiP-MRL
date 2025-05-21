from qudit_circuit import QuditCircuit

full_adder = QuditCircuit(4) # Circuit initialization, 4 qutrits

# As in Qiskit qutrit are all in state 0 at the beginning
# Therefore we add a +2 gate to Q0 and Q1 (the 2 inputs) while testing the circuit
# Q0 and Q1 will be in state, after the circuit execution Q1 will contain the sum while Q1 won't change
# Q2 is the Cin in this case will be in state 0 and won't change after execution
# Q3 will contain the Cout and is initially in state 0
full_adder.plus2(0)
full_adder.plus2(1)

full_adder.barrier() # Barrier added for clearer visualization

# Actual full adder qutrit circuit
full_adder.c_plus2(1,0)
full_adder.c_one_two(0,1)
full_adder.c_plus1(1,3)
full_adder.c_one_two(0,1)
full_adder.plus1(1)
full_adder.c_plus1(1,0)
full_adder.plus2(1)
full_adder.c_plus2(2,0)
full_adder.c_one_two(0,2)
full_adder.c_plus1(2,3)
full_adder.c_one_two(0,2)
full_adder.plus1(2)
full_adder.c_plus1(2,0)
full_adder.plus2(2)

full_adder.draw()

'''
OUTPUT:

           +-----+                 |||      +-----+                                                +-----+               +-----+                                                +-----+             
Q0   ------| + 2 |-----------------|||------| + 2 |-------O---------------------O------------------| + 1 |---------------| + 2 |-------O---------------------O------------------| + 1 |-------------
           +-----+                 |||      +-----+       |                     |                  +-----+               +-----+       |                     |                  +-----+             
                      +-----+      |||         |       +-----+               +-----+    +-----+       |       +-----+       |          |                     |                     |                
Q1   -----------------| + 2 |------|||---------O-------| 1 2 |-------O-------| 1 2 |----| + 1 |-------O-------| + 2 |-------|----------|---------------------|---------------------|----------------
                      +-----+      |||                 +-----+       |       +-----+    +-----+               +-----+       |          |                     |                     |                
                                   |||                               |                                                      |       +-----+               +-----+    +-----+       |       +-----+  
Q2   ------------------------------|||-------------------------------|------------------------------------------------------O-------| 1 2 |-------O-------| 1 2 |----| + 1 |-------O-------| + 2 |--
                                   |||                               |                                                              +-----+       |       +-----+    +-----+               +-----+  
                                   |||                            +-----+                                                                      +-----+                                              
Q3   ------------------------------|||----------------------------| + 1 |----------------------------------------------------------------------| + 1 |----------------------------------------------
                                   |||                            +-----+                                                                      +-----+                                             
'''

full_adder.simulate_einsum()

'''
OUTPUT:
                                      
QUDIT 0 state probabilities:
  0
  1
  0
QUDIT 1 state probabilities:
  0
  0
  1
QUDIT 2 state probabilities:
  1
  0
  0
QUDIT 3 state probabilities:
  0
  1
  0
'''
