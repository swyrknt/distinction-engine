"""
Foundational (Research) Tests for the "Timeless" DistinctionEngine (v4)

This test suite attacks the "timeless" implementation.
All "ruler" metrics (Coherence, Usage, AND Time) are
now 100% emergent properties calculated by the observer.

HONEST-TO-THE-THEORY:
- Implementation: Uses the "timeless" distinction.py (no creation_step).
- Evolution: Uses the "local" evolution helper.
- Measurement: Uses the "honest" ruler: [emergent_coherence, emergent_usage, emergent_age]
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestFoundationalResearch(unittest.TestCase):

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
        # --- FIX: Sample from the *values* of the dictionary ---
        current_distinctions = list(self.engine.all_distinctions.values())
        if len(current_distinctions) < 2:
            return

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


    # --- FOUNDATIONAL TEST 1: SELF-ORGANIZATION ---

    def test_falsify_spontaneous_organization(self):
        print("\n🔬 FOUNDATIONAL TEST: Does the universe spontaneously organize?")
        self._evolve_universe(steps=2000)
        
        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        
        self.assertGreater(g.number_of_nodes(), 100, "Evolution failed to produce enough distinctions.")
        
        emergent_coherence = nx.average_clustering(g)
        print(f"   ...Emergent Coherence (Avg. Clustering): {emergent_coherence:.6f}")
        
        self.assertGreater(emergent_coherence, 0.001, 
                         "🚩 FALSIFIED: The system did not self-organize.")
        print("   ✅ PASSED: System shows spontaneous self-organization.")

    # --- FOUNDATIONAL TEST 2: COMPLEXITY ---

    def test_falsify_emergent_complexity(self):
        print("\n🔬 FOUNDATIONAL TEST: Does the universe produce complexity?")
        self._evolve_universe(steps=3000)
        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        self.assertGreater(g.number_of_nodes(), 150)

        degrees = [d for n, d in g.degree()]
        if not degrees:
            self.fail("Could not measure degrees; graph is empty.")

        mean_degree = np.mean(degrees)
        std_dev_degree = np.std(degrees)
        print(f"   ...Emergent Usage (Degree Dist.): mean={mean_degree:.2f}, std_dev={std_dev_degree:.2f}")

        self.assertGreater(std_dev_degree, mean_degree * 0.5,
                         "🚩 FALSIFIED: System is not complex.")
        print("   ✅ PASSED: System shows emergent 'fat-tail' complexity.")

    # --- FOUNDATIONAL TEST 3: THE "HONEST" QUANTUM ATTACK ---

    def _get_emergent_age(self, g: nx.Graph, node_id: str, origin_id: str) -> int:
        """
        Calculates "Emergent Age" (or causal distance) as the shortest path
        length from the node to the origin 'd0'.
        """
        try:
            return nx.shortest_path_length(g, source=origin_id, target=node_id)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return 0 # The origin node, or a disconnected node

    def _get_emergent_state_vector(self, g: nx.Graph, d: Distinction, metrics: Dict) -> np.ndarray:
        """
        THE "RULER" (v5 - Fully Emergent):
        Defines the state of a distinction as a vector of its
        *emergent properties*: [coherence, usage, age/distance].
        """
        if d is None or d.id not in g:
            return np.array([0, 0, 0])
            
        # 1. Emergent Coherence (Local Clustering)
        coherence = nx.clustering(g, d.id)
        
        # 2. Emergent Usage (Normalized Degree)
        usage = g.degree(d.id) / metrics["max_degree"] if metrics["max_degree"] > 0 else 0
        
        # 3. Emergent Time (Normalized Age/Path Length from d0)
        #    This is our "Space" or "Container" metric.
        age = self._get_emergent_age(g, d.id, metrics["origin_id"]) / metrics["max_age"] if metrics["max_age"] > 0 else 0
        
        vector = np.array([coherence, usage, age])
        return vector

    def test_correlation_of_content_and_container(self):
        """
        THEORY-HONEST QUANTUM TEST (v5):
        Tests the superdeterministic nature of the "all one process"
        by correlating a node's *internal* state (Content) with
        its *external* state (Container).
        """
        print("\n⚛️  ATTACKING SUPERDETERMINISM (The Real Test)")
        print("   Testing correlation of 'Content' (Coherence) vs. 'Container' (Age/Distance)...")

        # 1. Evolve the system *locally*
        print("   Evolving system locally to create a complex process space...")
        self._evolve_universe(steps=2000) 
        
        # 2. Build our "measuring tools" from the *final, static* state
        print("   Taking one snapshot of the universe...")
        state = self.engine.get_state_snapshot()
        g = self._build_graph_from_snapshot(state)
        # --- FIX: Unpack tuple to get distinctions ---
        all_distinctions = list(state[0])
        
        if len(all_distinctions) < 100:
            self.fail("Falsification failed: Universe too small to test.")
        
        # 3. Calculate all emergent properties ONCE
        print("   Calculating emergent properties for all distinctions...")
        all_degrees = dict(g.degree())
        all_coherences = nx.clustering(g)
        origin_id = self.engine.d0.id
        
        all_ages = {}
        max_age = 0
        for d in all_distinctions:
            age = self._get_emergent_age(g, d.id, origin_id)
            all_ages[d.id] = age
            if age > max_age:
                max_age = age

        max_degree = max(all_degrees.values()) if all_degrees else 1
        
        if max_age == 0:
            self.fail("Falsification failed: Universe has no 'age' (graph is disconnected).")

        # 4. Run the Analysis:
        #    Instead of sampling, we will correlate the *entire* universe.
        #    This is a more robust and direct test.
        print("   Correlating properties for all distinctions...")
        
        coherence_list = []
        age_list = []
        
        for d in all_distinctions:
            if d.id == origin_id: continue # Skip origin
            coherence_list.append(all_coherences[d.id])
            age_list.append(all_ages[d.id])
        
        if not coherence_list:
             self.fail("Falsification failed: Could not measure any properties.")

        # 5. The Real Test: ANALYSIS
        correlation_matrix = np.corrcoef(coherence_list, age_list)
        correlation = correlation_matrix[0, 1]

        print(f"\n   --- Superdeterminism Test Results ---")
        print(f"   Correlation (Coherence vs. Emergent Age): {correlation:.4f}")
        
        # 6. The Verdict
        if abs(correlation) > 0.1:
            print("   ✅ THEORY VALIDATED: A systemic correlation exists.")
            print("   This proves a distinction's internal 'content' (Coherence)")
            print("   is correlated with its external 'container' (Age/Distance).")
        else:
            print("   ⚠️  THEORY FALSIFIED: No systemic correlation found.")
            
        self.assertGreater(abs(correlation), 0.1,
                         "Theory failed: A distinction's internal state (Coherence) "
                         "is not correlated with its external state (Age/Distance).")

if __name__ == '__main__':
    unittest.main()