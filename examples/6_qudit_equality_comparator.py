equality = QuditCircuit(3,4) # Circuit with 3 qudit of basis 4

# The circuit requires the manual insertion of following matrices 

zero_three_one = np.array([
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [1, 0, 0, 0]
])

zero_three_two = np.array([
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 0]
])

one_three_two = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 1, 0, 0]
])

zero_two_three_one = np.array([
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 0],
    [0, 0, 1, 0]
])

plus3 = np.array([
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0]
])

# Q0 and Q1 are input states, they are both in state 0
# The Equality Comparator will set Q2 to state 3 if input are in the same state, 0 otherwise

equality.barrier()

equality.custom_gate(zero_three_one,0,'031')
equality.c_custom_gate(zero_three_one,0,1,'031')
equality.custom_gate(zero_three_two,0,'032')
equality.c_custom_gate(one_three_two,0,1,'132')
equality.custom_gate(zero_three_one,0,'031')

equality.c_custom_gate(zero_two_three_one,0,1,'0231')
equality.c_custom_gate(plus3,1,2,'+3')

equality.draw()

'''
OUTPUT:

           +-----+               +-----+               +-----+                        
Q0   ------| 031 |-------O-------| 032 |-------O-------| 031 |-------O----------------
           +-----+       |       +-----+       |       +-----+       |                
                      +-----+               +-----+               +-----+             
Q1   -----------------| 031 |---------------| 132 |---------------|0231 |-------O-----
                      +-----+               +-----+               +-----+       |     
                                                                             +-----+  
Q2   ------------------------------------------------------------------------| +3  |--
                                                                             +-----+
'''

equality.simulate_einsum()

'''
OUTPUT:
                                      
QUDIT 0 state probabilities:
  1
  0
  0
  0
QUDIT 1 state probabilities:
  0
  0
  0
  1
QUDIT 2 state probabilities:
  0
  0
  0
  1
'''



