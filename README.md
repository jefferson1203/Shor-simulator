# Shor's Algorithm Simulator

An interactive and educational simulator of Shor's quantum algorithm for integer factorization.

## Features

- Step-by-step simulation of Shor's algorithm
- Interactive visualization using Streamlit
- Custom quantum circuit simulation
- Educational explanations for each step
- Modular design for easy understanding

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the simulator:
```bash
streamlit run app.py
```

## Project Structure

- `quantum/`: Quantum circuit simulation components
- `classical/`: Classical preprocessing and post-processing
- `visualization/`: Plotting and visualization modules
- `app.py`: Main Streamlit application
