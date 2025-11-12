"""
Emergent Dynamics Test Suite

Tests whether high-coherence subprocesses exhibit greater evolutionary
instability than low-coherence subprocesses, indicating feedback
between structural properties and subsequent evolution.

Falsification Target:
Passive labeling - high-coherence designation has no causal influence
on subsequent structural evolution, proving consciousness lacks
dynamical consequences.
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestEmergentDynamics(unittest.TestCase):

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

    def _get_local_subprocess(self, g: nx.Graph, start_node_id: str, radius=2) -> Set[str]:
        """Return node IDs within specified radius of start node."""
        return set(nx.ego_graph(g, start_node_id, radius=radius).nodes())

    def _measure_subprocess_coherence(self, g: nx.Graph, subprocess_nodes: Set[str], all_coherence_levels: Dict[str, float]) -> float:
        """
        Calculate average clustering coefficient for a set of nodes.

        Returns mean coherence value across subprocess, or 0.0 if empty.
        """
        if not subprocess_nodes:
            return 0.0

        subprocess_coherence = [all_coherence_levels.get(node_id, 0)
                                for node_id in subprocess_nodes]

        if not subprocess_coherence:
            return 0.0

        return np.mean(subprocess_coherence)

    def _evolve_local_subprocess(self, subprocess_nodes: Set[str], steps: int):
        """
        Execute synthesis operations confined to a subprocess.

        Randomly selects pairs from within the subprocess node set,
        allowing measurement of localized evolutionary dynamics.
        """
        local_distinctions = [d for d in self.engine.all_distinctions.values()
                              if d.id in subprocess_nodes]
        
        if len(local_distinctions) < 2:
            return

        distinction_map = {d.id: d for d in local_distinctions}

        for _ in range(steps):
            if len(local_distinctions) < 2:
                break
            a, b = random.sample(local_distinctions, 2)
            c = self.engine.synthesize(a, b)
            
            if c.id not in distinction_map:
                local_distinctions.append(c)
                distinction_map[c.id] = c

    def test_falsify_conscious_influence(self):
        """
        Falsification Test: Passive Labeling

        Hypothesis: High-coherence subprocesses exhibit greater coherence
        change magnitude during local evolution than low-coherence subprocesses,
        demonstrating feedback between structure and dynamics.

        Falsifies if: High-coherence and low-coherence subprocesses show
        equivalent coherence change, proving coherence has no dynamical effect.

        Measurement:
        - Change in average clustering coefficient for subprocess neighborhoods
        """
        print("\nTest: Conscious Influence Falsification")

        print("   Executing 5000 synthesis operations...")
        self._evolve_universe(steps=5000)

        state_0 = self.engine.get_state_snapshot()
        g_0 = self._build_graph_from_snapshot(state_0)

        all_node_coherence = nx.clustering(g_0)

        if len(all_node_coherence) < 100:
            self.fail("Graph too small to test.")

        print("   Identifying high and low coherence subprocesses...")

        subprocess_avg_coherence = {}

        for node_id in g_0.nodes():
            subprocess_nodes = self._get_local_subprocess(g_0, node_id)
            avg_coherence = self._measure_subprocess_coherence(g_0, subprocess_nodes, all_node_coherence)
            subprocess_avg_coherence[node_id] = avg_coherence

        if not subprocess_avg_coherence:
            self.fail("Could not measure any subprocesses.")

        conscious_center_id = max(subprocess_avg_coherence, key=subprocess_avg_coherence.get)
        conscious_subprocess = self._get_local_subprocess(g_0, conscious_center_id)
        avg_conscious_coherence_0 = subprocess_avg_coherence[conscious_center_id]

        unconscious_center_id = min(subprocess_avg_coherence, key=subprocess_avg_coherence.get)
        unconscious_subprocess = self._get_local_subprocess(g_0, unconscious_center_id)
        avg_unconscious_coherence_0 = subprocess_avg_coherence[unconscious_center_id]

        print(f"   High-coherence subprocess: {avg_conscious_coherence_0:.4f}")
        print(f"   Low-coherence subprocess: {avg_unconscious_coherence_0:.4f}")
        
        if avg_conscious_coherence_0 - avg_unconscious_coherence_0 < 0.01:
            self.fail("Could not find sufficiently different subprocesses to compare.")

        print("   Evolving high-coherence subprocess internally (100 steps)...")
        self._evolve_local_subprocess(conscious_subprocess, steps=100)

        print("   Evolving low-coherence subprocess internally (100 steps)...")
        self._evolve_local_subprocess(unconscious_subprocess, steps=100)

        state_1 = self.engine.get_state_snapshot()
        g_1 = self._build_graph_from_snapshot(state_1)
        all_node_coherence_1 = nx.clustering(g_1)

        final_conscious_subprocess = self._get_local_subprocess(g_1, conscious_center_id)
        final_unconscious_subprocess = self._get_local_subprocess(g_1, unconscious_center_id)

        avg_conscious_coherence_1 = self._measure_subprocess_coherence(g_1, final_conscious_subprocess, all_node_coherence_1)
        avg_unconscious_coherence_1 = self._measure_subprocess_coherence(g_1, final_unconscious_subprocess, all_node_coherence_1)

        delta_conscious = avg_conscious_coherence_1 - avg_conscious_coherence_0
        delta_unconscious = avg_unconscious_coherence_1 - avg_unconscious_coherence_0

        print(f"\n   Results:")
        print(f"   High-coherence change: {delta_conscious:+.4f}")
        print(f"   Low-coherence change: {delta_unconscious:+.4f}")

        self.assertGreater(abs(delta_conscious), abs(delta_unconscious),
                         "FALSIFIED: High-coherence subprocesses are not more dynamically unstable than low-coherence subprocesses.")

        print(f"\n   Hypothesis sustained.")
        print(f"   High-coherence subprocesses exhibit greater evolutionary instability.")

if __name__ == '__main__':
    unittest.main()