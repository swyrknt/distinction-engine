"""
Emergent Consciousness Test Suite

Tests whether the synthesis process generates highly integrated
structures (binding events) and whether high-coherence states exhibit
measurably distinct topological properties from low-coherence states.

Falsification Targets:
1. Absence of binding - the system fails to produce high-integration structures
2. Structural uniformity - high-coherence states are topologically indistinguishable
   from low-coherence states
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestEmergentConsciousness(unittest.TestCase):

    def setUp(self):
        """Initialize a fresh engine instance for each test."""
        self.engine = DistinctionEngine()

    def _build_graph_from_snapshot(self, state: Tuple[Set[Distinction], Set[Tuple[str, str]]]) -> nx.Graph:
        """Convert engine state snapshot to NetworkX graph for analysis."""
        distinctions, relationships = state
        g = nx.Graph()
        
        g.add_nodes_from([d.id for d in distinctions])
        g.add_edges_from(relationships)
        return g

    def _evolve_universe(self, steps: int):
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

    def test_falsify_binding_events(self):
        """
        Falsification Test: Absence of Binding

        Hypothesis: The synthesis process generates structures with high
        clustering coefficients (binding events), indicating local integration.

        Falsifies if: Maximum clustering coefficient fails to exceed threshold,
        proving the system cannot produce integrated structures.

        Measurement:
        - Clustering coefficient for all nodes (measures local triangle density)
        """
        print("\nTest: Binding Events Falsification")

        print("   Executing 5000 synthesis operations...")
        self._evolve_universe(steps=5000)

        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)

        self.assertGreater(g.number_of_nodes(), 500, "Evolution failed to produce enough distinctions.")

        print("   Measuring clustering coefficients...")
        all_coherence_levels = nx.clustering(g)

        if not all_coherence_levels:
            self.fail("Could not measure coherence; graph is empty.")

        max_coherence = max(all_coherence_levels.values())
        avg_coherence = np.mean(list(all_coherence_levels.values()))

        print(f"\n   Results:")
        print(f"   Maximum clustering coefficient: {max_coherence:.4f}")
        print(f"   Average clustering coefficient: {avg_coherence:.6f}")

        threshold = 0.5
        self.assertGreater(max_coherence, threshold,
                         f"FALSIFIED: Maximum coherence {max_coherence:.4f} does not exceed threshold {threshold}.")

        print(f"\n   Hypothesis sustained.")
        print(f"   High-integration structures detected (coherence > {threshold}).")

    def _get_subgraph_properties(self, g: nx.Graph, node_id: str) -> Dict:
        """
        Measure structural properties of a node's local neighborhood.

        Returns node count, edge count, and density of 1-hop ego graph.
        """
        subgraph = nx.ego_graph(g, node_id, radius=1)
        
        if subgraph.number_of_nodes() <= 1:
            return {"nodes": 1, "edges": 0, "density": 0}
            
        return {
            "nodes": subgraph.number_of_nodes(),
            "edges": subgraph.number_of_edges(),
            "density": nx.density(subgraph)
        }

    def test_falsify_qualia_structure(self):
        """
        Falsification Test: Structural Uniformity

        Hypothesis: High-coherence nodes exhibit higher local neighborhood
        density than low-coherence nodes, indicating distinct topological
        properties correlate with coherence levels.

        Falsifies if: High-coherence and low-coherence nodes show no
        significant difference in local neighborhood density.

        Measurement:
        - Ego graph density (1-hop) for max and min coherence nodes
        """
        print("\nTest: Qualia Structure Falsification")

        print("   Executing 5000 synthesis operations...")
        self._evolve_universe(steps=5000)

        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        all_coherence_levels = nx.clustering(g)

        if len(all_coherence_levels) < 100:
            self.fail("Graph too small to test.")

        conscious_node_id = max(all_coherence_levels, key=all_coherence_levels.get)
        unconscious_node_id = min(all_coherence_levels, key=all_coherence_levels.get)

        conscious_coherence = all_coherence_levels[conscious_node_id]
        unconscious_coherence = all_coherence_levels[unconscious_node_id]

        print(f"   High-coherence node: {conscious_coherence:.4f}")
        print(f"   Low-coherence node: {unconscious_coherence:.4f}")

        if conscious_coherence - unconscious_coherence < 0.1:
            self.fail("Could not find sufficiently different high and low coherence nodes to compare.")

        conscious_structure = self._get_subgraph_properties(g, conscious_node_id)
        unconscious_structure = self._get_subgraph_properties(g, unconscious_node_id)

        print(f"\n   Results:")
        print(f"   High-coherence neighborhood: {conscious_structure}")
        print(f"   Low-coherence neighborhood: {unconscious_structure}")

        self.assertGreater(conscious_structure["density"], unconscious_structure["density"],
                         "FALSIFIED: High-coherence nodes are not structurally more integrated than low-coherence nodes.")

        print(f"\n   Hypothesis sustained.")
        print(f"   High-coherence states exhibit greater local integration.")

if __name__ == '__main__':
    unittest.main()