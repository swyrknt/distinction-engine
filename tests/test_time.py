"""
Time Dynamics Test Suite

Tests whether the causal radius of the graph (maximum path distance
from origin) increases monotonically and expansively, indicating
irreversible arrow of time rather than stagnant or reversible dynamics.

Falsification Targets:
1. Time reversal - causal radius decreases between epochs
2. Temporal stagnation - causal radius fails to expand over time
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestTimeDynamics(unittest.TestCase):

    def setUp(self):
        """Initialize a fresh engine instance for each test."""
        self.engine = DistinctionEngine()
        self.origin_id = self.engine.d0.id

    def _build_graph_from_snapshot(self, state: Tuple[Set[Distinction], Set[Tuple[str, str]]]) -> nx.Graph:
        """Convert engine state snapshot to NetworkX graph for analysis."""
        distinctions, relationships = state
        g = nx.Graph()
        g.add_nodes_from([d.id for d in distinctions])
        g.add_edges_from(relationships)
        return g

    def _evolve_universe_locally(self, steps: int):
        """
        Execute synthesis operations with local selection bias.

        Randomly selects pairs of distinctions for synthesis, with preference
        for topologically proximate pairs (within 2-hop neighborhoods).
        Builds the computational substrate through iterated local operations.
        """
        current_distinctions = list(self.engine.all_distinctions.values())
        if len(current_distinctions) < 2:
            return

        distinction_map = {d.id: d for d in current_distinctions}

        for i in range(steps):
            state = self.engine.get_state_snapshot()
            g = self._build_graph_from_snapshot(state)
            
            if len(current_distinctions) < 2:
                break
                
            a = random.choice(current_distinctions)
            b = None

            try:
                neighborhood_ids = set(g.neighbors(a.id))
                for neighbor_id in list(neighborhood_ids):
                    neighborhood_ids.update(g.neighbors(neighbor_id))
                neighborhood_ids.discard(a.id)

                if neighborhood_ids:
                    b_id = random.choice(list(neighborhood_ids))
                    b = distinction_map.get(b_id)
            
            except (nx.NetworkXError, KeyError):
                pass 
            
            if b is None or b.id == a.id:
                others = [d for d in current_distinctions if d.id != a.id]
                if not others:
                    continue
                b = random.choice(others)
            
            c = self.engine.synthesize(a, b)
            
            if c.id not in distinction_map:
                current_distinctions.append(c)
                distinction_map[c.id] = c

    def _get_emergent_age_radius(self, g: nx.Graph) -> int:
        """
        Calculate maximum causal distance from origin.

        Returns maximum shortest path length from primordial node d0 across
        all reachable nodes, representing the causal radius of the graph.
        """
        all_ages = []
        for node_id in g.nodes():
            if node_id == self.origin_id:
                continue
            try:
                age = nx.shortest_path_length(g, source=self.origin_id, target=node_id)
                all_ages.append(age)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue

        return max(all_ages) if all_ages else 0

    def test_falsify_arrow_of_time(self):
        """
        Falsification Test: Arrow of Time

        Hypothesis: Causal radius (maximum path distance from origin) increases
        monotonically and expansively over evolution epochs, indicating
        irreversible time arrow.

        Falsifies if:
        - Causal radius decreases between epochs (time reversal)
        - Causal radius fails to expand significantly (temporal stagnation)

        Measurement:
        - Causal radius tracked across 10 epochs of 500 synthesis operations each
        """
        print("\nTest: Arrow of Time Falsification")

        num_epochs = 10
        steps_per_epoch = 500

        universe_age_history = []

        initial_state = self.engine.get_state_snapshot()
        initial_graph = self._build_graph_from_snapshot(initial_state)
        initial_age = self._get_emergent_age_radius(initial_graph)
        universe_age_history.append(initial_age)

        print(f"   Epoch 0: Causal radius = {initial_age}")

        for i in range(1, num_epochs + 1):
            self._evolve_universe_locally(steps=steps_per_epoch)

            state = self.engine.get_state_snapshot()
            g = self._build_graph_from_snapshot(state)
            current_age = self._get_emergent_age_radius(g)

            print(f"   Epoch {i}: Causal radius = {current_age}")

            self.assertGreaterEqual(current_age, universe_age_history[-1],
                                  f"FALSIFIED: Causal radius decreased from {universe_age_history[-1]} to {current_age}.")

            universe_age_history.append(current_age)

        self.assertGreater(universe_age_history[-1], universe_age_history[0] + (num_epochs / 2),
                         "FALSIFIED: Process is not expansive (temporal stagnation).")

        print(f"\n   Results:")
        print(f"   Age history: {universe_age_history}")
        print(f"\n   Hypothesis sustained.")
        print(f"   Causal radius increases monotonically and expansively (irreversible time arrow).")

if __name__ == '__main__':
    unittest.main()