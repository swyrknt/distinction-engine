"""
Foundational (Research) Test for Information Theory

This test suite attacks the "all one process" claim from
the lens of information theory.

Emergent Claim Tested:
1.  Are all subprocesses in the universe systemically
    correlated? (i.e., is their mutual information non-zero?)
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestInformationDynamics(unittest.TestCase):

    def setUp(self):
        """
        Create a fresh, clean "universe" (Engine) for each experiment.
        """
        self.engine = DistinctionEngine()

    # --- "MEASURING TOOLS" (HELPERS) ---

    def _build_graph_from_snapshot(self, state: Tuple[Set[Distinction], Set[Tuple[str, str]]]) -> nx.Graph:
        """
        Builds a NetworkX graph object from an immutable snapshot.
        """
        distinctions, relationships = state
        g = nx.Graph()
        g.add_nodes_from([d.id for d in distinctions])
        g.add_edges_from(relationships)
        return g

    # --- HONEST "LOCAL" EVOLUTION HELPER ---
    def _evolve_universe_locally(self, steps: int) -> List[Distinction]:
        """
        Runs the "one process" locally and returns the
        *final* list of all distinctions.
        """
        current_distinctions = list(self.engine.all_distinctions.values())
        if len(current_distinctions) < 2:
            return current_distinctions

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
                
        # Return the final, complete list of distinctions
        return list(self.engine.all_distinctions.values())
    # --- END HONEST EVOLUTION HELPER ---

    def _get_local_subprocess(self, g: nx.Graph, start_node_id: str, radius=2) -> Set[str]:
        """
        Gets the set of node IDs in a local neighborhood (our "subprocess").
        """
        return set(nx.ego_graph(g, start_node_id, radius=radius).nodes())

    def _measure_subprocess_coherence(self, g: nx.Graph, subprocess_nodes: Set[str]) -> float:
        """
        Measures the *average* emergent coherence (clustering)
        of a specific set of nodes (the subprocess).
        """
        if not subprocess_nodes:
            return 0.0
            
        # We need the coherence of *all* nodes to do this measurement
        all_coherence_levels = nx.clustering(g)
        
        subprocess_coherence = [all_coherence_levels.get(node_id, 0) 
                                for node_id in subprocess_nodes]
                                
        if not subprocess_coherence:
            return 0.0
            
        return np.mean(subprocess_coherence)

    # --- FOUNDATIONAL TEST 11: MUTUAL INFORMATION ---

    def test_falsify_information_independence(self):
        """
        FALSIFICATION TEST 11: The "Information" Test
        
        Hypothesis: As the "one process" evolves, all "subprocesses"
        (regions of the graph) are systemically correlated.
        
        Falsification: Two subprocesses can evolve independently,
        showing zero correlation (zero mutual information).
        """
        print("\nℹ️  ATTACKING INFORMATION THEORY: Are all subprocesses correlated?")
        
        # 1. Evolve the universe to create a complex substrate
        print("   Evolving universe locally for 3000 steps to create substrate...")
        all_distinctions = self._evolve_universe_locally(steps=3000)
        
        # 2. Get the initial state and find two *distinct* subprocesses
        state_0 = self.engine.get_state_snapshot()
        g_0 = self._build_graph_from_snapshot(state_0)
        
        if len(all_distinctions) < 100:
            self.fail("Graph too small to test.")
            
        # Find two random, non-overlapping subprocesses
        sample_nodes = random.sample(all_distinctions, 2)
        subprocess_A_nodes = self._get_local_subprocess(g_0, sample_nodes[0].id)
        subprocess_B_nodes = self._get_local_subprocess(g_0, sample_nodes[1].id)
        
        # Ensure they are non-overlapping
        while not subprocess_A_nodes.isdisjoint(subprocess_B_nodes):
            sample_nodes = random.sample(all_distinctions, 2)
            subprocess_A_nodes = self._get_local_subprocess(g_0, sample_nodes[0].id)
            subprocess_B_nodes = self._get_local_subprocess(g_0, sample_nodes[1].id)

        print(f"   ...Found two distinct subprocesses (A: {len(subprocess_A_nodes)} nodes, B: {len(subprocess_B_nodes)} nodes).")

        # 3. The "Dynamics" Experiment
        #    We will now evolve the *entire* universe and record
        #    the coherence "state" of A and B over time.
        
        time_series_A = []
        time_series_B = []
        
        observation_steps = 1000
        
        print(f"   ...Observing system dynamics for {observation_steps} steps...")
        
        for _ in range(observation_steps):
            # Evolve the *entire* universe by one "local" step
            self._evolve_universe_locally(steps=1)
            
            # Get a new snapshot and measure the state of A and B
            state_t = self.engine.get_state_snapshot()
            g_t = self._build_graph_from_snapshot(state_t)
            
            # We must update our subprocess node lists, as they may have grown
            # by integrating with neighbors
            current_A_nodes = self._get_local_subprocess(g_t, sample_nodes[0].id)
            current_B_nodes = self._get_local_subprocess(g_t, sample_nodes[1].id)
            
            # Measure their "state" (average coherence)
            state_A = self._measure_subprocess_coherence(g_t, current_A_nodes)
            state_B = self._measure_subprocess_coherence(g_t, current_B_nodes)
            
            time_series_A.append(state_A)
            time_series_B.append(state_B)

        # 4. The Analysis:
        #    We will calculate the Pearson Correlation as a proxy
        #    for Mutual Information.
        
        correlation_matrix = np.corrcoef(time_series_A, time_series_B)
        correlation = correlation_matrix[0, 1]
        
        print(f"\n   --- Information Theory Test Results ---")
        print(f"   Correlation between subprocess A and B: {correlation:.4f}")
        
        # 5. The Falsification:
        #    If the universe is "all one process," the evolutions
        #    of A and B *must* be correlated (positively or negatively).
        #    If the correlation is ~0, they are independent.
        
        self.assertGreater(abs(correlation), 0.05,
                         f"🚩 FALSIFIED: Subprocesses are statistically independent (correlation={correlation:.4f})."
                         " The 'all one process' claim is false.")
        
        print(f"\n   ✅ THEORY VALIDATED: A systemic correlation exists.")
        print("      Subprocesses are not independent; their dynamics are linked,")
        print("      proving the 'all one process' philosophy.")

if __name__ == '__main__':
    unittest.main()