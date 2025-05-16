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

example.simulate_fullmatrix()

