# 1D Bar Finite Element Solver in Python

A lightweight, fully commented Python script that performs a 1D Finite Element Analysis (FEA) on an axial bar. 

This code is specifically designed as an educational tool for structural engineering and computational mechanics students. It breaks down the "black box" of the Finite Element Method into clear, digestible steps, demonstrating everything from local stiffness matrix generation to global assembly and boundary condition application.

## Features

* **Direct Stiffness Assembly:** Demonstrates how local element matrices are mapped and added to the global stiffness matrix.
* **Matrix Partitioning:** Shows the standard mathematical approach for applying boundary conditions by extracting the free degrees of freedom (DOFs).
* **Automated Validation:** Automatically compares the numerical FEM solution against the exact analytical solution (`PL/AE`) to verify accuracy.
* **Reaction Forces:** Calculates the reaction force at the fixed support using the global stiffness matrix and solved displacements.
* **Zero Dependencies:** Relies entirely on standard matrix math using just `numpy`.

## The Mathematics of the 1D Bar Element

The Finite Element Method (FEM) solves complex physics problems by breaking them down into simpler, discrete "elements." For a 1D axial bar, the governing physics is based on Hooke's Law: $F = k \Delta x$.

### 1. The Element Stiffness Matrix ($\mathbf{k}^e$)
For a single, uniform segment of a bar subjected to axial tension or compression, its physical stiffness $k$ is defined by its material and geometry:
$$k = \frac{EA}{L_e}$$
Where:
*   $E$ = Young's Modulus (material stiffness)
*   $A$ = Cross-sectional Area
*   $L_e$ = Length of the specific element

A 1D element has two nodes (left and right). If we apply a force to pull the right node, the left node feels an equal and opposite pull. This relationship is captured in the **Element Stiffness Matrix**:

$$\mathbf{k}^e = \frac{EA}{L_e} \begin{bmatrix} 1 & -1 \\ 
                                               -1 & 1 \end{bmatrix}$$

This matrix relates the nodal forces ($f_1$, $f_2$) to the nodal displacements ($u_1$, $u_2$) for that single element:
$$\begin{bmatrix} f_1 \\ 
                  f_2 \end{bmatrix} = \frac{EA}{L_e} \begin{bmatrix} 1 & -1 \\
                                                                    -1 & 1 \end{bmatrix} \begin{bmatrix} u_1 \\ 
                                                                                                         u_2 \end{bmatrix}$$

### 2. Global Assembly ($\mathbf{K}_{global}$)
A full bar is made of multiple elements connected end-to-end. To find the behavior of the whole system, we assemble the local matrices into a giant **Global Stiffness Matrix** ($\mathbf{K}$). 

Because elements share nodes, their stiffnesses add together at those shared points. For a 2-element bar (3 nodes total), the assembly looks like this:

$$\mathbf{K}_{global} = \begin{bmatrix} k_1 & -k_1 & 0 \\ -k_1 & k_1 + k_2 & -k_2 \\ 0 & -k_2 & k_2 \end{bmatrix}$$

The middle term ($k_1 + k_2$) represents Node 1, which is shared by Element 1 and Element 2. Physically, it means both elements are resisting movement at that joint.

### 3. The Global Equation
Once assembled, the entire system is represented by the matrix equation:
$$\mathbf{K} \mathbf{U} = \mathbf{F}$$

Where:
*   $\mathbf{K}$ = Global Stiffness Matrix
*   $\mathbf{U}$ = Vector of all nodal displacements (unknowns)
*   $\mathbf{F}$ = Vector of all applied external forces (knowns)

### 4. Boundary Conditions and Partitioning
Before we can solve $\mathbf{K} \mathbf{U} = \mathbf{F}$, we have a mathematical problem: the global matrix $\mathbf{K}$ is singular (its determinant is zero). This means the bar is floating in space and has infinite solutions. We must apply boundary conditions to "lock" it in place.

We partition the matrices into **Free** ($f$) DOFs (nodes that can move) and **Prescribed/Fixed** ($p$) DOFs (nodes bolted to the wall):

$$\begin{bmatrix} \mathbf{K}_{ff} & \mathbf{K}_{fp} \\ \mathbf{K}_{pf} & \mathbf{K}_{pp} \end{bmatrix} \begin{bmatrix} \mathbf{U}_f \\ \mathbf{U}_p \end{bmatrix} = \begin{bmatrix} \mathbf{F}_f \\ \mathbf{F}_p \end{bmatrix}$$

Since our wall is completely fixed, we know the displacement at the wall is zero ($\mathbf{U}_p = \mathbf{0}$). This greatly simplifies the top row of our partitioned equation:

$$\mathbf{K}_{ff} \mathbf{U}_f = \mathbf{F}_f$$

### 5. Solving for Displacements
Now we have a stable, solvable system. We find the unknown displacements ($\mathbf{U}_f$) by taking the inverse of the reduced stiffness matrix and multiplying it by the applied forces:

$$\mathbf{U}_f = \mathbf{K}_{ff}^{-1} \mathbf{F}_f$$

*(Note: In the Python code, we use `np.linalg.solve()` rather than directly calculating the inverse, as it is computationally faster and more stable, but the mathematical result is identical).*

### 6. Calculating Reactions
Finally, we want to know how much force the wall is pushing back with (the reaction force, $\mathbf{F}_p$). We look at the bottom row of our partitioned matrix:

$$\mathbf{F}_p = \mathbf{K}_{pf} \mathbf{U}_f + \mathbf{K}_{pp} \mathbf{U}_p$$

Because $\mathbf{U}_p = 0$, the equation simplifies to:
$$\mathbf{F}_p = \mathbf{K}_{pf} \mathbf{U}_f$$

This exactly matches the step in the code where we take the first row of the global matrix (`K_global[fixed_dof, :]`) and multiply it by the newly solved displacement vector.

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
