# The Distinction Engine

**A Computational Ontology for Emergent Topology and Physics**

The Distinction Engine is a minimal graph processing system designed to investigate emergent phenomena. It models a universe generated from a single axiom—Distinction—where properties such as geometry, time, and physical forces arise as emergent features of graph topology rather than hard-coded variables.

This repository contains the fundamental engine, research test suite, and visualization tools.

## Repository Structure

* **`engine/`**: Core axiomatic system implementing deterministic synthesis with five foundational axioms: Identity, Nontriviality, Synthesis, Symmetry, and Irreflexivity.
* **`tests/`**: Research test suite designed to falsify claims regarding emergent geometry, causal time, topological forces, and information dynamics.
* **`visuals/`**: 3D force-directed visualization tools for rendering graph state and emergent properties.

## Quick Start

### Automatic Setup
Use the provided setup script to create a virtual environment and install dependencies:

**Mac/Linux:**
```bash
python3 setup_env.py
source venv/bin/activate
```

**Windows:**
```bash
python setup_env.py
.\venv\Scripts\activate
```

### Manual Setup
```bash
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Running Tests

Research claims are validated using pytest.

**Run all tests:**
```bash
python -m pytest tests/
```

**Run all tests with verbose output:**
```bash
python -m pytest tests/ -v
```

**Run all tests with print statements:**
```bash
python -m pytest tests/ -v -s
```

**Run all tests and stop at first failure:**
```bash
python -m pytest tests/ -x
```

**Run specific test file:**
```bash
python -m pytest tests/test_geometry.py
```

**Run multiple specific tests:**
```bash
python -m pytest tests/test_geometry.py tests/test_time.py -v
```

**Run tests matching a pattern:**
```bash
# Tests with "geometry" in filename
python -m pytest tests/ -k geometry -v

# Tests with "time" or "space" in filename
python -m pytest tests/ -k "time or space" -v
```

**Run tests in parallel (requires pytest-xdist):**
```bash
python -m pytest tests/ -n auto
```

**Available test modules:**
- `test_distinction.py`: Core axiomatic validation
- `test_dynamics.py`: Subprocess dynamics and coherence
- `test_geometry.py`: Emergent dimensionality and fractal properties
- `test_time.py`: Arrow of time and causal radius expansion
- `test_spacetime.py`: Spatial-temporal coherence
- `test_physics.py`: Force-state correlation
- `test_forces.py`: Cross-subprocess interaction dynamics
- `test_information.py`: Information coupling across subprocesses
- `test_research.py`: Self-organization and complexity
- `test_biology.py`: Structural replication dynamics
- `test_chemistry.py`: Atomic emergence
- `test_consciousness.py`: Binding events and integration

## Visualization

Generate 3D force-directed visualization:

```bash
python -m visuals.visualization
```

This executes local synthesis evolution, calculates emergent properties (age, coherence, usage), and renders an interactive HTML visualization using Plotly. The origin node is fixed at (0,0,0), with spatial positions emerging from graph connectivity.

**Visual encoding:**
- Node color: Emergent age (causal distance from origin)
- Node size: Coherence (clustering coefficient)
- Spatial layout: Force-directed positioning based on graph topology

## Theoretical Framework

The engine implements Distinction Process Theory, where physical laws emerge as properties of a self-organizing graph.

**Core concepts:**
- **Identity**: Defined by relationship to origin node (d0)
- **Time**: Causal radius (shortest path distance from origin)
- **Space**: Topological distance (absence of direct relationship)
- **Forces**: Deterministic integration of subgraphs based on structural compatibility

**Five axioms:**
1. Identity: A distinction is defined solely by its unique identifier
2. Nontriviality: System initializes with two distinct entities (0, 1)
3. Synthesis: Two distinctions combine deterministically to create a third
4. Symmetry: Relationships are bidirectional and order-independent
5. Irreflexivity: A distinction synthesized with itself yields itself

## License

MIT License
