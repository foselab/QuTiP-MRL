from qudit_circuit import QuditCircuit

example = QuditCircuit(num_qudit=3) 

example.plus1(target=1)

example.draw()

#OUTPUT:      
              
#  Q0   ---------------
#                      
#             +-----+  
#  Q1   ------| + 1 |--
#             +-----+  
#                      
#  Q2   ---------------

example.c_zero_one(control=0,target=1)

example.draw()

#OUTPUT:  

#  Q0   --------------------O-----
#                           |     
#             +-----+    +-----+  
#  Q1   ------| + 1 |----| 0 1 |--
#             +-----+    +-----+  
#                               
#  Q2   --------------------------
