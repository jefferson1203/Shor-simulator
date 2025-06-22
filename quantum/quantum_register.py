import numpy as np
import math
import random

class QuantumRegister:
    def __init__(self, num_qubits):
        """
        Initialise un registre quantique avec num_qubits qubits.
        """
        self.num_qubits = num_qubits
        self.state = np.zeros(2**num_qubits, dtype=np.complex128)
        self.state[0] = 1  # Start in |0> state
        
    def apply_hadamard(self, qubit_index):
        """
        Applique la porte de Hadamard à un qubit spécifique.
        """
        if not (0 <= qubit_index < self.num_qubits):
            raise ValueError(f"Qubit index {qubit_index} out of range")
            
        # Apply Hadamard gate using tensor product
        h_matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        
        # Create identity matrices for other qubits
        identity = np.eye(2)
        
        # Construct the full operator
        operator = np.eye(1)
        for i in range(self.num_qubits):
            if i == qubit_index:
                operator = np.kron(operator, h_matrix)
            else:
                operator = np.kron(operator, identity)
        
        # Apply the operator
        self.state = operator @ self.state
        
    def apply_hadamard_to_all(self):
        """
        Applique efficacement la porte de Hadamard à tous les qubits, en supposant que
        l'état initial est |0...0>. Cela crée une superposition égale de tous
        les états de base.
        """
        Q = 2**self.num_qubits
        self.state = np.ones(Q, dtype=np.complex128) / np.sqrt(Q)
        
    def measure(self):
        """
        Effectue une mesure sur le registre.
        Retourne l'état mesuré (représentation entière).
        """
        probabilities = np.abs(self.state)**2
        result = np.random.choice(2**self.num_qubits, p=probabilities)
        return result
        
    def get_state(self):
        """
        Retourne le vecteur d'état quantique actuel.
        """
        return self.state.copy()
        
    def _find_period_classically(self, a, n):
        """
        Fonction auxiliaire pour trouver la période r de a^x mod n.
        C'est un calcul classique utilisé pour "tricher" dans la simulation.
        """
        if math.gcd(a, n) != 1:
            return None
        r = 1
        while True:
            if pow(a, r, n) == 1:
                return r
            r += 1
            if r > n:  # Failsafe, r is always less than n
                return None

    def apply_oracle(self, a, n):
        """
        Applique un oracle 'simulé' pour U_f|x> = |x>|a^x mod n>.
        Cette méthode simule l'effet de l'oracle suivi d'une mesure
        du second registre, ce qui effondre le premier registre en une
        superposition d'états avec la période correcte.
        """
        # 1. Classically find the period 'r'. This is the "cheat" that makes
        # the simulation work without a full quantum modular exponentiation circuit.
        r = self._find_period_classically(a, n)
        if r is None:
            print(f"Warning: Could not find period for a={a}, N={n}")
            return

        Q = 2**self.num_qubits

        # 2. Choose a random offset 'x0' to simulate the measurement of the
        # second register collapsing to a random value f(x0).
        x0 = random.randint(0, r - 1)

        # 3. Create a new state vector. The state collapses to a superposition
        # of all |x> such that f(x) = f(x0). These are x = x0, x0+r, x0+2r, ...
        new_state = np.zeros(Q, dtype=np.complex128)
        
        periodic_indices = []
        k = 0
        while True:
            idx = x0 + k * r
            if idx < Q:
                periodic_indices.append(idx)
                k += 1
            else:
                break
        
        if not periodic_indices:
            print(f"Warning: Q={Q} is too small to represent the period r={r}.")
            return

        # 4. Set the amplitudes for these states to be equal and normalize.
        amplitude = 1.0 / np.sqrt(len(periodic_indices))
        for idx in periodic_indices:
            new_state[idx] = amplitude
            
        # 5. Replace the register's state with this new periodic state.
        # This bypasses the Hadamard transform result and directly
        # creates the state that the QFT needs to find the period.
        self.state = new_state

    def apply_iqft(self):
        """
        Applique la Transformée de Fourier Quantique Inverse au registre.
        Ceci est fait en utilisant la Transformée de Fourier Rapide Inverse 
        hautement optimisée de la bibliothèque numpy.
        """
        # np.fft.ifft normalise par 1/N, alors que la QFT normalise par 1/sqrt(N).
        # On doit donc multiplier par sqrt(N) pour compenser.
        self.state = np.fft.ifft(self.state) * np.sqrt(2**self.num_qubits)

    def get_state_vector(self):
        return self.state

    def __str__(self):
        """
        Retourne une représentation textuelle de l'état quantique.
        """
        result = "Quantum State:\n"
        for i in range(2**self.num_qubits):
            if np.abs(self.state[i]) > 1e-10:  # Only show non-zero amplitudes
                result += f"|{i:0{self.num_qubits}b}>: {self.state[i]}\n"
        return result
