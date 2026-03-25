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
        self.__gate_table = None
        self.__initial_ASCII_block()

    def set_gate_table(self, gate_table: dict):
        """
        Register a label->matrix dictionary used by shift()/ms()/toffoli() wrappers.
        
        Args:
            gate_table (dict): A dictionary mapping string labels to unitary matrices (as numpy arrays or lists).
                For example: {"+1": [[0, 0, 1], [1, 0, 0], [0, 1, 0]], "12": [[1, 0, 0], [0, 0, 1], [0, 1, 0]]}
        """
        if not isinstance(gate_table, dict):
            raise TypeError("gate_table must be a dict mapping labels to matrices")
        self.__gate_table = gate_table

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

    def cc_custom_gate(self, gate, control1, control2, target, name: str = "CUST", control_values=None):
        """
        Doubly-controlled custom gate.

        control_values:
            list/tuple of two integers [v1, v2].
            Gate is applied iff control1==v1 and control2==v2.
            If control_values is None, both controls are assumed to be |d-1>.

        Input:
            gate (np.ndarray): Unitary matrix representing the gate.
            control1 (int): Index of the first control qudit.
            control2 (int): Index of the second control qudit.
            target (int): Index of the target qudit.
            name (str): Gate label (max 4 characters) for visualization.
            control_values (list/tuple, optional): Values of the control qudits for which the gate is applied.
        """
        if len(name) > 4:
            raise ValueError("Name of the gate must be of max 4 chars")

        if control_values is None:
            control_values = [self.num_states - 1, self.num_states - 1]
        if len(control_values) != 2:
            raise ValueError("control_values must be a list or tuple of length 2")

        v1, v2 = control_values
        self.__einsum_gates.append(("CCV", gate, control1, control2, target, (v1, v2)))
        self.__fullmatrix_gates.append(("CCV", qt.Qobj(gate), control1, control2, target, (v1, v2)))
        self.__multi_controlled_gate_ASCII_block(ascii_gates.custom_ascii(name), controls=[control1, control2], target=target, control_values=[v1, v2])

        gate_data = {
            "name": name,
            "controls": [control1, control2],
            "control_values": [v1, v2],
            "target": target,
            "color": "#603F83",
            "column": len(self.__mpl_circuit_visualization_list),
        }
        self.__mpl_circuit_visualization_list.append(gate_data)

    def toffoli(self, label: str, control1: int, control2: int, target: int, control_values=None, name: str | None = None):
        """
        Apply a Toffoli-like gate with a custom single-qudit operation.

        Example: toffoli("+2", 0, 1, 2) or toffoli("+2", 0, 1, 2, [2, 2])

        Input:
            label (str): Label of the single-qudit gate to apply (e.g., "+1", "12", etc.).
            control1 (int): Index of the first control qudit.
            control2 (int): Index of the second control qudit.
            target (int): Index of the target qudit.
            control_values (list/tuple, optional): Values of the control qudits for which the gate is applied. If None, defaults to both controls being |d-1⟩.
            name (str, optional): Custom label for visualization. If None, defaults to the provided label.
        """
        if name is None:
            name = label
        U = self._label_to_matrix(label)
        return self.cc_custom_gate(
            U,
            control1=control1,
            control2=control2,
            target=target,
            name=str(name)[:4],
            control_values=control_values,
        )
    
    def feynman(self, control: int, target: int):
        """
        Apply a Feynman-like gate (also known as controlled-NOT in the qubit case) that increments the target qudit by 1 
        if the control qudit is in the |d-1⟩ state.

        Input:
            control (int): Index of the control qudit.
            target (int): Index of the target qudit.
        """
        U = self._label_to_matrix("+1")
        return self.c_custom_gate(
            U,
            control=control,
            target=target,
            name="F"
        )
        
    def barrier(self):
        """
        Insert a barrier in the circuit for graphical purposes. It does not affect the simulation.
        It can be inserted by the user in any point of the circuit.
        """
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

    def c_custom_gate(self, gate, control, target, name: str = 'CUST', control_values=None):
        """
        Apply a custom controlled qudit gate.

        The gate is applied to the target qudit only when the control qudit is in the |d−1⟩ state (with d being the basis states of the circuit).
        gate must be a matrix in the form of numpy.array.

        Args:
            gate (np.ndarray): Unitary matrix representing the gate.
            control (int): Index of the control qudit.
            target (int): Index of the target qudit.
            name (str): Gate label (max 4 characters) for visualization.
            control_values (list/tuple, optional): Values of the control qudit for which the gate is applied. If None, defaults to |d-1⟩.

        Raises:
            ValueError: If name exceeds 4 characters.
        """ 
        if len(name) > 4:
            raise ValueError("Name of the gate must be of max 4 chars")

        if control_values is None:
            v = self.num_states - 1
        else:
            if isinstance(control_values, (list, tuple)):
                if len(control_values) != 1:
                    raise ValueError("control_values must be an int or a list/tuple of length 1")
                v = int(control_values[0])
            else:
                v = int(control_values)

        if not (0 <= v < self.num_states):
            raise ValueError(f"control value v must be in [0, {self.num_states - 1}]")

        self.__einsum_gates.append(("CV", gate, control, target, v))
        self.__fullmatrix_gates.append(("CV", qt.Qobj(gate), control, target, v))

        self.__controlled_gate_ASCII_block(ascii_gates.custom_ascii(name), control, target)

        gate_data = {
            "name": name,
            "controls": [control],
            "control_values": [v],
            "target": target,
            "color": "#603F83",
            "column": len(self.__mpl_circuit_visualization_list),
        }
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
        output_list = []

        initial_state = qt.tensor([qt.basis(self.num_states, 0)] * self.num_qudit)
        final_state = qt.Qobj(
            initial_state.full(),
            dims=[[self.num_states ** self.num_qudit], [1]],
        )

        for gate in self.__fullmatrix_gates:
            if len(gate) == 2 and not isinstance(gate[0], str):
                op_matrix, target_index = gate
                full_op = self.__single_qudit_gate(op_matrix, target_index)

            elif len(gate) == 3 and not isinstance(gate[0], str):
                op_matrix, control_index, target_index = gate
                full_op = self.__controlled_qudit_gate(op_matrix, control_index, target_index)

            else:
                if isinstance(gate[0], str) and gate[0] == "CV":
                    _, op_matrix, c1, target_index, v = gate
                    full_op = self.__value_multi_controlled_qudit_gate(
                        op_matrix, controls=[c1], values=[v], target=target_index
                    )

                elif isinstance(gate[0], str) and gate[0] == "CCV":
                    _, op_matrix, c1, c2, target_index, control_values = gate
                    full_op = self.__value_multi_controlled_qudit_gate(
                        op_matrix, controls=[c1, c2], values=list(control_values), target=target_index
                    )
                else:
                    op_matrix = gate[0]
                    control_indices = gate[1:-1]
                    target_index = gate[-1]
                    full_op = self.__multi_controlled_qudit_gate(op_matrix, list(control_indices), target_index)

            final_state = full_op * final_state

        final_state_tensor = qt.Qobj(
            final_state.full(),
            dims=[[self.num_states] * self.num_qudit, [1] * self.num_qudit],
        )

        for i in range(self.num_qudit):
            state = final_state_tensor.ptrace(i)
            matrix = state.full()
            matrix[np.abs(matrix) < 1e-15] = 0
            output_list.append(f"QUDIT {i} Density Matrix:\n{matrix}")
        print("\n".join(output_list))

        probs = np.abs(final_state_tensor.full().flatten()) ** 2
        threshold = 1e-5
        print("\nFinal measurement probabilities:\n")
        for i, p in enumerate(probs):
            if p > threshold:
                basis_state = self.__index_to_basis_string(i)
                print(f"|{basis_state}⟩: {p * 100:.2f}%")

        if show_final_state_vector:
            print("\nFinal State Vector:\n", final_state)
         
        
    def __index_to_basis_string(self,index):
     return ''.join(str(x) for x in np.base_repr(index, self.num_states).zfill(self.num_qudit)) 

    def __multi_controlled_qudit_gate(self, GATE, controls, target):
        """
        Constructs the full operator for a multi-controlled single-qudit gate.
        The gate is applied to the target qudit only when all control qudits are in the |d−1⟩ state (with d being the basis states of the circuit).     

        Args:
            GATE (qt.Qobj): The single-qudit gate to apply (as a Qobj).
            controls (list): List of control qudit indices.
            target (int): Index of the target qudit.    

        Returns:
            qt.Qobj: The full operator representing the multi-controlled gate.
        """
        
        d = self.num_states
        n = self.num_qudit

        P = qt.basis(d, d - 1) * qt.basis(d, d - 1).dag()
        target_gate_delta = GATE - qt.qeye(d)

        op_list_P = [qt.qeye(d) for _ in range(n)]
        for c in controls:
            op_list_P[c] = P
        P_full = qt.tensor(op_list_P)

        op_list_T = [qt.qeye(d) for _ in range(n)]
        op_list_T[target] = target_gate_delta
        T_full = qt.tensor(op_list_T)

        flat_dims = [[d ** n], [d ** n]]
        P_full.dims = flat_dims
        T_full.dims = flat_dims

        full_operator = qt.qeye(d ** n) + P_full * T_full
        return full_operator

    def simulate_statevector(self, input_state=None, threshold=1e-9):
        """
        Exact simulation without building full (d^n x d^n) operators.
        Works well for n=10 on laptops.

        Supports:
          - single-qudit gates
          - legacy controlled gates on |d-1>
          - CV value-controlled 1-control custom gates
          - CCV value-controlled 2-control custom gates

        Args:
        input_state (list/tuple, optional): Initial state of the system as a list of integers representing the basis state of each qudit.
            If None, the system is initialized in the |0⟩ state for each qudit.
        threshold (float): Minimum probability threshold for printing basis states in the output.
        """
        d = self.num_states
        n = self.num_qudit

        state = np.zeros([d] * n, dtype=np.complex128)
        if input_state is None:
            state[(0,) * n] = 1.0
        else:
            state[tuple(input_state)] = 1.0

        def apply_1q_gate(st, U, axis):
            tmp = np.tensordot(st, U.T, axes=([axis], [0]))
            return np.moveaxis(tmp, -1, axis)

        for gate in self.__einsum_gates:
            # single-qudit: (U, t)
            if len(gate) == 2 and not isinstance(gate[0], str):
                U, t = gate
                state = apply_1q_gate(state, U, t)
                continue

            # CV: ("CV", U, c, t, v)
            if isinstance(gate[0], str) and gate[0] == "CV":
                _, U, c, t, v = gate
                sl = [slice(None)] * n
                sl[c] = slice(v, v + 1)  # keep dim
                sub = state[tuple(sl)]
                state[tuple(sl)] = apply_1q_gate(sub, U, t)
                continue

            # CCV: ("CCV", U, c1, c2, t, (v1, v2))
            if isinstance(gate[0], str) and gate[0] == "CCV":
                _, U, c1, c2, t, (v1, v2) = gate
                sl = [slice(None)] * n
                sl[c1] = slice(v1, v1 + 1)
                sl[c2] = slice(v2, v2 + 1)
                sub = state[tuple(sl)]
                state[tuple(sl)] = apply_1q_gate(sub, U, t)
                continue

            # legacy multi-control on |d-1>: (U, c1, c2, ..., t)
            U = gate[0]
            controls = list(gate[1:-1])
            t = gate[-1]
            sl = [slice(None)] * n
            for c in controls:
                sl[c] = slice(d - 1, d)
            sub = state[tuple(sl)]
            state[tuple(sl)] = apply_1q_gate(sub, U, t)

        probs = np.abs(state) ** 2
        flat = probs.reshape(-1)

        print("\nFinal measurement probabilities:\n")
        for i, p in enumerate(flat):
            if p > threshold:
                basis = np.base_repr(i, d).zfill(n)
                print(f"|{basis}⟩: {p * 100:.2f}%")
        
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

        qudit_states = []

        state = np.zeros([self.num_states] * self.num_qudit, dtype="complex64")
        state[(0,) * self.num_qudit] = 1.0

        for gate in self.__einsum_gates:
            if len(gate) == 2 and not isinstance(gate[0], str):
                op_matrix, target_index = gate
                control_indices = []
                values = []
            else:
                if isinstance(gate[0], str) and gate[0] == "CV":
                    _, op_matrix, c1, target_index, v = gate
                    control_indices = [c1]
                    values = [v]
                elif isinstance(gate[0], str) and gate[0] == "CCV":
                    _, op_matrix, c1, c2, target_index, control_values = gate
                    control_indices = [c1, c2]
                    values = list(control_values)
                else:
                    op_matrix = gate[0]
                    control_indices = list(gate[1:-1])
                    target_index = gate[-1]
                    values = [self.num_states - 1] * len(control_indices)

                if control_indices:
                    all_ok = True
                    for control_index, v in zip(control_indices, values):
                        axes = tuple(j for j in range(self.num_qudit) if j != control_index)
                        control_state = np.sum(np.abs(state) ** 2, axis=axes)
                        target_state = np.zeros(self.num_states)
                        target_state[v] = 1
                        if not np.allclose(control_state, target_state):
                            all_ok = False
                            break
                    if not all_ok:
                        continue

            indices = [chr(ord("a") + i) for i in range(self.num_qudit)]
            einsum_str = f'{"".join(indices)},{indices[target_index]}x->'
            indices[target_index] = "x"
            einsum_str += "".join(indices)
            state = np.einsum(einsum_str, state, op_matrix.T)

        for i in range(self.num_qudit):
            axes = tuple(j for j in range(self.num_qudit) if j != i)
            reduced = np.sum(np.abs(state) ** 2, axis=axes)
            qudit_states.append(reduced)

        for i, q in enumerate(qudit_states):
            print(f"QUDIT {i} state probabilities:")
            for values in q:
                print(f"  {values:.0f}")

    def get_output(self, input_state=None):
        """
        Simulates the execution of the quantum circuit using Einstein summation (einsum) and returns a vector with the value of each qudit
        
        This method evolves the state of the circuit with tensor contractions using NumPy's einsum.
        It allows the simulation of circuits with a relatively large number of qudits, as it avoids explicit matrix multiplication.
        The number of qudits that is possible to use in the circuits depends on the number of states of the qudit.
        Generally a maximum of 17 qutrits can be used with this kind of simulation.
        
        The quantum state is represented as a multidimensional tensor with shape [d, d, ..., d] (one axis per qudit) where d is the number of states.
        The gates are applied via einsum string manipulation, with index-wise operations.
        Controlled gates are only applied if the control qudit is in the num_states-1⟩ state.

        Input:
            input_state: A list of integers representing the initial state of each qudit.
        
        Output:
            A vector with the value of each qudit after circuit execution
        """  

        qudit_states = []

        if input_state is not None:
            state = np.zeros([self.num_states] * self.num_qudit, dtype="complex64")
            state[tuple(input_state)] = 1.0
        else:
            state = np.zeros([self.num_states] * self.num_qudit, dtype="complex64")
            state[(0,) * self.num_qudit] = 1.0

        for gate in self.__einsum_gates:
            if len(gate) == 2 and not isinstance(gate[0], str):
                op_matrix, target_index = gate
                control_indices = []
                values = []
            else:
                if isinstance(gate[0], str) and gate[0] == "CV":
                    _, op_matrix, c1, target_index, v = gate
                    control_indices = [c1]
                    values = [v]
                elif isinstance(gate[0], str) and gate[0] == "CCV":
                    _, op_matrix, c1, c2, target_index, control_values = gate
                    control_indices = [c1, c2]
                    values = list(control_values)
                else:
                    op_matrix = gate[0]
                    control_indices = list(gate[1:-1])
                    target_index = gate[-1]
                    values = [self.num_states - 1] * len(control_indices)

                if control_indices:
                    all_ok = True
                    for control_index, v in zip(control_indices, values):
                        axes = tuple(j for j in range(self.num_qudit) if j != control_index)
                        control_state = np.sum(np.abs(state) ** 2, axis=axes)
                        target_state = np.zeros(self.num_states)
                        target_state[v] = 1
                        if not np.allclose(control_state, target_state):
                            all_ok = False
                            break
                    if not all_ok:
                        continue

            indices = [chr(ord("a") + i) for i in range(self.num_qudit)]
            einsum_str = f'{"".join(indices)},{indices[target_index]}x->'
            indices[target_index] = "x"
            einsum_str += "".join(indices)
            state = np.einsum(einsum_str, state, op_matrix.T)

        for i in range(self.num_qudit):
            axes = tuple(j for j in range(self.num_qudit) if j != i)
            reduced = np.sum(np.abs(state) ** 2, axis=axes)
            qudit_states.append(reduced)

        result = []
        for q in qudit_states:
            result.append(int(np.argmax(q)))
        return result
    
    def get_output(self, input_state=[]):
     """
     Simulates the execution of the quantum circuit using Einstein summation (einsum) and returns a vector with the value of each qudit
     
     This method evolves the state of the circuit with tensor contractions using NumPy's einsum.
     It allows the simulation of circuits with a relatively large number of qudits, as it avoids explicit matrix multiplication.
     The number of qudits that is possible to use in the circuits depends on the number of states of the qudit.
     Generally a maximum of 17 qutrits can be used with this kind of simulation.
     
     The quantum state is represented as a multidimensional tensor with shape [d, d, ..., d] (one axis per qudit) where d is the number of states.
     The gates are applied via einsum string manipulation, with index-wise operations.
     Controlled gates are only applied if the control qudit is in the num_states-1⟩ state.

     Output:
     A vector with the value of each qudit after circuit execution
     """  

     qudit_states = [] # Created to later print the results
    
     if input_state: # If the user provides an input state it is used to initialize the circuit
        state = np.zeros([self.num_states] * self.num_qudit, dtype="complex64")
        state[tuple(input_state)] = 1.0
     else:
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
        elif len(gate) == 5:
            _, op_matrix, c1, target_index, v = gate
            control_indices = [c1]
            values = [v]

            # Retrieves the state of the control qudit
            axes = tuple(j for j in range(self.num_qudit) if j != c1)
            control_state = np.sum(np.abs(state) ** 2, axis=axes)
            target_state = np.zeros(self.num_states)
            target_state[v] = 1
            if not np.allclose(control_state, target_state):
                continue
        else:
            print(gate)
            raise ValueError("Unforeseen gate length: " + str(len(gate)))          
            
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
        
     result = []
     for i, q in enumerate(qudit_states): 
        result.append(np.argmax(q)) # Takes the index of the maximum value of each qudit state, which corresponds to the qudit value
     return result
     
        
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
            
            target = gate.get("target", None)  # Retrieves all other info on the gate
            color = gate.get("color", "#000000")

            if 'controls' in gate:
                controls = gate['controls']
                values = gate.get("control_values", [None] * len(controls))

                if gate.get("name") == "F" and len(controls) == 1:
                    # Only one control for that gate
                    control = controls[0]
                    target_circle = plt.Circle((relative_gate_position, target), 0.25, fill=False, color=color, linewidth=2.5, zorder=5)
                    ax.add_patch(target_circle)
                    ax.plot([relative_gate_position - 0.2, relative_gate_position + 0.2], [target, target], color=color, lw=2.5, zorder=6)
                    ax.plot([relative_gate_position, relative_gate_position], [target - 0.2, target + 0.2], color=color, lw=2.5, zorder=6)
                    control_circle = plt.Circle((relative_gate_position, control), 0.1, color=color, zorder=6)
                    ax.add_patch(control_circle)
                    ax.plot([relative_gate_position, relative_gate_position], [min(control, target), max(control, target)], color=color, lw=2.5, zorder=5)
                else:
                    # Creates the gate box and the text above it
                    ax.add_patch(plt.Rectangle((relative_gate_position - 0.3, target - 0.4), 0.6, 0.8, fill=True, color=color, zorder=3))
                    ax.text(relative_gate_position, target, name, ha='center', va='center', fontsize=24, weight='bold', fontname='Courier New', zorder=6)
                    # Creates the control indicator
                    for control, val in zip(controls, values):
                        circle = plt.Circle((relative_gate_position, control), 0.18, color=color, zorder=5)
                        ax.add_patch(circle)

                        if val is not None:
                            ax.text(relative_gate_position, control, str(val), ha="center", va="center", fontsize=12, color="white", weight="bold", zorder=6)

                        ax.plot([relative_gate_position, relative_gate_position], [min(control, target), max(control, target)], color=color, lw=2.5, zorder=5) # Line that connects control and gate
            elif "control" in gate:
                control = gate["control"]
                ax.add_patch(plt.Rectangle((relative_gate_position - 0.3, target - 0.4), 0.6, 0.8, fill=True, color=color, zorder=3))
                ax.text(relative_gate_position, target, name, ha="center", va="center", fontsize=24, weight="bold", fontname="Courier New", zorder=6)
                circle = plt.Circle((relative_gate_position, control), 0.1, color=color, zorder=5)
                ax.add_patch(circle)
                ax.plot([relative_gate_position, relative_gate_position], [min(control, target), max(control, target)], color=color, lw=2.5, zorder=5)
            
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

    def optimize(self, gate_dict=None, tol: float = 0.0, merge_only_names=None):
        """
            Given a dictionary of gates and their corresponding unitary matrices, this method optimizes the quantum 
            circuit by merging consecutive gates into a single gate when possible.
        """
        return self.merged_custom_copy(
            gate_dict=gate_dict,
            tol=tol,
            merge_only_names=merge_only_names,
        )
    
    def _label_to_matrix(self, label: str):
        """
        Convert a gate label to its corresponding unitary matrix.
        Supported labels:
        - "+k": Cyclic shift by k positions (e.g., "+1" shifts |0⟩ to |1⟩, |1⟩ to |2⟩, ..., |d-1⟩ to |0⟩).
        - "ab": Swap states |a⟩ and |b⟩ (where a and b are single-digit integers representing state indices).
        - "0" or "I": Identity gate.

        Args:
            label (str): The label of the gate.

        Throws:
            ValueError: If the label is not recognized or if it has invalid format.

        Returns:
            np.ndarray: The unitary matrix corresponding to the given label.
        """
        d = self.num_states
        if not isinstance(label, str):
            raise TypeError("label must be a string")

        label = label.strip()

        # If a gate table is registered, allow arbitrary labels from it.
        if getattr(self, "__gate_table", None) is not None and label in self.__gate_table:
            return np.asarray(self.__gate_table[label], dtype=complex)

        # "+k" cyclic shift
        if label.startswith("+"):
            try:
                k = int(label[1:]) % d
            except ValueError as e:
                raise ValueError(f"Invalid shift label: {label}") from e
            P = np.zeros((d, d), dtype=complex)
            for j in range(d):
                P[(j + k) % d, j] = 1.0
            return P

        # swap "ab" (single-digit indices)
        if len(label) == 2 and label.isdigit():
            a = int(label[0])
            b = int(label[1])
            if not (0 <= a < d and 0 <= b < d and a != b):
                raise ValueError(f"Invalid swap label: {label}")
            P = np.eye(d, dtype=complex)
            P[[a, b], :] = P[[b, a], :]
            return P

        # identity aliases
        if label in ("0", "I"):
            return np.eye(d, dtype=complex)

        raise ValueError(f"Unsupported label: {label}")

    def shift(self, label: str, target: int, name: str | None = None):
        """
        Apply a single-qudit permutation gate specified by a label.

        Supported labels:
        - "+k": Cyclic shift by k positions (e.g., "+1" shifts |0⟩ to |1⟩, |1⟩ to |2⟩, ..., |d-1⟩ to |0⟩).
        - "ab": Swap states |a⟩ and |b⟩ (where a and b are single-digit integers representing state indices).
        - "0" or "I": Identity gate.    

        Args:
            label (str): The label of the gate to apply.
            target (int): The index of the target qudit.
            name (str | None): Optional name for the gate (max 4 characters) for visualization. If None, defaults to the label.
        
        Examples: shift("+1", 2), shift("12", 0)
        """
        if name is None:
            name = label
        U = self._label_to_matrix(label)

        # Use native qutrit helpers when possible (keeps colors/ASCII in the original style).
        if self.num_states == 3:
            if label in ("I", "0"):
                return self.id(target)
            if label == "+1":
                return self.plus1(target)
            if label == "+2":
                return self.plus2(target)
            if label == "01":
                return self.zero_one(target)
            if label == "02":
                return self.zero_two(target)
            if label == "12":
                return self.one_two(target)

        # Generic path
        return self.custom_gate(U, target=target, name=str(name)[:4])

    def ms(self, label: str, control: int, target: int, control_values=None, name: str | None = None):
        """
        Value-controlled single-control gate (MS-style wrapper).

        Supported labels:
        - "+k": Cyclic shift by k positions (e.g., "+1" shifts
            |0⟩ to |1⟩, |1⟩ to |2⟩, ..., |d-1⟩ to |0⟩).
        - "ab": Swap states |a⟩ and |b⟩ (where a and b are single-digit integers representing state indices).
        - "0" or "I": Identity gate.

        Args:
            label (str): The label of the gate to apply.
            control (int): The index of the control qudit.
            target (int): The index of the target qudit.
            control_values (int or list/tuple of length 1, optional): The control value(s) that enable the gate. If None, defaults to the maximum state (num_states - 1).
            name (str | None): Optional name for the gate (max 4 characters) for visualization. If None, defaults to the label.
        
        Example: ms("+1", 1, 0) or ms("+1", 1, 0, [2])
        """
        if name is None:
            name = label
        U = self._label_to_matrix(label)

        # Use native qutrit helpers when possible (keeps colors/ASCII in the original style).
        if self.num_states == 3 and control_values is None:
            if label == "+1":
                return self.c_plus1(control, target)
            if label == "+2":
                return self.c_plus2(control, target)
            if label == "01":
                return self.c_zero_one(control, target)
            if label == "02":
                return self.c_zero_two(control, target)
            if label == "12":
                return self.c_one_two(control, target)

        return self.c_custom_gate(U, control=control, target=target, name=str(name)[:4], control_values=control_values)

    def __multi_controlled_gate_ASCII_block(self, GATE_ASCII, controls, target, control_values=None):
        """
        Creates the ASCII block for a multi-controlled gate, with optional control values.

        Parameters:
        GATE_ASCII: The ASCII representation of the gate to be applied on the target qu
        controls: A list of control qudit indices.
        target: The index of the target qudit.
        control_values: A list of values for each control qudit that enable the gate. If
                        None, defaults to the maximum state (num_states - 1) for all controls.
                        
        """
        
        if control_values is None:
            control_values = [self.num_states - 1] * len(controls)
        if len(controls) != len(control_values):
            raise ValueError("controls and control_values must have the same length")

        control_map = {int(c): str(v) for c, v in zip(controls, control_values)}
        all_nodes = list(controls) + [target]
        min_idx = min(all_nodes)
        max_idx = max(all_nodes)

        def value_control_cell(value, connect_up=False, connect_down=False):
            value = str(value)[:3]
            width = len(GATE_ASCII[1])
            center_col = (width - 1) // 2

            top = [" "] * width
            if connect_up:
                top[center_col] = "|"
            top = "".join(top)

            ctrl = f"({value})"
            start = max(0, center_col - len(ctrl) // 2)
            end = start + len(ctrl)
            if end > width:
                end = width
                start = max(0, end - len(ctrl))
            mid = ["-"] * width
            mid[start:end] = list(ctrl[: end - start])
            mid = "".join(mid)

            bot = [" "] * width
            if connect_down:
                bot[center_col] = "|"
            bot = "".join(bot)
            return [top, mid, bot]

        block = []
        for q in range(self.num_qudit):
            if q == target:
                block.extend(GATE_ASCII)
            elif q in control_map:
                block.extend(
                    value_control_cell(
                        control_map[q],
                        connect_up=(q > min_idx),
                        connect_down=(q < max_idx),
                    )
                )
            elif min_idx < q < max_idx:
                block.extend(ascii_gates.LINE_ASCII)
            else:
                block.extend(ascii_gates.WIRE_ASCII)

        self.__ascii_circuit_visualization_list.append(block)

    def __value_multi_controlled_qudit_gate(self, GATE, controls, values, target):
        """
        Builds a multi-controlled qudit gate operator, 'GATE' is applied on target if all controls are in their specified values, otherwise identity is applied.

        Arguments:
        GATE: The gate to be applied on the target qudit (as a qt.Qobj).
        controls: A list of control qudit indices.
        values: A list of values for each control qudit that enable the gate. Must be the same length as controls.
        target: The index of the target qudit.
        """
        d = self.num_states
        n = self.num_qudit

        if len(controls) != len(values):
            raise ValueError("controls and values must have same length")

        target_gate_delta = GATE - qt.qeye(d)

        op_list_P = [qt.qeye(d) for _ in range(n)]
        for c, v in zip(controls, values):
            Pv = qt.basis(d, v) * qt.basis(d, v).dag()
            op_list_P[c] = Pv
        P_full = qt.tensor(op_list_P)

        op_list_T = [qt.qeye(d) for _ in range(n)]
        op_list_T[target] = target_gate_delta
        T_full = qt.tensor(op_list_T)

        flat_dims = [[d ** n], [d ** n]]
        P_full.dims = flat_dims
        T_full.dims = flat_dims

        full_operator = qt.qeye(d ** n) + P_full * T_full
        return full_operator

    def merged_custom_copy(self, gate_dict=None, tol: float = 0.0, merge_only_names=None):
            """Return a NEW QuditCircuit with MERGE-ONLY optimization (matrix-based).
    
            Supported merges:
              1) Single-qudit custom gates added via custom_gate(...), if their name is in gate_dict.
                 These are merged on the SAME target. They may be separated by gates that DO NOT touch
                 that target qudit (i.e., gates acting only on other qudits commute with them).
    
              2) Single-control custom gates added via c_custom_gate(...), if their name is in gate_dict.
                 These are merged when they have the SAME (control, target) and the (implicit) control_value
                 equals (num_states - 1). They may be separated by gates that do NOT touch either the control
                 or the target qudit.
    
            Merge rule: for a sequence U1 then U2, merged operator is U2 @ U1.
            """
            import numpy as np

            if gate_dict is None:
                gate_dict = {"0": np.eye(self.num_states, dtype=complex)}
                for k in range(1, self.num_states):
                    gate_dict[f"+{k}"] = self._label_to_matrix(f"+{k}")
                for a in range(self.num_states):
                    for b in range(a + 1, self.num_states):
                        gate_dict[f"{a}{b}"] = self._label_to_matrix(f"{a}{b}")
    
            src = list(self.__mpl_circuit_visualization_list)
            out = QuditCircuit(num_qudit=self.num_qudit, num_states=self.num_states)
    
            allowed = set(gate_dict.keys()) if merge_only_names is None else set(merge_only_names)
            control_value_required = self.num_states - 1
    
            def matrix_to_name(M):
                for name, A in gate_dict.items():
                    if tol == 0.0:
                        if np.array_equal(M, A):
                            return name
                    else:
                        if np.allclose(M, A, atol=tol, rtol=0.0):
                            return name
                return None
    

            def is_identity(M):
                M = np.asarray(M)
                if M.ndim != 2 or M.shape[0] != M.shape[1]:
                    return False
                I = np.eye(M.shape[0], dtype=complex)
                atol = tol if (tol is not None and tol > 0) else 1e-12
                return np.allclose(M, I, atol=atol, rtol=0.0)
    
            def gate_qudits(g):
                qs = set()
                if g.get("name") == "barrier":
                    return qs  # barrier handled separately
                if "target" in g:
                    qs.add(g["target"])
                if "control" in g:
                    qs.add(g["control"])
                if "controls" in g:
                    qs.update(list(g.get("controls")))
                return qs
    
            # Pending single-qudit merges: target -> matrix
            pending_single = {}  # t -> M
            # Pending controlled merges:
            #   single-control: (c,t,val) -> M
            #   double-control: (c1,c2,t,v1,v2) -> M
            pending_ctrl = {}
    
            def flush_all():
                # flush controlled first, then single (either order is fine because they shouldn't overlap)
                for key in list(pending_ctrl.keys()):
                    M = pending_ctrl.pop(key)
                    if is_identity(M):
                        continue
                    name = matrix_to_name(M)
                    if name is not None and name in ("0", "I"):
                        continue
                    if name is None:
                        raise ValueError("Merged controlled matrix not found in gate_dict.")
                    if len(key) == 3:
                        c, t, v = key
                        out.c_custom_gate(M, control=c, target=t, name=name, control_values=[v])
                    elif len(key) == 5:
                        c1, c2, t, v1, v2 = key
                        out.cc_custom_gate(M, control1=c1, control2=c2, target=t, name=name, control_values=[v1, v2])
                    else:
                        raise ValueError("Unsupported pending controlled key format.")
                for t in list(pending_single.keys()):
                    M = pending_single.pop(t)
                    if is_identity(M):
                        continue
                    name = matrix_to_name(M)
                    if name is not None and name in ("0", "I"):
                        continue
                    if name is None:
                        raise ValueError("Merged single-qudit matrix not found in gate_dict.")
                    out.custom_gate(M, target=t, name=name)
    
            def replay_gate(g):
                name = g.get("name")
                if name == "barrier":
                    out.barrier()
                    return
    
                # legacy single-control visualization: {'name':..., 'control':c, 'target':t}
                if "control" in g and "target" in g and "controls" not in g:
                    c = g["control"]; t = g["target"]
                    if name in ("0", "I"):
                        return
                    if name not in gate_dict:
                        raise ValueError(f"Controlled gate '{name}' not in gate_dict; cannot replay.")
                    out.c_custom_gate(gate_dict[name], control=c, target=t, name=name)
                    return
    
                # value-controlled (newer) visualization: {'name':..., 'controls':[...], 'control_values':[...], 'target':t}
                if "controls" in g and "target" in g:
                    ctrls = list(g["controls"])
                    vals = list(g.get("control_values", [control_value_required] * len(ctrls)))
                    t = g["target"]
                    if name in ("0", "I"):
                        return
                    if name == "F" and len(ctrls) == 1:
                        out.feynman(ctrls[0], t)
                        return
                    if name not in gate_dict:
                        raise ValueError(f"Controlled gate '{name}' not in gate_dict; cannot replay.")
                    if len(ctrls) == 1:
                        out.c_custom_gate(gate_dict[name], control=ctrls[0], target=t, name=name, control_values=[vals[0]])
                        return
                    if len(ctrls) == 2:
                        out.cc_custom_gate(gate_dict[name], control1=ctrls[0], control2=ctrls[1], target=t, name=name, control_values=[vals[0], vals[1]])
                        return
                    raise ValueError("merged_custom_copy replay supports up to 2 controls.")
    
                # single-qudit
                if "target" in g:
                    t = g["target"]
                    if name in ("0", "I"):
                        return
                    if name not in gate_dict:
                        raise ValueError(f"Single-qudit gate '{name}' not in gate_dict; cannot replay.")
                    out.custom_gate(gate_dict[name], target=t, name=name)
                    return
    
                raise ValueError(f"Unknown gate format: {g}")
    
            for g in src:
                name = g.get("name")

                if name == "barrier":
                    flush_all()
                    out.barrier()
                    continue

                # Identify whether THIS gate is mergeable, so we don't flush the very pending entry
                # we intend to extend.
                mergeable_single_target = None
                mergeable_ctrl_key = None

                # Single-qudit merge candidate?
                if ("target" in g and "control" not in g and "controls" not in g
                    and name in allowed and name in gate_dict):
                    mergeable_single_target = g["target"]

                # Single-control controlled merge candidate? (legacy form)
                if ("control" in g and "target" in g and "controls" not in g
                    and name in allowed and name in gate_dict):
                    c = g["control"]; t = g["target"]
                    mergeable_ctrl_key = (c, t, control_value_required)

                # Controlled merge candidate? (value-controlled form)
                if (mergeable_ctrl_key is None and "controls" in g and "target" in g
                    and name in allowed and name in gate_dict):
                    ctrls = list(g["controls"])
                    vals = list(g.get("control_values", [control_value_required] * len(ctrls)))
                    if len(ctrls) == 1 and vals[0] == control_value_required:
                        mergeable_ctrl_key = (ctrls[0], g["target"], control_value_required)
                    elif len(ctrls) == 2:
                        mergeable_ctrl_key = (ctrls[0], ctrls[1], g["target"], vals[0], vals[1])

                touched = gate_qudits(g)
                # Flush pending merges that must stay BEFORE this gate.
                # But do NOT flush the exact pending entry we are about to merge into.
                if touched:
                    # flush controlled
                    for key in list(pending_ctrl.keys()):
                        if key == mergeable_ctrl_key:
                            continue
                        if len(key) == 3:
                            c, t, v = key
                            touches = (c in touched or t in touched)
                        elif len(key) == 5:
                            c1, c2, t, v1, v2 = key
                            touches = (c1 in touched or c2 in touched or t in touched)
                        else:
                            raise ValueError("Unsupported pending controlled key format.")
                        if touches:
                            M = pending_ctrl.pop(key)
                            if is_identity(M):
                                continue
                            nm = matrix_to_name(M)
                            if nm is not None and nm in ("0", "I"):
                                continue
                            if nm is None:
                                raise ValueError("Merged controlled matrix not found in gate_dict.")
                            if len(key) == 3:
                                c, t, v = key
                                out.c_custom_gate(M, control=c, target=t, name=nm, control_values=[v])
                            else:
                                c1, c2, t, v1, v2 = key
                                out.cc_custom_gate(M, control1=c1, control2=c2, target=t, name=nm, control_values=[v1, v2])

                    # flush single-qudit
                    for t in list(pending_single.keys()):
                        if t == mergeable_single_target:
                            continue
                        if t in touched:
                            M = pending_single.pop(t)
                            if is_identity(M):
                                continue
                            nm = matrix_to_name(M)
                            if nm is not None and nm in ("0", "I"):
                                continue
                            if nm is None:
                                raise ValueError("Merged single-qudit matrix not found in gate_dict.")
                            out.custom_gate(M, target=t, name=nm)

                # Try to absorb into pending merges (single or controlled) if mergeable.
                # --- Single-qudit merge candidate ---
                if ("target" in g and "control" not in g and "controls" not in g
                    and name in allowed and name in gate_dict):
                    t = g["target"]
                    M = gate_dict[name]
                    if t in pending_single:
                        pending_single[t] = M @ pending_single[t]
                    else:
                        pending_single[t] = M.copy()
                    continue
    
                # --- Single-control controlled merge candidate ---
                # Case A: legacy form with 'control' and 'target'
                if ("control" in g and "target" in g and "controls" not in g
                    and name in allowed and name in gate_dict):
                    c = g["control"]; t = g["target"]
                    key = (c, t, control_value_required)
                    M = gate_dict[name]
                    if key in pending_ctrl:
                        pending_ctrl[key] = M @ pending_ctrl[key]
                    else:
                        pending_ctrl[key] = M.copy()
                    continue
    
                # Case B: value-controlled form with controls / control_values
                if ("controls" in g and "target" in g and name in allowed and name in gate_dict):
                    ctrls = list(g["controls"])
                    vals = list(g.get("control_values", [control_value_required] * len(ctrls)))
                    if len(ctrls) == 1 and vals[0] == control_value_required:
                        c = ctrls[0]; t = g["target"]
                        key = (c, t, control_value_required)
                        M = gate_dict[name]
                        if key in pending_ctrl:
                            pending_ctrl[key] = M @ pending_ctrl[key]
                        else:
                            pending_ctrl[key] = M.copy()
                        continue
                    if len(ctrls) == 2:
                        c1, c2 = ctrls
                        v1, v2 = vals
                        key = (c1, c2, g["target"], v1, v2)
                        M = gate_dict[name]
                        if key in pending_ctrl:
                            pending_ctrl[key] = M @ pending_ctrl[key]
                        else:
                            pending_ctrl[key] = M.copy()
                        continue
                    # if not mergeable, just replay after flushing above
                    replay_gate(g)
                    continue
    
                # Not mergeable -> replay
                replay_gate(g)
    
            flush_all()
            return out