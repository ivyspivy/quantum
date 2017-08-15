#### READ ME ###
# These exercises can be found on http://pyquil.readthedocs.io/en/latest/getting_started.html#exercises
# I have not yet done the single-shot Grover's algorithm

import pyquil.quil as pq
import pyquil.api as api
from pyquil.gates import *
import numpy as np

# open a synchronous connection
qvm = api.SyncConnection()

def listToInt(list):
# will convert a list of bits into its integer representation
    return int(''.join(str(n) for n in list), 2) # binary is base 2

def throw_octahedral_die():
    # returns 1-8
    p = pq.Program()
    cRegister = [0,1,2]

    #We will put all 3 qubits into superposition
    p.inst(H(0), H(1), H(2))

    #Then we will measure each qubit
    p.measure(0, 0)
    p.measure(1, 1)
    p.measure(2, 2)
    bits = qvm.run(p, cRegister)
    return listToInt(bits[0]) + 1 # we need to add 1 because our program returns 0-7

def throw_polyhedral_die(num_sides):
    # return the result of throwing a num_sides sided die by running a quantum program
    p = pq.Program()
    import math
    numBits = math.ceil(math.log(num_sides,2)) #calculating the number of bits needed
    cRegister = list(range(numBits)) #making a classical register with the number of bits
    for i in range(numBits):
        p.inst(H(i)) # put every bit into superposition
    for i in range(numBits):
        p.measure(i,i) # measure every bit into its classical register
    bits = qvm.run(p, cRegister)
    num = listToInt(bits[0]) + 1
    # since we can get integers above the num_sides, we keep calling the method
    # until we get an integer within the range.
    if(num > num_sides):
        return throw_polyhedral_die(num_sides)
    else:
        return num

def controlled(matrix):
    # takes in a 2x2 matrix U representing a single qubit operator
    # return a 4x4 matrix that is a controlled variant of U
    # first argument being control qubit

    # The mathematics can be found on the Wikipedia page
    # https://en.wikipedia.org/wiki/Quantum_gate#Controlled_gates
    # under Controlled gates.
    return np.array([[1,0,0,0],[0,1,0,0], [0, 0, matrix[0,0], matrix[0,1]], [0,0,matrix[1,0], matrix[1,1]]])

p = pq.Program()
cRegister = [0,1]
p.defgate("CY", controlled(np.array([[0, -1j], [1j, 0]])))
p.inst(H(0))
p.inst(("CY", 0, 1))
wvf, _ = qvm.wavefunction(p)
print(wvf)

# print(throw_octahedral_die())
# print(throw_polyhedral_die(30))
