import numpy as np

# ==========================================
# 1. DEFINE PROBLEM PARAMETERS
# ==========================================
L = 1.0        # Total length of the bar (meters)
A = 0.01       # Cross-sectional area (m^2)
E = 200e9      # Young's Modulus for Steel (N/m^2)
Load = 10000   # Axial force applied at the end (Newtons)

num_elements = 4  # Try changing this to see how the mesh refines!
num_nodes = num_elements + 1
Le = L / num_elements  # Length of a single element

print(f"--- 1D Bar FEM Solver ({num_elements} Elements) ---")

# ==========================================
# 2. INITIALIZE GLOBAL MATRICES
# ==========================================
# Create empty global stiffness matrix (K) and Force vector (F)
K_global = np.zeros((num_nodes, num_nodes))
F_global = np.zeros((num_nodes, 1))

# ==========================================
# 3. LOCAL STIFFNESS & GLOBAL ASSEMBLY
# ==========================================
# k = (A*E/L) * [[1, -1], [-1, 1]]
# This assumes linear shape functions (N1 = 1 - x/L, N2 = x/L)
k_local = (A * E / Le) * np.array([[ 1.0, -1.0], 
                                   [-1.0,  1.0]])

# Assembly Loop
for e in range(num_elements):
    # Element connectivity: element 'e' connects node 'e' and node 'e+1'
    n1 = e
    n2 = e + 1
    
    # Add local stiffness to the correct global positions
    K_global[n1:n2+1, n1:n2+1] += k_local

print("\nGlobal Stiffness Matrix [K] before BCs:")
print(np.array2string(K_global, precision=2, formatter={'float_kind':lambda x: "%.2e" % x}))

# ==========================================
# 4. APPLY BOUNDARY CONDITIONS 
# ==========================================
# We want to fix the left wall (Node 0), so displacement u[0] = 0
# We apply the 'Load' to the right-most node.
F_global[-1, 0] = Load 

# Define Free and fixed DOFs
fixed_dof = 0
free_dofs = list(range(1, num_nodes)) # Nodes 1, 2, 3, 4 are free to move

# Partition the Matrix (Extract K_ff and F_f)
K_ff = K_global[np.ix_(free_dofs, free_dofs)]
F_f = F_global[free_dofs]

# ==========================================
# 5. SOLVE THE SYSTEM
# ==========================================
# Initialize an array to hold all displacements (starts at zero)
u_global = np.zeros((num_nodes, 1))

# Solve the reduced system: K_ff * u_f = F_f
u_free = np.linalg.solve(K_ff, F_f)

# Put the solved free displacements back into the global displacement vector
u_global[free_dofs] = u_free

# ==========================================
# 6. POST-PROCESSING (Results)
# ==========================================
print("\nNodal Displacements (meters):")
for i in range(num_nodes):
    print(f"Node {i}: {u_global[i,0]:.8f} m")

# Calculate Reaction Force at the wall (F_p = K_pf * u_f + K_pp * u_p)
# Since u_p (displacement at wall) is 0, F_reaction = K[0,:] * u_global
reaction_force = np.dot(K_global[fixed_dof, :], u_global)[0]
print(f"\nReaction Force at Wall (Node 0): {reaction_force:.2f} N")

# Validation check: Total displacement of a uniform bar should be PL/AE
analytical_u_max = (Load * L) / (A * E)
print(f"Analytical Max Displacement: {analytical_u_max:.8f} m")
