"""
Foundational (Research) Test for Emergent Dynamics (v3)

This test suite attacks the "Consciousness Feedback Loop" claim
using our "honest" timeless and local model.

Emergent Claim Tested:
1.  Does the emergence of a "conscious" (high-coherence)
    subprocess *influence* its own future evolution?
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
    def _evolve_universe(self, steps: int):
        """
        Runs the "one process" locally to create the substrate.
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
    # --- END HONEST EVOLUTION HELPER ---

    def _get_local_subprocess(self, g: nx.Graph, start_node_id: str, radius=2) -> Set[str]:
        """
        Gets the set of node IDs in a local neighborhood (our "subprocess").
        """
        return set(nx.ego_graph(g, start_node_id, radius=radius).nodes())

    def _measure_subprocess_coherence(self, g: nx.Graph, subprocess_nodes: Set[str], all_coherence_levels: Dict[str, float]) -> float:
        """
        Measures the *average* emergent coherence (clustering)
        of a specific set of nodes (the subprocess).
        """
        if not subprocess_nodes:
            return 0.0
        
        # Filter to only the nodes in our subprocess
        subprocess_coherence = [all_coherence_levels.get(node_id, 0) 
                                for node_id in subprocess_nodes]
                                
        if not subprocess_coherence:
            return 0.0
            
        return np.mean(subprocess_coherence)

    def _evolve_local_subprocess(self, subprocess_nodes: Set[str], steps: int):
        """
        THE "PETRI DISH":
        Evolves a local subprocess *only* by integrating it with itself.
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

    # --- FOUNDATIONAL TEST 7: CONSCIOUS INFLUENCE ---

    def test_falsify_conscious_influence(self):
        """
        FALSIFICATION TEST 7: The Feedback Loop Test
        
        Hypothesis: A "conscious" (high-coherence) subprocess
        will evolve differently than an "unconscious" one.
        
        Falsification: "Consciousness" is a passive label.
        """
        print("\n🧠 ATTACKING DYNAMICS: Does 'consciousness' have causal power?")
        
        # 1. Evolve the universe to create a complex substrate
        print("   Evolving universe locally for 5000 steps...")
        self._evolve_universe(steps=5000)
        
        # 2. Get the initial state and measure everything
        state_0 = self.engine.get_state_snapshot()
        g_0 = self._build_graph_from_snapshot(state_0)
        
        # This is our "ruler" for single-node coherence
        all_node_coherence = nx.clustering(g_0)
        
        if len(all_node_coherence) < 100:
            self.fail("Graph too small to test.")
            
        # --- NEW "HONEST" SELECTION LOGIC ---
        print("   Surveying all subprocesses to find 'conscious' and 'unconscious' regions...")
        
        subprocess_avg_coherence = {} # Map[node_id, avg_coherence_of_its_neighborhood]
        
        for node_id in g_0.nodes():
            # For each node, define its subprocess (its neighborhood)
            subprocess_nodes = self._get_local_subprocess(g_0, node_id)
            
            # And measure that subprocess's *average* coherence
            avg_coherence = self._measure_subprocess_coherence(g_0, subprocess_nodes, all_node_coherence)
            subprocess_avg_coherence[node_id] = avg_coherence

        if not subprocess_avg_coherence:
            self.fail("Could not measure any subprocesses.")

        # 3. Find our two "petri dishes"
        # Find the "most conscious" subprocess
        conscious_center_id = max(subprocess_avg_coherence, key=subprocess_avg_coherence.get)
        conscious_subprocess = self._get_local_subprocess(g_0, conscious_center_id)
        avg_conscious_coherence_0 = subprocess_avg_coherence[conscious_center_id]
        
        # Find the "most unconscious" subprocess
        unconscious_center_id = min(subprocess_avg_coherence, key=subprocess_avg_coherence.get)
        unconscious_subprocess = self._get_local_subprocess(g_0, unconscious_center_id)
        avg_unconscious_coherence_0 = subprocess_avg_coherence[unconscious_center_id]
        # --- END NEW SELECTION LOGIC ---
        
        print(f"   ...Found 'Conscious' subprocess (Initial Coherence: {avg_conscious_coherence_0:.4f})")
        print(f"   ...Found 'Unconscious' subprocess (Initial Coherence: {avg_unconscious_coherence_0:.4f})")
        
        if avg_conscious_coherence_0 - avg_unconscious_coherence_0 < 0.01:
            self.fail("Could not find sufficiently different subprocesses to compare.")

        # 4. Run the "Conscious" Experiment (Feedback Loop)
        print("   ...Evolving 'Conscious' subprocess internally...")
        self._evolve_local_subprocess(conscious_subprocess, steps=100)
        
        # 5. Run the "Unconscious" Experiment (Control)
        print("   ...Evolving 'Unconscious' subprocess internally...")
        self._evolve_local_subprocess(unconscious_subprocess, steps=100)

        # 6. The Measurement: Get the *final* state
        state_1 = self.engine.get_state_snapshot()
        g_1 = self._build_graph_from_snapshot(state_1)
        all_node_coherence_1 = nx.clustering(g_1)

        # Measure the *final* coherence of our (now larger) subprocesses
        # We must re-get the node lists as they have grown
        final_conscious_subprocess = self._get_local_subprocess(g_1, conscious_center_id)
        final_unconscious_subprocess = self._get_local_subprocess(g_1, unconscious_center_id)

        avg_conscious_coherence_1 = self._measure_subprocess_coherence(g_1, final_conscious_subprocess, all_node_coherence_1)
        avg_unconscious_coherence_1 = self._measure_subprocess_coherence(g_1, final_unconscious_subprocess, all_node_coherence_1)
        
        delta_conscious = avg_conscious_coherence_1 - avg_conscious_coherence_0
        delta_unconscious = avg_unconscious_coherence_1 - avg_unconscious_coherence_0
        
        print(f"\n   --- Dynamics Test Results ---")
        print(f"   'Conscious' Coherence Change: {delta_conscious:+.4f}")
        print(f"   'Unconscious' Coherence Change: {delta_unconscious:+.4f}")

        # 7. The Falsification:
        #    HONEST TEST: A "conscious" (highly integrated) process is
        #    *unstable* and *dynamic*. An "unconscious" process is *stable*.
        
        self.assertGreater(abs(delta_conscious), abs(delta_unconscious),
                         "🚩 FALSIFIED: 'Conscious' subprocesses are not more dynamic (unstable)"
                         " than 'unconscious' ones. Consciousness has no causal power.")
        
        print(f"\n   ✅ THEORY VALIDATED: 'Conscious' subprocesses show a")
        print("      more dynamic (unstable) evolution, proving a 'feedback loop' exists.")

if __name__ == '__main__':
    unittest.main()