from math import ceil
import matplotlib.pyplot as plt
import numpy as np
import qutip as qt

import qutip_mrl.qutrit_matrices as qutrit_matrices
import qutip_mrl.ascii_gates as ascii_gates


class QuditCircuit:

    """
    Core of the library, a class to create and manage a quantum circuit composed of qudits with any number of basis states.

    Each qudit can have an arbitrary number of basis states (default is 3, qutrits).
    The circuit supports adding qutrit gates using built-in matrices or any qudit gate providing a numpy.array matrix.
    It also supports einsum and full matrix simulation and offers ASCII and matplotlib-based visualizations.

    Attributes:
        num_qudit (int): Number of qudits in the circuit.
        num_states (int): Number of basis states per qudit (default: 3).

    Example:
        qc = QuditCircuit(6)           # Creates a circuit with 6 QUTRIT
        qc = QuditCircuit(5,4)         # Creates a circuit with 5 QUDITS, each having 4 basis states
    """

    def __init__(self, num_qudit: int, num_states: int=3):
        """
        Initialize a QuditCircuit with the given number of qudits and basis states.

        Args:
            num_qudit (int): Number of qudits in the circuit.
            num_states (int, optional): Number of basis states per qudit. Default is 3 (qutrits).
        """    
        self.num_qudit = num_qudit
        self.num_states = num_states
        # Structures for simulation and visualization
        self.__einsum_gates = []
        self.__fullmatrix_gates = []
        self.__ascii_circuit_visualization_list = []
        self.__mpl_circuit_visualization_list = []
        self.__initial_ASCII_block()

    # Functions called by the user to insert a gate in the circuit
    def id(self, target):
        """
        Apply the qutrit identity gate to the specified target qudit.

        Args:
            target (int): Index of the target qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """
        if self.num_states> 3: # Warns the user that he is trying to insert qutrit gates in a qudit circuit with basis states greater than 3
         raise ValueError(f"Trying to insert a Qutrit gate in a >3-states qudit circuit")  
        # Appends the gate and the target in both the einsum and fullmatrix lists that will be used when circuit is simulated
        self.__einsum_gates.append((qutrit_matrices.Z_I,target))
        self.__fullmatrix_gates.append((qt.Qobj(qutrit_matrices.Z_I), target))
        
        # Code used for the ASCII visual representation,
        self.__simple_gate_ASCII_block(ascii_gates.ID_ASCII, target)
        # Code used for the Matplotlib visual representation, generates the gate's info and adds them in a list
        gate_data = {'name': 'I', 'target': target, 'color': 'lightblue', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)   

    def plus1(self, target):
        """
        Apply the qutrit +1 gate to the specified target qudit.
        The gate increases the Qutrit state by 1.

        Args:
            target (int): Index of the target qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """        
        if self.num_states> 3:
         raise ValueError(f"Trying to insert a Qutrit gate in a >3 states qudit circuit")          
        self.__einsum_gates.append((qutrit_matrices.Z_PLUS_1,target))
        self.__fullmatrix_gates.append((qt.Qobj(qutrit_matrices.Z_PLUS_1), target))
        
        self.__simple_gate_ASCII_block(ascii_gates.PLUS1_ASCII, target)
        gate_data = {'name': '+1', 'target': target, 'color': '#2a9d8f', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)          
            
    def plus2(self, target):
        """
        Apply the qutrit +2 gate to the specified target qudit.
        The gate increases the Qutrit state by 2.

        Args:
            target (int): Index of the target qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """        
        if self.num_states> 3:
         raise ValueError(f"Trying to insert a Qutrit gate in a >3 states qudit circuit")      
        self.__einsum_gates.append((qutrit_matrices.Z_PLUS_2,target))
        self.__fullmatrix_gates.append((qt.Qobj(qutrit_matrices.Z_PLUS_2), target))
        
        self.__simple_gate_ASCII_block(ascii_gates.PLUS2_ASCII, target)
        gate_data = {'name': '+2', 'target': target, 'color': '#0081a7', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)
        
    def one_two(self, target):
        """
        Apply the qutrit 12 gate to the specified target qudit.
        The gate exchanges the Qutrit states 1 and 2 (1->2,2->1), if The qutrit is in state 0 it does nothing.

        Args:
            target (int): Index of the target qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """            
        if self.num_states> 3:
         raise ValueError(f"Trying to insert a Qutrit gate in a >3 states qudit circuit")          
        self.__einsum_gates.append((qutrit_matrices.Z_12,target))
        self.__fullmatrix_gates.append((qt.Qobj(qutrit_matrices.Z_12), target))
        
        self.__simple_gate_ASCII_block(ascii_gates.ONE_TWO_ASCII, target)
        gate_data = {'name': '12', 'target': target, 'color': '#e76f51', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)  

    def zero_one(self, target):
        """
        Apply the qutrit 01 gate to the specified target qudit.
        The gate exchanges the Qutrit states 0 and 1 (0->1,1->0), if The qutrit is in state 2 it does nothing.

        Args:
            target (int): Index of the target qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """           
        if self.num_states> 3:
         raise ValueError(f"Trying to insert a Qutrit gate in a >3 states qudit circuit")              
        self.__einsum_gates.append((qutrit_matrices.Z_01,target))
        self.__fullmatrix_gates.append((qt.Qobj(qutrit_matrices.Z_01), target))
        
        self.__simple_gate_ASCII_block(ascii_gates.ZERO_ONE_ASCII, target)
        gate_data = {'name': '01', 'target': target, 'color': '#e9c46a', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)  

    def zero_two(self, target):
        """
        Apply the qutrit 02 gate to the specified target qudit.
        The gate exchanges the Qutrit states 0 and 2 (0->2,2->0), if The qutrit is in state 1 it does nothing.

        Args:
            target (int): Index of the target qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """            
        if self.num_states> 3:
         raise ValueError(f"Trying to insert a Qutrit gate in a >3 states qudit circuit")              
        self.__einsum_gates.append((qutrit_matrices.Z_02,target))
        self.__fullmatrix_gates.append((qt.Qobj(qutrit_matrices.Z_02), target))
        
        self.__simple_gate_ASCII_block(ascii_gates.ZERO_TWO_ASCII, target)
        gate_data = {'name': '02', 'target': target, 'color': '#f4a261', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)  
        
    def c_plus1(self, control, target):
        """
        If the control is in state |2⟩ apply qutrit gate +1 to the target qudit.

        Args:
            control (int): Index of the control qudit.
            target (int): Index of the target qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """    
        
        if self.num_states> 3:
         raise ValueError(f"Trying to insert a Qutrit gate in a >3 states qudit circuit")              
        self.__einsum_gates.append((qutrit_matrices.Z_PLUS_1,control,target))
        self.__fullmatrix_gates.append((qt.Qobj(qutrit_matrices.Z_PLUS_1), control, target))
        
        self.__controlled_gate_ASCII_block(ascii_gates.PLUS1_ASCII, control, target)
        gate_data = {'name': '+1', 'control': control, 'target': target, 'color': '#2a9d8f', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)   
        
    def c_plus2(self, control, target):
        """
        If the control is in state |2⟩ apply qutrit gate +2 to the target qudit.

        Args:
            control (int): Index of the control qudit.
            target (int): Index of the target qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """            
        if self.num_states> 3:
         raise ValueError(f"Trying to insert a Qutrit gate in a >3 states qudit circuit")              
        self.__einsum_gates.append((qutrit_matrices.Z_PLUS_2,control,target))
        self.__fullmatrix_gates.append((qt.Qobj(qutrit_matrices.Z_PLUS_2), control, target))
        
        self.__controlled_gate_ASCII_block(ascii_gates.PLUS2_ASCII, control, target)
        gate_data = {'name': '+2', 'control': control, 'target': target, 'color': '#0081a7', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)       

    def c_feynman_2(self, A, B, C):
        """
        It applies a ternary controlled feynman gate

        Args:
            A (int): Index of the A qudit.
            B (int): Index of the B qudit.
            C (int): Index of the C qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """            
        if self.num_states> 3:
         raise ValueError(f"Trying to insert a Qutrit gate in a >3 states qudit circuit")  
        self.c_plus2(B, C)
        self.c_one_two(A, B)
        self.c_plus1(B, C)
        self.c_one_two(A, B)          

    def c_one_two(self, control, target):
        """
        If the control is in state |2⟩ apply qutrit gate 12 to the target qudit.

        Args:
            control (int): Index of the control qudit.
            target (int): Index of the target qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """          
        if self.num_states> 3:
         raise ValueError(f"Trying to insert a Qutrit gate in a >3 states qudit circuit")              
        self.__einsum_gates.append((qutrit_matrices.Z_12,control,target))
        self.__fullmatrix_gates.append((qt.Qobj(qutrit_matrices.Z_12), control, target))
        
        self.__controlled_gate_ASCII_block(ascii_gates.ONE_TWO_ASCII, control, target)
        gate_data = {'name': '12', 'control': control, 'target': target, 'color': '#e76f51', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)   

    def c_zero_one(self, control, target):
        """
        If the control is in state |2⟩ apply qutrit gate 01 to the target qudit.

        Args:
            control (int): Index of the control qudit.
            target (int): Index of the target qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """           
        if self.num_states> 3:
         raise ValueError(f"Trying to insert a Qutrit gate in a >3 states qudit circuit")              
        self.__einsum_gates.append((qutrit_matrices.Z_01,control,target))
        self.__fullmatrix_gates.append((qt.Qobj(qutrit_matrices.Z_01), control, target))
        
        self.__controlled_gate_ASCII_block(ascii_gates.ZERO_ONE_ASCII, control, target)
        gate_data = {'name': '01', 'control': control, 'target': target, 'color': '#e9c46a', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)   

    def c_zero_two(self, control, target):
        """
        If the control is in state |2⟩ apply qutrit gate 02 to the target qudit.

        Args:
            control (int): Index of the control qudit.
            target (int): Index of the target qudit.

        Raises:
            ValueError: If the circuit is configured with more than 3 basis states.
        """         
        if self.num_states> 3:
         raise ValueError(f"Trying to insert a Qutrit gate in a >3 states qudit circuit")         
        self.__einsum_gates.append((qutrit_matrices.Z_02,control,target))
        self.__controlled_gate_ASCII_block(ascii_gates.ZERO_TWO_ASCII, control, target)
        self.__fullmatrix_gates.append((qt.Qobj(qutrit_matrices.Z_02), control, target))
        
        gate_data = {'name': '02', 'control': control, 'target': target, 'color': '#f4a261', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data) 
        
    # Barrier used only for graphical purposes, can be inserted by the user in any point of the circuit    
    def barrier(self):
        self.__barrier_ASCII_block()
        barrier_data = {'name': 'barrier', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(barrier_data)
            
       
    # Following two functions are for general Qudit gate construction (user manually inserts the matrices).
    # These are meant for circuit with more than 3 basis states.
    def custom_gate(self, gate, target, name: str = 'CUST'):
        """
        Apply a custom single-qudit gate. 
        gate must be a matrix in the form of numpy.array.

        Args:
            gate (np.ndarray): Unitary matrix representing the gate.
            target (int): Index of the target qudit.
            name (str): Gate label (max 4 characters) for visualization.

        Raises:
            ValueError: If name exceeds 4 characters.
        """
        if len(name) > 4: # Ensure the gate name fits in ASCII visualization (max 4 characters)
         raise ValueError(f"Name of the gate must be of max 4 chars")  
            
        self.__einsum_gates.append((gate,target))
        self.__fullmatrix_gates.append((qt.Qobj(gate), target))
        
        self.__simple_gate_ASCII_block(ascii_gates.custom_ascii(name), target)
        gate_data = {'name': name, 'target': target, 'color': '#C7D3D4', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)           
        
    def c_custom_gate(self, gate, control, target, name: str = 'CUST'):
        """
        Apply a custom controlled qudit gate.

        The gate is applied to the target qudit only when the control qudit is in the |d−1⟩ state (with d being the basis states of the circuit).
        gate must be a matrix in the form of numpy.array.

        Args:
            gate (np.ndarray): Unitary matrix representing the gate.
            control (int): Index of the control qudit.
            target (int): Index of the target qudit.
            name (str): Gate label (max 4 characters) for visualization.

        Raises:
            ValueError: If name exceeds 4 characters.
        """ 
        if len(name) > 4:
         raise ValueError(f"Name of the gate must be of max 4 chars")
         
        self.__einsum_gates.append((gate, control, target))
        self.__fullmatrix_gates.append((qt.Qobj(gate), control, target))
        
        self.__controlled_gate_ASCII_block(ascii_gates.custom_ascii(name), control, target)
        gate_data = {'name': name, 'control': control, 'target': target, 'color': '#603F83', 'column': len(self.__mpl_circuit_visualization_list)}
        self.__mpl_circuit_visualization_list.append(gate_data)


    # Following two functions are for circuit simulation    

    def simulate_fullmatrix(self,show_final_state_vector: bool = False):
        """
        Simulates the execution of the quantum circuit using full matrix operations.
        
        Initializes the system in the |0⟩ state for each qudit, applies each gate to the system state
        and calculates and prints the density matrix for each individual qudit

        Notes:
        The circuit is evolved using matrix multiplication on the full quantum state. 
        As a result, the data size grows rapidly, and simulation becomes computationally expensive.
        The bigger the number of states is and the less qudits can be used in the circuit.
        When using qutrits it is recommended to limit the circuit to a maximum of 8 qutrits while using this simulator.

        Args:
            show_final_state_vector (bool): If True, prints the full final state vector.
        
        Output:
        Prints the density matrix of each qudit after circuit execution.
        Prints the final measurement probabilities
        Prints the Final State Vector if show_final_state_vector is flagged to 'True'
        """
        output_list=[]
        
        initial_state = qt.tensor([qt.basis(self.num_states, 0)] * self.num_qudit) # Prepares initial state with all qudits in |0⟩ state
        final_state = qt.Qobj(initial_state.full(), dims=[[self.num_states ** self.num_qudit], [1]]) # Converts dimensions to be able to work with operators

        for gate in self.__fullmatrix_gates:
            if len(gate)==2: # If the gate is NOT controlled calls the __shift_gate function to develop the system state, it will return the operator to apply to the state
             op_matrix, target_index = gate
             full_op = self.__single_qudit_gate(op_matrix, target_index)
            else: # If the gate is controlled calls the __ms_gate function to develop the system state, it will return the operator to apply to the state
             op_matrix, control_index, target_index = gate
             full_op = self.__controlled_qudit_gate(op_matrix, control_index, target_index)
            # Applies the returned operator to the final state evolving it
            final_state = full_op * final_state 
            
        # Converts the final state in a Qobj to allow the use of ptrace and the final probabilities measurment
        final_state_tensor = qt.Qobj(final_state.full(), dims=[[self.num_states] * self.num_qudit, [1] * self.num_qudit]) 
        
        # SECTION TO PRINT QUDIT DENSITY MATRICES
        for i in range(self.num_qudit): # From the final state it retrieves the (num_states x num_states) matrix of each qudit and prints it
         state = final_state_tensor.ptrace(i)
         matrix = state.full()
         matrix[np.abs(matrix) < 1e-15] = 0  # In the density matrix sets to 0 small values for more clarity 
         output_list.append(f"QUDIT {i} Density Matrix:\n{matrix}") 
        print("\n".join(output_list))
        
        # SECTION TO PRINT FINAL MEASUMENTS PROBABILITIES 
        probs = np.abs(final_state_tensor.full().flatten())**2 # Gives the measurement probability distribution in the computational basis
        threshold = 1e-5  # Will ignore states under this probability
        print("\nFinal measurement probabilities:\n")
        for i, p in enumerate(probs):
          if p > threshold:
           basis_state = self.__index_to_basis_string(i) # Calls the __index_to_basis_string
           print(f"|{basis_state}⟩: {p*100:.2f}%")
              
        # SECTION TO PRINT FINAL MEASUMENTS PROBABILITIES 
        if show_final_state_vector: # If user flagged the final state the functions also prints the  final_state vector
         print("\nFinal State Vector:\n", final_state)
         
        
    def __index_to_basis_string(self,index):
     return ''.join(str(x) for x in np.base_repr(index, self.num_states).zfill(self.num_qudit)) 
        
    def simulate_einsum(self):
     """
     Simulates the execution of the quantum circuit using Einstein summation (einsum).
     
     This method evolves the state of the circuit with tensor contractions using NumPy's einsum.
     It allows the simulation of circuits with a relatively large number of qudits, as it avoids explicit matrix multiplication.
     The number of qudits that is possible to use in the circuits depends on the number of states of the qudit.
     Generally a maximum of 17 qutrits can be used with this kind of simulation.
     
     The quantum state is represented as a multidimensional tensor with shape [d, d, ..., d] (one axis per qudit) where d is the number of states.
     The gates are applied via einsum string manipulation, with index-wise operations.
     Controlled gates are only applied if the control qudit is in the num_states-1⟩ state.

     Output:
     Prints the state probabilities of each qudit after circuit execution, based on the reduced probabilities.
     """  

     qudit_states = [] # Created to later print the results
    
     state = np.zeros([self.num_states] * self.num_qudit, dtype="complex64") # Prepares initial state with all qudit in |0⟩ state
     state[(0,) * self.num_qudit] = 1.0
     
     for gate in self.__einsum_gates: 
        if len(gate) == 2: # Checks if the gate is a simple gate or a controlled one
            op_matrix, target_index = gate
        elif len(gate) == 3:
            op_matrix, control_index, target_index = gate
            
            # Retrives the state of the control qudit
            axes = tuple(j for j in range(self.num_qudit) if j != control_index)
            control_state = np.sum(np.abs(state)**2, axis=axes)
            # If is not in the state |self.num_states-1⟩ it exits the for
            target_state = np.zeros(self.num_states)
            target_state[self.num_states - 1] = 1  # |self.num_states-1⟩
            if not np.allclose(control_state, target_state):
                continue
            
        # Applies the given gate on the target qudit
        indices = [chr(ord('a') + i) for i in range(self.num_qudit)] # Creates indices (ex. abc)
        einsum_str = f"{''.join(indices)},{indices[target_index]}x->" 
        indices[target_index] = 'x'
        einsum_str += ''.join(indices) # With these 3 lines the index of the target qudit is swap with 'x' (ex. abc,bx->axc)
        state = np.einsum(einsum_str, state, op_matrix.T) # We generate the state of the circuit with einsum 

     for i in range(self.num_qudit): # Analog to the code where the control qudit state is retrieved, here we retrieve the state of all qudits
        axes = tuple(j for j in range(self.num_qudit) if j != i)
        reduced = np.sum(np.abs(state)**2, axis=axes)
        qudit_states.append(reduced)
        
     for i, q in enumerate(qudit_states): # Prints the qudits states 
        print(f"QUDIT {i} state probabilities:")
        for values in q:
         print(f"  {values:.0f}")
  
        
    def draw(self,mode='ascii'):
        """
        Draws the quantum circuit. 
        The ascii version is shown all in a orizontal scrollable circuit.
        The Matplotlib is shown in segments one under the other in groups of 20 gates.

        Parameters:
        mode (str): 'ascii' (default) Renders the circuit using plain text.
                    'mpl' Renders the circuit using Matplotlib

        Example:
        qc.draw()           # ASCII circuit visualization
        qc.draw(mode='mpl') # Graphical circuit visualization with Matplotlib
        """
        if mode=='mpl':
            self.__mpl_draw()
        else:
            for lines in zip(*self.__ascii_circuit_visualization_list):
             print("".join(lines))        
        
    # Private functions used by the Class to create the graphic ASCII circuit
    
    def __initial_ASCII_block(self): # Used to start the visual representation and print each qudit of the circuit and the initial circuit lines
        block = []
        for i in range(self.num_qudit):
            if i>=10:
             block.extend(["         ", "Q" + str(i) + "  ----", "         "]) # If qudit is the 10th or more removes a space to avoid graphic problems
            else:
              block.extend(["         ", "Q" + str(i) + "   ----", "         "])    
        self.__ascii_circuit_visualization_list.append(block)
        
    def __simple_gate_ASCII_block(self, GATE_ASCII, target): # Used for the visual representation of single qudit gates
        block = []
        for _ in range(target):
            block.extend(ascii_gates.WIRE_ASCII) # Empty wires on qudits before the target qudit

        block.extend(GATE_ASCII) # Visual representation of the gate on the target qudit 

        for _ in range(self.num_qudit - target - 1): # Empty wires on qudits after the target qudit
            block.extend(ascii_gates.WIRE_ASCII)
        self.__ascii_circuit_visualization_list.append(block)
        
    def __controlled_gate_ASCII_block(self, GATE_ASCII, control, target): # Used for the visual representation of a controlled gate
        block = []
        
        if target > control: # Based on the position of the target and the control we have 2 different codes
            for _ in range(control):
                block.extend(ascii_gates.WIRE_ASCII) # Empty wires before the control
            block.extend(ascii_gates.CONTROL_ASCII) # Visual representation of the control symbol on the control qudit
            for _ in range(target - control - 1): # Line that connects control to the gate on target qudit 
                block.extend(ascii_gates.LINE_ASCII)

            block.extend(GATE_ASCII) # Visual representation of the gate on the target qudit 

            for _ in range(self.num_qudit - target - 1):
                block.extend(ascii_gates.WIRE_ASCII)
            self.__ascii_circuit_visualization_list.append(block)
            
        else: # Mirrored version of the previous 'if'
            for _ in range(target):
                block.extend(ascii_gates.WIRE_ASCII)
            block.extend(GATE_ASCII)
            for _ in range(control - target - 1):
                block.extend(ascii_gates.LINE_ASCII)

            block.extend(ascii_gates.CONTROL_ASCII_REV)

            for _ in range(self.num_qudit - control - 1):
                block.extend(ascii_gates.WIRE_ASCII)
            self.__ascii_circuit_visualization_list.append(block)
            
    def __barrier_ASCII_block(self): # Barrier lines
        block = []
        for _ in range(self.num_qudit): 
            block.extend(ascii_gates.BARRIER_ASCII)
        self.__ascii_circuit_visualization_list.append(block)
                
            
    # Function used by the Class to create the graphic Matplotlib circuit
           
    def __mpl_draw(self, max_gates=20): # Splits the drawing after 20 gates
     total_gates = len(self.__mpl_circuit_visualization_list)
     num_figures = max(1, ceil(total_gates / max_gates))  # Ensure at least one figure is created (ex. 42 gates gives 42/20=3 figures)

     for index in range(num_figures): # Creates one figure per time
        start_gate = index * max_gates # Gates printing interval
        end_gate = start_gate + max_gates 

        fig, ax = plt.subplots(figsize=(1.5 * max_gates, self.num_qudit)) # Creates figure with dimensions related to the number of qudits and the max_gate value 

        # Axes set up and borders removal
        ax.set_xlim(-0.5, max_gates - 0.5)
        ax.set_ylim(self.num_qudit - 0.5, -0.5)
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Draws wires in the figure
        for q in range(self.num_qudit):
            ax.plot([-0.5, max_gates - 0.5], [q, q], 'k', lw=2.5)

        # Cycle to draw gates in the figure
        for gate in self.__mpl_circuit_visualization_list:
            
            gate_position = gate['column'] # Takes the gate position from the gate info
            if not (start_gate <= gate_position < end_gate):
                continue  # Skips the gate if it is not beetween the gates range of the current figure

            relative_gate_position = gate_position - start_gate  # Brings the global position to a local position on the current figure
        
            name = gate['name'] # Retrives name and checks if it is a barrier
            if name == 'barrier':
                # Prints the barrier
                ax.axvline(x=relative_gate_position, color='gray', linestyle='--', linewidth=5, zorder=1)
                continue  # Skips the rest since is not a gate
            
            target = gate['target']  # Retrieves all other info on the gate
            color = gate['color']

            if 'control' in gate:
                control = gate['control']
                # Creates the gate box and the text above it
                ax.add_patch(plt.Rectangle((relative_gate_position - 0.3, target - 0.4), 0.6, 0.8, fill=True, color=color, zorder=3))
                ax.text(relative_gate_position, target, name, ha='center', va='center', fontsize=24, weight='bold', fontname='Courier New', zorder=6)
                # Creates the control indicator
                circle = plt.Circle((relative_gate_position, control), 0.1, color=color, zorder=5)
                ax.add_patch(circle)
                ax.plot([relative_gate_position, relative_gate_position], [min(control, target), max(control, target)], color=color, lw=2.5, zorder=5) # Line that connects control and gate
            else: # If is not a controlled gate just puts the gate box on the target
                ax.add_patch(plt.Rectangle((relative_gate_position - 0.3, target - 0.4), 0.6, 0.8, fill=True, color=color, zorder=3))
                ax.text(relative_gate_position, target, name, ha='center', va='center', fontsize=24, weight='bold', fontname='Courier New', zorder=6)

        # Sets labels on y axis to be the number of qudit
        ax.set_yticks(range(self.num_qudit))
        ax.set_yticklabels([rf'$q_{{{i}}}$' for i in range(self.num_qudit)])
        ax.tick_params(axis='y', length=0)
        ax.set_xticks([])
        for label in ax.get_yticklabels():
            label.set_fontsize(15)
        
        # Prints the figure or figures    
        if num_figures==1:
            plt.show()
        else:
            plt.title(f"Circuit Segment {index + 1}", fontsize=18)
            plt.show()
        
    # Private funcion called by simulate_fullmatrix() when a single qudit gate acts on the circuit
    
    def __single_qudit_gate(self, GATE, target):
        """
        Builds a single_qudit_gate operator,

        :param GATE: Matrix of a gate in qt.obj form
        :param target: Index of target qudit
        :return: Tensor product of all qudits
        """
        # Builds operator doing a tensor product beetween GATE on target qudit and identities on other qudits
        operator_list = [qt.Qobj(np.eye(self.num_states, dtype=complex)) for _ in range(self.num_qudit)]
        operator_list[target] = GATE
        operator = qt.tensor(*operator_list)
        # Coverts operator dimensions
        return qt.Qobj(operator.full(), dims=[[self.num_states ** self.num_qudit], [self.num_states ** self.num_qudit]])
         
        
    # Private funcion called by simulate_fullmatrix() when a controlled gate acts on the circuit
    
    def __controlled_qudit_gate(self, GATE, control, target):
      """
      Builds a controlled_qudit_gate operator, 'GATE' is applied on target if control is in num_states-1⟩ state, otherwise identity is applied

      :param GATE: Matrix of a gate in qt.obj form
      :param control: Index of control qudit
      :param target: Index of target qudit
      :return: Tensor product of all qudits
      """
      # Pass inputs for code clarity purposes
      d = self.num_states
      n = self.num_qudit 

      # Defines the projector on |d-1><d-1| for control qudit, isolates the d-1 component of the qudit
      P = qt.basis(d, d - 1) * qt.basis(d, d - 1).dag()

      # (GATE - I), to apply only when control is in |d-1>
      target_gate_delta = GATE - qt.qeye(d)

      # Builds a list of identities with the projector inserted at the control qudit position
      op_list_P = [qt.qeye(d) for _ in range(n)]
      op_list_P[control] = P # On control we apply projector
      P_full = qt.tensor(op_list_P)

      # Operator that extends the target_gate_delta to the all system  
      op_list_T = [qt.qeye(d) for _ in range(n)]
      op_list_T[target] = target_gate_delta # On target we apply delta_gate
      T_full = qt.tensor(op_list_T)

      # Modify operators dimensions 
      flat_dims = [[d ** n], [d ** n]]
      P_full.dims = flat_dims
      T_full.dims = flat_dims

      # Final operator, will give I on target when control is not in d-1 state, or GATE when control is in d-1 state
      full_operator = qt.qeye(d ** n) + P_full * T_full
      return full_operator
