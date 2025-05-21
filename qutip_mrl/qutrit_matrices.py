import numpy as np

Z_I = np.array([ # Identity matrix does nothing to the Qutrit
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])

Z_PLUS_1 = np.array([ # Increases the Qutrit state by 1 (0->1,1->2,2->0) 
    [0, 0, 1],
    [1, 0, 0],
    [0, 1, 0]
])

Z_PLUS_2 = np.array([ # Increases the Qutrit state by 2 (0->2,1->0,2->1) 
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
])

Z_12 = np.array([ # Exchanges the Qutrit states 1 and 2 (1->2,2->1), if The qutrit is in state 0 it does nothing
    [1, 0, 0],
    [0, 0, 1],
    [0, 1, 0]
])

Z_01 = np.array([ # Exchanges the Qutrit states 0 and 1 (0->1,1->0), if The qutrit is in state 2 it does nothing
    [0, 1, 0],
    [1, 0, 0],
    [0, 0, 1]
])

Z_02 = np.array([ # Exchanges the Qutrit states 0 and 2 (0->2,2->0), if The qutrit is in state 1 it does nothing 
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0]
])
