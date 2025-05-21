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
