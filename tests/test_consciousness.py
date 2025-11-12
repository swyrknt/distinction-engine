"""
Foundational (Research) Test for Emergent Consciousness (v3)

This test suite attacks the "Consciousness" claims of the
"timeless" theory. It uses the "honest" local evolution model.

Emergent Claims Tested:
1.  Does the process spontaneously produce "binding events"
    (highly integrated, coherent structures)?
2.  Do these "conscious" structures (qualia) have a measurably
    different topology than "unconscious" structures?
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
        """
        Create a fresh, clean "universe" (Engine) for each experiment.
        """
        self.engine = DistinctionEngine()

    # --- "MEASURING TOOLS" (HELPERS) ---

    def _build_graph_from_snapshot(self, state: Tuple[Set[Distinction], Set[Tuple[str, str]]]) -> nx.Graph:
        """
        Builds a NetworkX graph object from an immutable snapshot.
        This is our "telescope" - it observes the state.
        """
        # --- FIX: Unpack the tuple ---
        distinctions, relationships = state
        g = nx.Graph()
        
        g.add_nodes_from([d.id for d in distinctions])
        g.add_edges_from(relationships)
        return g

    # --- HONEST "LOCAL" EVOLUTION HELPER ---
    def _evolve_universe(self, steps: int):
        """
        Runs the "one process" locally.
        """
        # --- FIX: We must sample from the *values* of the dictionary ---
        current_distinctions = list(self.engine.all_distinctions.values())
        if len(current_distinctions) < 2:
            return

        # We need a quick way to map id -> object
        distinction_map = {d.id: d for d in current_distinctions}

        for i in range(steps):
            # --- FIX: Use the tuple-based snapshot ---
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

    # --- FOUNDATIONAL TEST 5: THE BINDING PROBLEM ---

    def test_falsify_binding_events(self):
        """
        FALSIFICATION TEST 5: The Binding Problem
        
        Hypothesis: The system will spontaneously produce moments
        of high integration ("binding events").
        """
        print("\n🧠 ATTACKING CONSCIOUSNESS (Binding): Do 'binding events' emerge?")
        
        # 1. Evolve the universe for a long time
        print("   Evolving universe locally for 5000 steps...")
        self._evolve_universe(steps=5000)
        
        # 2. Get the final state and build the graph
        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        
        self.assertGreater(g.number_of_nodes(), 500, "Evolution failed to produce enough distinctions.")

        # 3. The Measurement:
        print("   Measuring emergent coherence for all distinctions...")
        all_coherence_levels = nx.clustering(g)
        
        if not all_coherence_levels:
            self.fail("Could not measure coherence; graph is empty.")
            
        max_coherence = max(all_coherence_levels.values())
        avg_coherence = np.mean(list(all_coherence_levels.values()))

        print(f"\n   --- Binding Test Results ---")
        print(f"   Max Emergent Coherence (Binding): {max_coherence:.4f}")
        print(f"   Avg Emergent Coherence (Noise): {avg_coherence:.6f}")
        
        # 4. The Falsification:
        threshold = 0.5 
        self.assertGreater(max_coherence, threshold,
                         f"🚩 FALSIFIED: No 'binding events' found. Max coherence was {max_coherence:.4f},"
                         f" which does not clear the {threshold} threshold.")
        
        print(f"\n   ✅ THEORY VALIDATED: At least one 'binding event' (coherence > {threshold})")
        print("      was detected. Consciousness (as defined) spontaneously emerged.")

    # --- FOUNDATIONAL TEST 6: QUALIA STRUCTURE ---
    
    def _get_subgraph_properties(self, g: nx.Graph, node_id: str) -> Dict:
        """
        THE "QUALIA RULER": Measures the structural properties
        of a distinction's local neighborhood (its "experience").
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
        FALSIFICATION TEST 6: The Qualia Test
        
        Hypothesis: "Conscious" (high-coherence) states are
        structurally *different* from "unconscious" (low-coherence) states.
        """
        print("\n🎨 ATTACKING QUALIA: Do 'conscious' states have a unique structure?")
        
        # 1. Evolve the universe
        print("   Evolving universe locally for 5000 steps...")
        self._evolve_universe(steps=5000)
        
        # 2. Get state and measure coherence for all nodes
        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        all_coherence_levels = nx.clustering(g)
        
        if len(all_coherence_levels) < 100:
            self.fail("Graph too small to test.")
            
        # 3. Find our "conscious" and "unconscious" samples
        conscious_node_id = max(all_coherence_levels, key=all_coherence_levels.get)
        unconscious_node_id = min(all_coherence_levels, key=all_coherence_levels.get)
        
        conscious_coherence = all_coherence_levels[conscious_node_id]
        unconscious_coherence = all_coherence_levels[unconscious_node_id]

        print(f"   ...Found 'Conscious' node (Coherence: {conscious_coherence:.4f})")
        print(f"   ...Found 'Unconscious' node (Coherence: {unconscious_coherence:.4f})")
        
        if conscious_coherence - unconscious_coherence < 0.1:
            self.fail("Could not find sufficiently different 'conscious' and 'unconscious' nodes to compare.")

        # 4. The Measurement:
        conscious_structure = self._get_subgraph_properties(g, conscious_node_id)
        unconscious_structure = self._get_subgraph_properties(g, unconscious_node_id)

        print(f"\n   --- Qualia Test Results ---")
        print(f"   'Conscious' Structure: {conscious_structure}")
        print(f"   'Unconscious' Structure: {unconscious_structure}")

        # 5. The Falsification:
        #    HONEST TEST: We assert that the "conscious" structure is measurably
        #    more *integrated* (higher density) than the "unconscious" one.
        
        self.assertGreater(conscious_structure["density"], unconscious_structure["density"],
                         "🚩 FALSIFIED: 'Conscious' states are not structurally more integrated (denser) than 'unconscious' states.")
        
        print(f"\n   ✅ THEORY VALIDATED: 'Conscious' states (qualia) are")
        print("      measurably more *integrated* than 'unconscious' states.")

if __name__ == '__main__':
    unittest.main()