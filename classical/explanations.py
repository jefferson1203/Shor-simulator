class Explanations:
    @staticmethod
    def step_1():
        """
        Explication de l'étape 1 : Prétraitement Classique
        """
        return """
        ## Prétraitement Classique
        
        Cette étape est essentielle pour préparer le problème pour l'algorithme de Shor. Voici les points clés :

        1. **Choix du nombre N**
        - N doit être un entier naturel supérieur à 1
        - N doit être impair (sinon on peut le factoriser directement)
        - N ne doit pas être une puissance d'un nombre premier
        - N ne doit pas être premier (sinon il n'a pas de facteurs non triviaux)

        2. **Objectif**
        - Trouver les facteurs premiers de N
        - La factorisation est un problème difficile en informatique classique
        - L'algorithme de Shor utilise la puissance du calcul quantique pour résoudre ce problème efficacement
        """

    @staticmethod
    def step_2():
        """
        Explication de l'étape 2 : Sélection d'une base a
        """
        return """
        ## Sélection d'une base a

        1. **Choix de a**
        - a doit être un nombre entier entre 2 et N-1
        - a doit être premier avec N (PGCD(a, N) = 1)
        - On choisit a aléatoirement parmi les nombres premiers avec N

        2. **Pourquoi cette étape ?**
        - a sera utilisé pour construire la fonction périodique f(x) = a^x mod N
        - La période de cette fonction est la clé pour trouver les facteurs de N
        - Si on trouve un a qui partage un facteur avec N, on a déjà trouvé un facteur
        """

    @staticmethod
    def step_3():
        """
        Explication de l'étape 3 : Simulation Quantique
        """
        return """
        ## Simulation Quantique

        1. **Circuit Quantique**
        - Le circuit utilise des qubits pour représenter les nombres
        - Les portes quantiques (Hadamard, Oracle, QFT) transforment les états
        - Chaque transformation modifie la superposition des états

        2. **Portes Quantiques**
        - **Hadamard (H)** : Crée une superposition d'états
        - **Oracle (O)** : Encode la fonction périodique
        - **QFT (Transformée de Fourier Quantique)** : Révèle la période
        - **Mesure (M)** : Collaps de l'état quantique

        3. **Objectif**
        - Trouver une approximation de la période r de la fonction f(x) = a^x mod N
        - La période est cachée dans l'état quantique final
        """

    @staticmethod
    def step_4():
        """
        Explication de l'étape 4 : Post-traitement Classique
        """
        return """
        ## Post-traitement Classique

        1. **Continued Fractions**
        - Utilisées pour trouver la période exacte r
        - Convertissent l'approximation obtenue en une fraction continue
        - Les convergents donnent des fractions proches de la période

        2. **Pourquoi cette étape ?**
        - La mesure quantique donne une approximation
        - Les fractions continues permettent de trouver la période exacte
        - La période r est cruciale pour trouver les facteurs de N
        """

    @staticmethod
    def step_5():
        """
        Explication de l'étape 5 : Extraction des Facteurs
        """
        return """
        ## Extraction des Facteurs

        1. **Formule des Facteurs**
        - Si r est pair et a^(r/2) ≠ -1 mod N
        - Les facteurs sont obtenus avec : gcd(a^(r/2) ± 1, N)

        2. **Pourquoi ça marche ?**
        - Si r est la période de f(x) = a^x mod N
        - a^r ≡ 1 mod N
        - (a^(r/2) + 1)(a^(r/2) - 1) ≡ 0 mod N
        - Un des facteurs partage un facteur commun avec N
        """

    @staticmethod
    def quantum_gates():
        """
        Explication des portes quantiques
        """
        return """
        ## Portes Quantiques

        1. **Hadamard (H)**
        - Crée une superposition égale de tous les états
        - Transforme |0⟩ en (|0⟩ + |1⟩)/√2
        - Transforme |1⟩ en (|0⟩ - |1⟩)/√2

        2. **Oracle (O)**
        - Encode la fonction périodique f(x) = a^x mod N
        - Transforme |x⟩|0⟩ en |x⟩|f(x)⟩
        - Crée des corrélations entre les qubits

        3. **QFT (Transformée de Fourier Quantique)**
        - Révèle la structure périodique
        - Transforme la superposition en une autre base
        - La période apparaît dans l'état final

        4. **Mesure (M)**
        - Collaps de l'état quantique
        - Donne une approximation de la période
        - Plus de qubits = meilleure précision
        """
