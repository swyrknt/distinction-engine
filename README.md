# The Distinction Engine

**A Computational Ontology for Emergent Topology and Physics**

The Distinction Engine is a minimal graph processing system designed to investigate emergent phenomena. It models a universe generated from a single axiom—Distinction—where properties such as geometry, time, and physical forces arise as emergent features of graph topology rather than hard-coded variables.

This repository contains the **Open Core** of the project: the fundamental engine, the research test suite, and visualization tools.

## 📂 Repository Structure

* **`engine/`**: Contains the core logic (`distinction.py`). This is a strict implementation of the "One Process" axiom (local, deterministic synthesis).
* **`tests/`**: A suite of research-grade unit tests designed to falsify claims regarding emergent geometry, causal time, and topological forces.
* **`visuals/`**: Tools for rendering the graph state into 3D interactive models.

## ⚡ Quick Start

### 1. Automatic Setup
We provide a script to automatically create a virtual environment and install dependencies.

**Mac/Linux:**
```bash
python3 setup_env.py
source venv/bin/activate
````

**Windows:**

```bash
python setup_env.py
.\venv\Scripts\activate
```

### 2\. Manual Setup

If you prefer to configure it manually:

```bash
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 🔬 Running Tests

The research claims are validated via `pytest`.

**Run all tests:**

```bash
python -m pytest tests/
```

**Run all tests (verbose mode):**

```bash
python -m pytest tests/ -v
```

**Run all tests, stopping at the first failure:**

```bash
python -m pytest tests/ -x
```

**Run a specific research domain:**

```bash
# Test for emergent 3D geometry
python -m pytest tests/test_geometry.py

# Test for the Arrow of Time
python -m pytest tests/test_time.py

# Test for emergent forces/physics
python -m pytest tests/test_physics.py
```

## 🌌 Visualization

To observe the emergent structure of the graph in 3D:

```bash
python -m visuals.visualization
```

This will generate a force-directed graph layout based on the engine's state and open it in your default web browser.

## 📐 Theoretical Framework

This engine operates on **Distinction Process Theory**. It posits that physical laws are emergent properties of a self-organizing network.

1.  **Identity:** defined strictly by relationship to the Origin (`d0`).
2.  **Time:** defined as the causal radius (shortest path) from the Origin.
3.  **Space:** defined as the absence of direct relationship (topological distance).
4.  **Forces:** defined as the deterministic integration of sub-graphs, where interaction probability is a function of topological density ("Gravity") and structural compatibility.

## 📜 License

This project is released under the **MIT License**.
