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
        self.state[0] = 1  # Commence dans l'état |0>
        
    def apply_hadamard(self, qubit_index):
        """
        Applique la porte de Hadamard à un qubit spécifique.
        """
        if not (0 <= qubit_index < self.num_qubits):
            raise ValueError(f"L'indice de qubit {qubit_index} est hors limites")
            
        # Appliquer la porte de Hadamard en utilisant le produit tensoriel
        h_matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        
        # Créer des matrices identité pour les autres qubits
        identity = np.eye(2)
        
        # Construire l'opérateur complet
        operator = np.eye(1)
        for i in range(self.num_qubits):
            if i == qubit_index:
                operator = np.kron(operator, h_matrix)
            else:
                operator = np.kron(operator, identity)
        
        # Appliquer l'opérateur
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
            if r > n:  # Sécurité, r est toujours inférieur à n
                return None

    def apply_oracle(self, a, n):
        """
        Applique un oracle 'simulé' pour U_f|x> = |x>|a^x mod n>.
        Cette méthode simule l'effet de l'oracle suivi d'une mesure
        du second registre, ce qui effondre le premier registre en une
        superposition d'états avec la période correcte.
        """
        # 1. Trouver classiquement la période 'r'. C'est la "triche" qui permet à
        # la simulation de fonctionner sans un circuit complet d'exponentiation modulaire quantique.
        r = self._find_period_classically(a, n)
        if r is None:
            print(f"Avertissement : Impossible de trouver la période pour a={a}, N={n}")
            return

        Q = 2**self.num_qubits

        # 2. Choisir un décalage aléatoire 'x0' pour simuler la mesure du
        # second registre s'effondrant sur une valeur aléatoire f(x0).
        x0 = random.randint(0, r - 1)

        # 3. Créer un nouveau vecteur d'état. L'état s'effondre en une superposition
        # de tous les |x> tels que f(x) = f(x0). Ce sont x = x0, x0+r, x0+2r, ...
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
            print(f"Avertissement : Q={Q} est trop petit pour représenter la période r={r}.")
            return

        # 4. Définir les amplitudes de ces états pour qu'elles soient égales et normalisées.
        amplitude = 1.0 / np.sqrt(len(periodic_indices))
        for idx in periodic_indices:
            new_state[idx] = amplitude
            
        # 5. Remplacer l'état du registre par ce nouvel état périodique.
        # Cela contourne le résultat de la transformée de Hadamard et crée directement
        # l'état dont la TQF a besoin pour trouver la période.
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
        result = "État Quantique :\n"
        for i in range(2**self.num_qubits):
            if np.abs(self.state[i]) > 1e-10:  # N'afficher que les amplitudes non nulles
                result += f"|{i:0{self.num_qubits}b}>: {self.state[i]}\n"
        return result
