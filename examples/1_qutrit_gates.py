from qutip_mrl.qudit_circuit import QuditCircuit

example = QuditCircuit(num_qudit=3) 

example.plus1(target=1) # The 'plus1' qutrit gate is already in the library and there is no need for the user manual insertion of the matrix

example.c_zero_one(control=0,target=1)

example.draw()

'''
OUTPUT:  

Q0   --------------------O-----
                         |     
           +-----+    +-----+  
Q1   ------| + 1 |----| 0 1 |--
           +-----+    +-----+  
                             
Q2   --------------------------
'''


