class ContinuedFraction:
    def __init__(self, number, max_depth=100):
        """
        Initialise une fraction continue à partir d'un nombre.
        
        Args:
            number: Le nombre pour lequel calculer la fraction continue
            max_depth: Le nombre maximum d'itérations pour éviter les boucles infinies.
        """
        self.number = number
        self.max_depth = max_depth
        self.coefficients = []
        self._compute_coefficients()

    def _compute_coefficients(self):
        """
        Calcule les coefficients de la fraction continue.
        """
        num = self.number
        # On boucle tant que le nombre a une partie fractionnaire et qu'on n'a pas atteint la limite
        while len(self.coefficients) < self.max_depth:
            a = int(num)
            self.coefficients.append(a)
            # Si le nombre est un entier, on a terminé.
            if abs(num - a) < 1e-9: # Comparaison de flottants sécurisée
                break
            num = 1.0 / (num - a)

    def get_coefficients(self):
        """
        Retourne les coefficients de la fraction continue.
        
        Returns:
            list: Les coefficients de la fraction continue
        """
        return self.coefficients

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de la fraction continue.
        """
        return f"[{', '.join(map(str, self.coefficients))}]"


class ContinuedFractionConvergents:
    def __init__(self, coefficients):
        """
        Initialise les convergents d'une fraction continue.
        
        Args:
            coefficients: Les coefficients de la fraction continue
        """
        self.coefficients = coefficients
        self.convergents = []
        self._compute_convergents()

    def _compute_convergents(self):
        """
        Calcule les convergents de la fraction continue en utilisant la formule de récurrence standard.
        """
        if not self.coefficients:
            return

        h_minus_2, k_minus_2 = 0, 1
        h_minus_1, k_minus_1 = 1, 0

        for a in self.coefficients:
            h_n = a * h_minus_1 + h_minus_2
            k_n = a * k_minus_1 + k_minus_2
            
            self.convergents.append((h_n, k_n))
            
            # Mettre à jour les valeurs pour la prochaine itération
            h_minus_2, k_minus_2 = h_minus_1, k_minus_1
            h_minus_1, k_minus_1 = h_n, k_n

    def get_convergents(self):
        """
        Retourne les convergents calculés.
        
        Returns:
            list: Liste des convergents sous forme de tuples (numérateur, dénominateur)
        """
        return self.convergents

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne des convergents.
        """
        return ', '.join(f"{h}/{k}" for h, k in self.convergents)
