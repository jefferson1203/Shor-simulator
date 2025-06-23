import math
import random
from sympy import isprime

class Preprocessor:
    def __init__(self, n):
        """
        Initialise le préprocesseur avec le nombre à factoriser.
        """
        self.n = n
        self.is_valid = True
        self.validation_steps = []
        
    def validate_number(self):
        """
        Effectue toutes les validations de prétraitement.
        Retourne True si le nombre est valide pour l'algorithme de Shor.
        """
        self._check_triviality()
        self._check_parity()
        self._check_primality()
        self._check_perfect_power()
        return self.is_valid
        
    def _check_triviality(self):
        """
        Vérifie si le nombre est trivial (1 ou 0).
        """
        if self.n <= 1:
            self.is_valid = False
            self.validation_steps.append(f"Le nombre {self.n} est trivial (≤ 1)")
            return False
        return True
        
    def _check_parity(self):
        """
        Vérifie si le nombre est pair (et différent de 2).
        """
        if self.n % 2 == 0 and self.n != 2:
            self.is_valid = False
            self.validation_steps.append(f"Le nombre {self.n} est pair et différent de 2")
            return False
        return True
        
    def _check_primality(self):
        """
        Vérifie si le nombre est premier.
        """
        if isprime(self.n):
            self.is_valid = False
            self.validation_steps.append(f"Le nombre {self.n} est premier")
            return False
        return True
        
    def _check_perfect_power(self):
        """
        Vérifie si le nombre est une puissance parfaite (a^b).
        """
        for b in range(2, int(math.log2(self.n)) + 1):
            a = round(self.n ** (1/b))
            if a ** b == self.n:
                self.is_valid = False
                self.validation_steps.append(f"Le nombre {self.n} est une puissance parfaite ({a}^{b})")
                return False
        return True
        
    def get_validation_steps(self):
        """
        Retourne les étapes de validation effectuées.
        """
        return self.validation_steps
        
    def find_small_factors(self, a):
        """
        Tente de trouver de petits facteurs en utilisant pgcd(a, n).
        Retourne le facteur s'il est trouvé, sinon None.
        """
        gcd = math.gcd(a, self.n)
        if gcd != 1:
            return gcd
        return None

def find_a(n, exclude=None):
    """
    Trouve une base 'a' appropriée pour l'algorithme de Shor.
    'a' doit être > 1 et premier avec n.
    """
    if exclude is None:
        exclude = []
    
    possible_bases = [i for i in range(2, n) if math.gcd(i, n) == 1 and i not in exclude]
    if not possible_bases:
        raise ValueError(f"Impossible de trouver une base 'a' valide pour N={n} qui n'est pas dans {exclude}")
        
    return random.choice(possible_bases)
