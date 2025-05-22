# QuTiP-MRL: A Library for Multiple-Valued Reversible Logic Simulations

This repository is structured as follows:

- `qutip_mrl` library main directory contains the core functionalities of the QuTiP-MRL library;
    - `qudit_circuit.py` provides the core functionalities of QuTiP-MRL library, allowing users for the design, simulation, and rendering of quantum circuits; 
    - `ascii_gates.py` contains the definition of ASCII representation of each of the gates provided by our library (i.e., the ternary ones);
    - `qutrit_matrices.py` defines matrices for ternary logic gates;
    - `setup.py` defines the configuration and dependencies for using QuTiP-MRL;
- `examples` contains several examples of usage of the QuTiP-MRL library.

## Launching the examples

To run the examples, you can use the following command - to be executed from the root of the folder - in your terminal:

```bash
python -m examples.example_name
``` 

where `example_name` is the name of the example you want to run. For instance, to run the example `1_qutrit_gates.py`, you would use:

```bash
python -m examples.1_qutrit_gates
```

## How to use the library

To use the QuTiP-MRL library, you can import the `QuditCircuit` class from the `qutip_mrl` module. Here is a simple example of how to create a qudit circuit and add gates to it:

```python
from qutip_mrl.qudit_circuit import QuditCircuit

circuit = QuditCircuit(4)  # Create a qudit circuit with 4 qutrits
circuit2 = QuditCircuit(3, 4)  # Create a qudit circuit with 3 qudits having four levels each

# Adding a controlled +2 gate, with qutrit 1 as control and qutrit 0 as target
circuit.c_plus2(1,0)
# Adding a shift gate to qutrit 0
circuit.plus2(0)

# Adding a custom gate to the quaternary circuit to the qudit 0
zero_three_one = np.array([
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [1, 0, 0, 0]
])
circuit2.custom_gate(zero_three_one,0,'031')
# Adding a custom controlled gate to the qudit 0 for the quaternary circuit. The gate is controlled by qudit 1
circuit2.c_custom_gate(zero_three_one,0,1,'031')

# Simulating the circuit with two different modes
circuit.simulate_fullmatrix()
circuit.simulate_einsum()

# Rendering the circuit
circuit.draw()              # ASCII mode
circuit.draw('mpl')         # Matplotlib mode
```
