import streamlit as st
import numpy as np
import math
import random
import pandas as pd

from quantum.quantum_register import QuantumRegister
from quantum.circuit_visualizer_clean import CircuitVisualizer
from classical.preprocessing import find_a
from classical.continued_fraction import ContinuedFraction, ContinuedFractionConvergents
from classical.explanations import Explanations

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

class ShorSimulator:
    def __init__(self, n=15):
        self.n = n
        self.a = find_a(self.n)
        self.current_step = 1
        self.is_auto_running = False
        
        # Attributs pour une seule exécution
        self.quantum_register = None
        self.circuit_visualizer = None
        self.measurement = None
        self.state_before_measurement = None
        self.period_search_done = False
        self.period = None
        self.factors_calculated = False
        self.factor1 = None
        self.factor2 = None
        self.convergents = None
        self.fraction = None

    def _reset_for_new_run(self):
        """Crée une nouvelle simulation pour essayer une nouvelle base 'a'."""
        new_sim = ShorSimulator(self.n)
        new_sim.is_auto_running = self.is_auto_running
        new_sim.a = find_a(self.n, exclude=[self.a])
        new_sim.current_step = 2 # Recommencer à l'étape 2 avec la nouvelle base
        st.session_state.simulator = new_sim

    def _reset_quantum_part(self):
        """Réinitialise les résultats de la simulation quantique pour une nouvelle tentative."""
        self.quantum_register = None
        self.circuit_visualizer = None
        self.measurement = None
        self.state_before_measurement = None
        self.period_search_done = False
        self.period = None
        self.factors_calculated = False
        self.convergents = None
        self.fraction = None
        self.current_step = 3

    # --- Logique des étapes de l'algorithme ---
    def run_step(self, step):
        steps = {
            1: self._run_step_1,
            2: self._run_step_2,
            3: self._run_step_3,
            4: self._run_step_4,
            5: self._run_step_5,
        }
        steps[step]()

    def _run_step_1(self):
        st.header("Étape 1: Prétraitement Classique")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.expander("Cliquez pour voir l'explication de cette étape"):
            st.markdown(Explanations.step_1())
        st.write(f"Le nombre à factoriser est **{self.n}**. La base de départ choisie est **a = {self.a}**.")
        if st.button("Vérifier la base et continuer"):
            self.current_step = 2
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    def _run_step_2(self):
        st.header("Étape 2: Vérification de la Périodicité")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.expander("Cliquez pour voir l'explication de cette étape"):
            st.markdown(Explanations.step_2())

        is_coprime, is_even_period = self._check_periodicity()

        if not is_coprime:
            st.error(f"**Échec :** {self.a} et {self.n} ne sont pas premiers entre eux. Le facteur est **{math.gcd(self.a, self.n)}**.")
            st.balloons()
        elif is_even_period:
            st.success(f"**Succès :** La base a={self.a} est valide. La période est paire.")
            if st.button("Passer à l'étape 3 (Simulation Quantique)"):
                self.current_step = 3
                st.rerun()
        else:
            st.warning(f"**Échec :** La période pour a={self.a} est impaire.")
            if st.button("Essayer une nouvelle base"):
                self._reset_for_new_run()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    def _run_step_3(self):
        st.header("Étape 3: Simulation Quantique")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        num_qubits = int(np.ceil(np.log2(self.n**2)))
        if self.quantum_register is None: self.quantum_register = QuantumRegister(num_qubits)
        if self.circuit_visualizer is None: self.circuit_visualizer = CircuitVisualizer(num_qubits)

        col1, col2 = st.columns([2, 1])
        with col1:
            if self.is_auto_running:
                self._perform_quantum_simulation()
                self.current_step = 4
                st.rerun()
            elif self.measurement is None:
                self._manual_quantum_gates(num_qubits)
            else:
                st.success(f"Mesure obtenue: **{self.measurement}**")
                st.markdown("##### Distribution de probabilité avant mesure")
                if self.state_before_measurement is not None:
                    prob_fig_before = self.circuit_visualizer.plot_probabilities(self.state_before_measurement)
                    if prob_fig_before:
                        st.plotly_chart(prob_fig_before, use_container_width=True)

                st.markdown("##### État après mesure")
                # Créer un vecteur d'état où seul l'état mesuré a une probabilité de 1
                final_state_vector = np.zeros_like(self.state_before_measurement)
                final_state_vector[self.measurement] = 1
                prob_fig_after = self.circuit_visualizer.plot_probabilities(final_state_vector)
                if prob_fig_after:
                    st.plotly_chart(prob_fig_after, use_container_width=True)

        with col2:
            st.subheader("Circuit Quantique")
            circuit_fig = self.circuit_visualizer.show_circuit()
            st.plotly_chart(circuit_fig, use_container_width=True)

        if self.measurement is not None and not self.is_auto_running:
            if st.button("Passer à l'étape 4 (Recherche de Période)"):
                self.current_step = 4
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    def _run_step_4(self):
        st.header("Étape 4: Recherche de la Période")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.expander("Cliquez pour voir l'explication de cette étape"):
            st.markdown(Explanations.step_4())

        if not self.period_search_done: self._find_period()

        with st.expander("Détails du calcul de la fraction continue"):
            if self.fraction is not None:
                st.write(f"Fraction s/Q calculée à partir de la mesure: {self.fraction:.5f}")
            if self.convergents is not None:
                st.write("Convergents (h/k) de la fraction continue:")
                df_convergents = pd.DataFrame(self.convergents, columns=["h (numérateur)", "k (dénominateur)"])
                st.dataframe(df_convergents.astype(str))

        if self.period:
            st.success(f"**Succès :** La période 'r' trouvée est **{self.period}**.")
            if self.is_auto_running:
                self.current_step = 5
                st.rerun()
            elif st.button("Passer à l'étape 5 (Calcul des Facteurs)"):
                self.current_step = 5
                st.rerun()
        else:
            st.error("**Échec :** La recherche de la période a échoué. Cela peut arriver si la mesure est 0 ou donne une mauvaise approximation de la période.")
            if self.is_auto_running:
                self._reset_for_new_run()
                st.rerun()
            else:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Réessayer la mesure quantique"):
                        self._reset_quantum_part()
                        st.rerun()
                with col2:
                    if st.button("Essayer une nouvelle base (a)"):
                        self._reset_for_new_run()
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    def _run_step_5(self):
        st.header("Étape 5: Calcul des Facteurs")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.expander("Cliquez pour voir l'explication de cette étape"):
            st.markdown(Explanations.step_5())

        if not self.factors_calculated: self._calculate_factors()

        if self.factor1 and self.factor2 and self.factor1 * self.factor2 == self.n:
            st.balloons()
            st.success(f"## Les facteurs de {self.n} sont **{self.factor1}** et **{self.factor2}**!")
        else:
            st.warning("**Échec :** Le calcul a donné un facteur trivial.")
            if self.is_auto_running:
                self._reset_for_new_run()
                st.rerun()
            elif st.button("Essayer une nouvelle base"):
                self._reset_for_new_run()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Méthodes de calcul auxiliaires ---
    def _check_periodicity(self):
        is_coprime = math.gcd(self.a, self.n) == 1
        if not is_coprime: return False, False
        r = 1
        while pow(self.a, r, self.n) != 1: r += 1
        return True, r % 2 == 0

    def _manual_quantum_gates(self, num_qubits):
        with st.expander("Explication des portes quantiques", expanded=True):
            st.markdown(Explanations.quantum_gates())
        if st.button("Appliquer Hadamard"):
            self.quantum_register.apply_hadamard_to_all()
            self.circuit_visualizer.add_gate('H', list(range(num_qubits)), 1)
            st.rerun()
        if st.button("Appliquer Oracle"):
            self.quantum_register.apply_oracle(self.a, self.n)
            self.circuit_visualizer.add_gate('O', list(range(num_qubits)), 3)
            st.rerun()
        if st.button("Appliquer IQFT"):
            self.quantum_register.apply_iqft()
            self.circuit_visualizer.add_gate('IQFT', list(range(num_qubits)), 5)
            st.rerun()
        if st.button("Mesurer"):
            self._perform_measurement(num_qubits)
            st.rerun()

    def _perform_measurement(self, num_qubits):
        self.state_before_measurement = self.quantum_register.get_state_vector()

        max_retries = 20 # Sécurité pour éviter une boucle infinie
        measurement = 0
        for i in range(max_retries):
            measurement = self.quantum_register.measure()
            if measurement != 0:
                break # On a trouvé une mesure potentiellement utile
        
        self.measurement = measurement
        self.circuit_visualizer.add_gate('M', list(range(num_qubits)), 7)

    def _perform_quantum_simulation(self):
        num_qubits = self.quantum_register.num_qubits
        self.quantum_register.apply_hadamard_to_all()
        self.circuit_visualizer.add_gate('H', list(range(num_qubits)), 1)
        self.quantum_register.apply_oracle(self.a, self.n)
        self.circuit_visualizer.add_gate('O', list(range(num_qubits)), 3)
        self.quantum_register.apply_iqft()
        self.circuit_visualizer.add_gate('IQFT', list(range(num_qubits)), 5)
        self._perform_measurement(num_qubits)

    def _find_period(self):
        self.period_search_done = True
        num_qubits = self.quantum_register.num_qubits
        self.fraction = self.measurement / (2**num_qubits)
        cf = ContinuedFraction(self.fraction)
        self.convergents = ContinuedFractionConvergents(cf.get_coefficients()).get_convergents()
        for h, k in self.convergents:
            if k < self.n and pow(self.a, k, self.n) == 1:
                self.period = k
                return

    def _calculate_factors(self):
        self.factors_calculated = True
        if self.period is None or self.period % 2 != 0:
            self.factor1, self.factor2 = None, None
            return
        x = pow(self.a, self.period // 2, self.n)
        if x == self.n - 1:
            self.factor1, self.factor2 = None, None
            return
        self.factor1 = math.gcd(x + 1, self.n)
        self.factor2 = math.gcd(x - 1, self.n)



# --- Exécution principale de l'application ---
def main():
    st.set_page_config(layout="wide", page_title="Simulateur d'Algorithme de Shor", page_icon="utc/image.png")
    load_css('style.css')

    if 'simulator' not in st.session_state:
        st.session_state.simulator = ShorSimulator()
    simulator = st.session_state.simulator

    st.sidebar.title("Simulateur d'Algorithme de Shor")
    st.sidebar.markdown("---_Tx n°7708 Simulateur pour l'algorithme de Shor_---")
    
    new_n = st.sidebar.number_input("Nombre à factoriser (N)", min_value=15, max_value=100, value=simulator.n, step=2)
    if new_n != simulator.n:
        st.session_state.simulator = ShorSimulator(n=new_n)
        st.rerun()

    if st.sidebar.button("Recommencer de Zéro"):
        st.session_state.simulator = ShorSimulator()
        st.rerun()

    is_auto_running = st.sidebar.checkbox("Mode automatique", value=simulator.is_auto_running)
    if is_auto_running != simulator.is_auto_running:
        simulator.is_auto_running = is_auto_running
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("_Développé par_ :<br>Jefferson MBOUOPDA<br>&<br>Ruben MOUGOUE", unsafe_allow_html=True)
    st.sidebar.markdown("_Responsable_ : <br> Ahmed LOUNIS <br><br> _Superviseur_ : <br> Vincent ROBIN", unsafe_allow_html=True)
    st.sidebar.image("utc/image.png")

    simulator.run_step(simulator.current_step)

if __name__ == "__main__":
    main()
