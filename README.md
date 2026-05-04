# 1D Bar Finite Element Solver in Python

A lightweight, fully commented Python script that performs a 1D Finite Element Analysis (FEA) on an axial bar. 

This code is specifically designed as an educational tool for structural engineering and computational mechanics students. It breaks down the "black box" of the Finite Element Method into clear, digestible steps, demonstrating everything from local stiffness matrix generation to global assembly and boundary condition application.

## Features

* **Direct Stiffness Assembly:** Demonstrates how local element matrices are mapped and added to the global stiffness matrix.
* **Matrix Partitioning:** Shows the standard mathematical approach for applying boundary conditions by extracting the free degrees of freedom (DOFs).
* **Automated Validation:** Automatically compares the numerical FEM solution against the exact analytical solution (`PL/AE`) to verify accuracy.
* **Reaction Forces:** Calculates the reaction force at the fixed support using the global stiffness matrix and solved displacements.
* **Zero Dependencies:** Relies entirely on standard matrix math using just `numpy`.

## Prerequisites

To run this script, you only need Python and the NumPy library installed.
```bash
pip install numpy
```
## How It Works
The script is divided into six distinct, heavily commented sections that mirror standard FEM theory:
**1. Define Problem Parameters:** Set the physical properties (Length, Area, Young's Modulus) and the number of elements to mesh.

**2. Initialize Global Matrices:** Pre-allocate memory for the Global Stiffness Matrix [K] and Force vector {F}.

**3. Local Stiffness & Global Assembly:** Create the local stiffness matrix for a linear 1D bar element and "stamp" it into the correct global addresses.

**4. Apply Boundary Conditions:** Fix the left wall (Node 0) and apply the point load to the right-most node. Reduce the matrices to solve only for unknown (free) DOFs.

**5. Solve the System:** Use linear algebra (K * u = F) to solve for nodal displacements.

**6. Post-Processing:** Extract results, calculate support reactions, and validate against the analytical formula.

## Usage
Simply clone the repository and run the script.

```bash
python 1d_bar_fem.py
```
Try modifying the num_elements parameter at the top of the script (e.g., change it from 4 to 10 or 100) to see how the mesh density affects the matrix size, while the final linear displacement remains mathematically exact!

## Example Output
Running the default configuration (4 elements, 10kN load, 1m length) will output the following in your terminal:

```Plaintext
--- 1D Bar FEM Solver (4 Elements) ---

Global Stiffness Matrix [K] before BCs:
[[ 8.00e+09 -8.00e+09  0.00e+00  0.00e+00  0.00e+00]
 [-8.00e+09  1.60e+10 -8.00e+09  0.00e+00  0.00e+00]
 [ 0.00e+00 -8.00e+09  1.60e+10 -8.00e+09  0.00e+00]
 [ 0.00e+00  0.00e+00 -8.00e+09  1.60e+10 -8.00e+09]
 [ 0.00e+00  0.00e+00  0.00e+00 -8.00e+09  8.00e+09]]

Nodal Displacements (meters):
Node 0: 0.00000000 m
Node 1: 0.00000125 m
Node 2: 0.00000250 m
Node 3: 0.00000375 m
Node 4: 0.00000500 m

Reaction Force at Wall (Node 0): -10000.00 N
Analytical Max Displacement: 0.00000500 m
```
