example = QuditCircuit(num_qudit=3,num_states=4)

m1 = np.array([    # Exchanges the Qudit states 0 and 1 (0->1,1->0)
    [0, 1, 0, 0],  # Exchanges the Qudit states 2 and 3 (2->3,3->2)
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
])
m2 = np.array([    # Increases the Qudit state by 2 (0->2,1->3,2->0,3->1) 
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 0],
    [0, 1, 0, 0]
])
m3 = np.array([    # Exchanges the Qudit states 0 and 3 (0->3,3->0)
    [0, 0, 0, 1],  # Exchanges the Qudit states 1 and 2 (1->2,2->1)
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0]
])
m4 = np.array([   # Exchanges the Qudit states 0 and 3 (0->3,3->0)
    [0, 0, 0, 1],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 0]
])

example.custom_gate(gate=m3,target=2,name='M 3')
example.custom_gate(gate=m2,target=0,name='M 2')
example.c_custom_gate(gate=m4,control=2,target=1,name='M 4')
example.custom_gate(gate=m1,target=2,name='M 1')

example.draw()

example.simulate_einsum()


example.simulate_fullmatrix()

