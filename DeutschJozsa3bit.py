# I am using IBM's quantum computing SDK and API in python.
# You can get it here: https://github.com/IBM/qiskit-sdk-py
# To use the API, you need a IBM QX account, which is free at
# https://quantumexperience.ng.bluemix.net/qx

import sys
sys.path.append("../../") # solve the relative dependencies if you clone QISKit from the Git repo and use like a global.

from qiskit import QuantumProgram
import Qconfig


#Initialize a QuantumProgram object, with a quantum and classical register holding 3 bits
qProgram = QuantumProgram()
n = 3
qRegister = qProgram.create_quantum_registers("qRegister", n)
cRegister = qProgram.create_classical_registers("cRegister", n)
qCircuit = qProgram.create_circuit("qCircuit", ["qRegister"], ["cRegister"])


# First, we apply the Hadamard gates to every qubit
# Now, all the possible states are equally likely to be observed
for i in range(n):
    qCircuit.h(qRegister[i])

# With every possible state, we will apply the Oracle*. In this case,
# the oracle is a balanced function f(x) = x0 ⊕ x1x2. (⊕ means XOR)
# To make a constant function, you can either comment out the below oracle
# or make your own constant function!
# *an oracle analogous to calling a function in a classical computer. Note
# that for a different function, a new oracle needs to be built.

qCircuit.z(qRegister[0])
qCircuit.cz(qRegister[1], qRegister[2])

# Now, we apply the H-gate to all the qubits again.
for i in range(n):
    qCircuit.h(qRegister[i])


# That's it for this algorithm! Measure the qubits into the classical registers.
# For a constant function, we expect a 100% chance of observing all 0s. (if simulated)
# For a balanced function, we expect anything else.
# This means that when we examine the probability of measuring all 0s, we get 1 for a constant
# function (due to constructive interference) and 0 for a balanced function (destructed interference).
# This is a deterministic algorithm.
# The math behind this algorithm is on IBM's QX Full user guide:
# https://quantumexperience.ng.bluemix.net/qx/tutorial?sectionId=8443c4f713521c10b1a56a533958286b&pageIndex=3
# The biggest resource that helped my understand constructive/destructive interference in the algorithm was this video:
# https://www.youtube.com/watch?v=mGqyzZ-fnnY
# This algorithm can evaluate the function in one call, which is exponentially faster than
# a classical computer's 2^(n-1) + 1.
qCircuit.measure(qRegister[0], cRegister[0])
qCircuit.measure(qRegister[1], cRegister[1])
qCircuit.measure(qRegister[2], cRegister[2])

device = 'ibmqx_qasm_simulator' # Backend to execute your program, in this case it is the online simulator
circuits = ["qCircuit"]  # Group of circuits to execute
qProgram.compile(circuits, "local_qasm_simulator") # Compile your program

# Run your program in the device and check the execution result every 2 seconds
result = qProgram.run(wait=2, timeout=240)

print(qProgram.get_counts("qCircuit"))

# USE THE BLOCK OF CODE BELOW IF YOU WANT TO RUN ON AN ACTUAL QUANTUM COMPUTER
# It's cool running on an actual quantum computer, but keep in mind that
# decoherence and other environmental noise causes error.

# device = 'ibmqx2'   # Backend where you execute your program; in this case, on the Real Quantum Chip online
# circuits = ["qCircuit"]   # Group of circuits to execute
# shots = 1024           # Number of shots to run the program (experiment); maximum is 8192 shots.
# max_credits = 3          # Maximum number of credits to spend on executions.

# result = qProgram.execute(circuits, device, shots, max_credits=3, wait=10, timeout=240)
# print(qProgram.get_counts("Circuit"))
