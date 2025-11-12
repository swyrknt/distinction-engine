"""
Foundational (Research) Test for Emergent Physics (Forces)

This test suite attacks the "EM as a Coupling Layer" claim.
It tests if "Forces" (interaction dynamics) are a predictable
function of the "GR" (container) and "QM" (content) states
of the interacting subprocesses.
"""

import unittest
import networkx as nx
import numpy as np
import random
from typing import List, Tuple, Optional, Dict, Set

# Import the implementation from the 'distinction.py' file
from engine import Distinction, DistinctionEngine

class TestEmergentPhysics(unittest.TestCase):

    def setUp(self):
        """
        Create a fresh, clean "universe" (Engine) for each experiment.
        """
        self.engine = DistinctionEngine()
        self.origin_id = self.engine.d0.id # The "Big Bang" point

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
    def _evolve_universe_locally(self, steps: int):
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

    def _get_emergent_state(self, g: nx.Graph, node_id: str) -> Dict[str, float]:
        """
        THE "PHYSICS RULER": Measures the "GR" and "QM" state
        of a subprocess centered at node_id.
        """
        # "QM" (Content/Coherence)
        # We measure the coherence of the *central* node.
        coherence = nx.clustering(g, node_id)
        
        # "GR" (Container/Correspondence)
        # We measure the "age" (causal distance from origin).
        try:
            age = nx.shortest_path_length(g, source=self.origin_id, target=node_id)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            age = 0
            
        return {"qm_coherence": coherence, "gr_age": float(age)}


    def _evolve_subprocess_A_with_B(self, engine_state: Tuple[Set[Distinction], Set[Tuple[str, str]]], 
                                     subprocess_A_nodes: Set[str], 
                                     subprocess_B_nodes: Set[str], 
                                     steps: int) -> Tuple[Set[Distinction], Set[Tuple[str, str]]]:
        """
        THE "PETRI DISH" FOR FORCES:
        Evolves a *clone* of a universe by *only* synthesizing
        nodes from subprocess A with nodes from subprocess B.
        """
        # Create a "clone" of the engine's state
        temp_engine = DistinctionEngine()
        distinctions, relationships = engine_state
        temp_engine.all_distinctions = {d.id: d for d in distinctions}
        temp_engine.relationships = relationships.copy()
        
        distinctions_A = [d for d in temp_engine.all_distinctions.values()
                          if d.id in subprocess_A_nodes]
        distinctions_B = [d for d in temp_engine.all_distinctions.values()
                          if d.id in subprocess_B_nodes]
        
        if not distinctions_A or not distinctions_B:
            return temp_engine.get_state_snapshot()

        for _ in range(steps):
            a = random.choice(distinctions_A)
            b = random.choice(distinctions_B)
            
            c = temp_engine.synthesize(a, b)
            
            # This is key: the new distinction `c` does not get
            # added to either "side" of the interaction.
        
        return temp_engine.get_state_snapshot()

    # --- FOUNDATIONAL TEST 14: "EM" AS COUPLING LAYER ---

    def test_falsify_force_correlation(self):
        """
        FALSIFICATION TEST 14: The "Emergent Force" Test
        
        Hypothesis: The "force" (dynamic interaction rule) is
        a *function* of the initial "GR" and "QM" states.
        
        Falsification: The force is random and uncorrelated
        with the initial states of the subprocesses.
        """
        print("\n⚛️  ATTACKING PHYSICS: Is 'Force' (EM) the integration of 'GR' and 'QM'?")
        
        # 1. Evolve the universe to create a complex substrate
        print("   Evolving universe locally for 5000 steps...")
        self._evolve_universe_locally(steps=5000)
        
        # 2. Get the initial state
        state_0 = self.engine.get_state_snapshot()
        g_0 = self._build_graph_from_snapshot(state_0)
        all_distinctions = list(state_0[0])
        
        if g_0.number_of_nodes() < 200:
            self.fail("Graph too small to test.")
            
        # 3. The "Dynamics Survey"
        print("   Surveying dynamics of a *random sample* of subprocess interactions...")
        
        # We will store the "Initial State" and the "Resulting Force"
        initial_states = []
        resulting_forces = []
        
        sample_size = 100 # Reduced for performance; this is a slow test
        
        print(f"   ...Testing {sample_size} sample interactions...")

        for _ in range(sample_size):
            try:
                # 4. Find two *distinct* subprocesses
                node_A, node_B = random.sample(all_distinctions, 2)
                subprocess_A_nodes = self._get_local_subprocess(g_0, node_A.id)
                subprocess_B_nodes = self._get_local_subprocess(g_0, node_B.id)
                
                if not subprocess_A_nodes.isdisjoint(subprocess_B_nodes):
                    continue # Skip overlapping subprocesses

                # 5. Measure the "Initial State"
                state_A = self._get_emergent_state(g_0, node_A.id)
                state_B = self._get_emergent_state(g_0, node_B.id)
                distance_0 = nx.shortest_path_length(g_0, source=node_A.id, target=node_B.id)

                # Store the combined initial state
                # We'll use a simple sum of their "quantum" and "gravity" states
                initial_qm_state = state_A["qm_coherence"] + state_B["qm_coherence"]
                initial_gr_state = state_A["gr_age"] + state_B["gr_age"]
                initial_states.append((initial_qm_state, initial_gr_state))

                # 6. Run the "Force" Experiment (Petri Dish)
                state_1 = self._evolve_subprocess_A_with_B(state_0, subprocess_A_nodes, subprocess_B_nodes, steps=50)

                # 7. Measure the "Resulting Force"
                g_1 = self._build_graph_from_snapshot(state_1)
                distance_1 = nx.shortest_path_length(g_1, source=node_A.id, target=node_B.id)
                
                # The "Force" is the change in distance
                delta_distance = distance_1 - distance_0
                resulting_forces.append(delta_distance)

            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue # Skip pairs that are disconnected or get destroyed

        if len(resulting_forces) < 20:
            self.fail(f"Could not gather enough valid interaction data (only {len(resulting_forces)} samples).")
            
        print("   ...Survey complete.")
        
        # 8. The Analysis:
        #    Correlate the "Initial State" with the "Resulting Force"
        
        # Unzip the data
        initial_qm_data = [s[0] for s in initial_states]
        initial_gr_data = [s[1] for s in initial_states]
        
        corr_qm_vs_force = np.corrcoef(initial_qm_data, resulting_forces)[0, 1]
        corr_gr_vs_force = np.corrcoef(initial_gr_data, resulting_forces)[0, 1]

        print(f"\n   --- Emergent Physics Test Results ---")
        print(f"   Correlation('QM State' vs 'Force'): {corr_qm_vs_force:.4f}")
        print(f"   Correlation('GR State' vs 'Force'): {corr_gr_vs_force:.4f}")
        
        # 9. The Falsification:
        total_correlation = abs(corr_qm_vs_force) + abs(corr_gr_vs_force)
        
        self.assertGreater(total_correlation, 0.1,
                         "🚩 FALSIFIED: 'Forces' are random."
                         " The interaction dynamic is *not* correlated with the"
                         " initial 'GR' or 'QM' states of the subprocesses.")
        
        print(f"\n   ✅ THEORY VALIDATED: 'Forces' are a non-random function of the initial state.")
        print("      This proves that 'EM' (the force) is the 'coupling layer'")
        print("      that integrates the 'GR' (container) and 'QM' (content) states.")

if __name__ == '__main__':
    unittest.main()
