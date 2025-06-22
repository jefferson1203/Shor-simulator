import streamlit as st
import plotly.graph_objects as go
import numpy as np

class CircuitVisualizer:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.fig = go.Figure()
        self._setup_qubit_lines()

    def _setup_qubit_lines(self):
        for i in range(self.num_qubits):
            self.fig.add_trace(go.Scatter(
                x=[0, 10], y=[i, i], mode='lines',
                line=dict(color='black', width=1), showlegend=False
            ))
            self.fig.add_annotation(
                x=-0.5, y=i, text=f'Q{i}', showarrow=False
            )
        self.fig.update_layout(
            title='Circuit Quantique', xaxis_title='Étapes', yaxis_title='Qubits',
            showlegend=False, xaxis=dict(range=[0, 8]), yaxis=dict(range=[-1, self.num_qubits]),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=50, b=50)
        )

    def add_gate(self, gate_type, qubit_indices, step):
        if not qubit_indices:
            return

        # Pour les portes à un seul qubit (comme H), dessinez une boîte sur chaque ligne de qubit.
        if gate_type in ['H']:
            for qubit_idx in qubit_indices:
                self.fig.add_annotation(
                    x=step, y=qubit_idx, text=gate_type, showarrow=False,
                    font=dict(size=15), bgcolor='lightblue', bordercolor='black',
                    borderwidth=1, borderpad=4, opacity=0.9
                )
            return

        # Pour les portes multi-qubits (O, IQFT, M), dessinez une seule grande boîte.
        min_q, max_q = min(qubit_indices), max(qubit_indices)
        
        # Dessiner une seule boîte couvrant les qubits
        self.fig.add_shape(
            type="rect",
            x0=step - 0.5, y0=min_q - 0.5,
            x1=step + 0.5, y1=max_q + 0.5,
            line=dict(color="black", width=1),
            fillcolor="lightblue",
            layer="below"
        )
        
        # Ajouter l'étiquette de la porte au centre de la boîte
        self.fig.add_annotation(
            x=step, y=(min_q + max_q) / 2,
            text=gate_type,
            showarrow=False,
            font=dict(size=15, color="black"),
        )

    def plot_probabilities(self, state_vector):
        if state_vector is None: return None
        probabilities = np.abs(state_vector)**2
        significant_indices = np.where(probabilities > 1e-9)[0]
        if len(significant_indices) == 0: return None
        
        states_to_plot = significant_indices
        probs_to_plot = probabilities[significant_indices]

        fig = go.Figure(data=[go.Bar(x=states_to_plot, y=probs_to_plot)])
        fig.update_layout(
            title="Probabilités des états de mesure finaux",
            xaxis_title="État (valeur décimale)", yaxis_title="Probabilité",
            xaxis=dict(type='category')
        )
        return fig

    def show_circuit(self):
        return self.fig

    def reset(self):
        self.fig.data = []
        self.fig.layout.annotations = []
        self._setup_qubit_lines()
