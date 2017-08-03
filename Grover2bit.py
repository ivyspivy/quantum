# I am using IBM's quantum computing SDK and API in python.
# You can get it here: https://github.com/IBM/qiskit-sdk-py
# To use the API, you need a IBM QX account, which is free at
# https://quantumexperience.ng.bluemix.net/qx

import sys
sys.path.append("../../") # solve the relative dependencies if you clone QISKit from the Git repo and use like a global.

from qiskit import QuantumProgram
import Qconfig


#Initialize a QuantumProgram object, with a quantum and classical register holding 2 bits
qProgram = QuantumProgram()
qRegister = qProgram.create_quantum_registers("qRegister", 2)
cRegister = qProgram.create_classical_registers("cRegister", 2)

#create a quantum circuit - arguments: name, [quantum registers], [classical registers]
qCircuit = qProgram.create_circuit("qCircuit", ["qRegister"], ["cRegister"])

#ALTERNATIVE METHOD OF CREATING THE EQUIVALENT CIRCUIT#
# qSpecs = {
#   "circuits": [{"name": "qCircuit",
#               "quantum_registers": [{"name": "qRegister", "size": 2}],
#               "classical_registers": [{"name": "cRegister", "size": 2}]
#    }]
# }
# qProgram = QuantumProgram(specs = qSpecs)

#Grover's Algorithm
# This is a search algorithm for quantum computers.
# This example uses 2 qubits, for a total of 2^2 = 4 different states.
# Note that for each different correct state, the quantum oracle must
# change to reflect that the oracle acts on the correct state.
# In this algorithm, I mention the amplitudes of the correct state.
# These amplitudes squared represent the probability that you observe
# that particular state. Grover's algorithm works because it acts on
# the amplitudes of all the possible states.

# First, we put all qubits in superposition using the Hadamard gate
# For n qubits, there are 2^n possible states, and using the H-gate
# on all the qubits will cause all the states to be equally observed.
# In other words, the amplitudes of all the states are equal.
qCircuit.h(qRegister[0])
qCircuit.h(qRegister[1])

#Oracle:
# The oracle is a quantum black box* that negates the amplitude** of the correct state. In this
# case, the correct state is going to be the first position, 00.
# By negating the amp. of the correct state, the avg. amp. of the states will lower.
# *The black box can be observed through inputs and outputs
# ** To negate the amplitude, we apply a rotation of pi around the Z axis.

qCircuit.s(qRegister[0])    # These s gates actually influence what the oracle will
qCircuit.s(qRegister[1])    # interpret as the correct state. In this case, each s gate is a '0'
qCircuit.cz(qRegister[0],qRegister[1])
qCircuit.s(qRegister[0])    # and the correct state is 00.
qCircuit.s(qRegister[1])    # The s gates are placed around the control-Z gate in the same order.

# You can comment out the s gates (make sure to get both sides of the control-Z gate)
# to change the oracle's correct state. You can play around with it to see how the oracle
# changes the outputs!



# Diffusion transform
# This circuit will perform an inversion of the amplitudes about the average amplitude.
# This will cause the correct state to be amplified (and be positive again), while the
# other states will be transformed into smaller amplitudes.
# The diffusion transform is the same no matter which correct state you want to act on.
qCircuit.h(qRegister[0])
qCircuit.h(qRegister[1])
qCircuit.x(qRegister[0])
qCircuit.x(qRegister[1])
qCircuit.cz(qRegister[0],qRegister[1])
qCircuit.x(qRegister[0])
qCircuit.x(qRegister[1])
qCircuit.h(qRegister[0])
qCircuit.h(qRegister[1])


# If you are using this algorithm for a larger register with n qubits, you will need to apply
# the oracle and diffusion transform sqrt(N) times, where N = 2^n. Therefore,
# Grover's algorithm is O(sqrt(N)), which is quadratically faster than a classical
# unordered search algorithm. For a deeper analysis into Grover's algorithm, please go to
# https://people.cs.umass.edu/~strubell/doc/quantum_tutorial.pdf. This article, written by
# Emma Strubell, is very informative if you are a beginner to quantum like me!

# Now we measure the qubits from the quantum register to the classical register.
qCircuit.measure(qRegister[0], cRegister[0])
qCircuit.measure(qRegister[1], cRegister[1])


# Now we have to compile and execute our program. The code below was taken
# from the tutorial section of https://github.com/IBM/qiskit-sdk-py.

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
