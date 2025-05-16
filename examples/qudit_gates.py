from qudit_circuit import QuditCircuit
import numpy as np

example = QuditCircuit(num_qudit=3,num_states=4)

user_matrix = np.array([ 
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0]
])

example.custom_gate(gate=user_matrix,target=1,name='EX.')

example.c_custom_gate(gate=user_matrix,control=2,target=0,name='EX.')

example.draw()

'''
OUTPUT:  

                      +-----+  
Q0   -----------------| EX. |--
                      +-----+  
           +-----+       |     
Q1   ------| EX. |-------|-----
           +-----+       |     
                         |     
Q2   --------------------O-----
'''


