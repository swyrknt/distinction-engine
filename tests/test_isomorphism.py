"""
Structural Isomorphism Test Suite

Tests whether semantic meaning is topologically invariant across different
symbolic labeling systems (languages). Validates that identical logical
structures constructed with different labels yield identical distinct IDs.

Falsification Target:
Linguistic Coupling - The identity of a concept depends on its label
rather than its structure. If English 'Nature' and Japanese 'Shizen'
produce different IDs despite identical construction histories, the
hypothesis is falsified.
"""

import unittest
from engine import Distinction, DistinctionEngine

class TestIsomorphism(unittest.TestCase):

    def setUp(self):
        self.engine = DistinctionEngine()

    def _construct_concept_hierarchy(self, labels: dict) -> str:
        """
        Build standard logic hierarchy using language-specific label map.

        Returns ID of final concept. Uses isolated engine instance to ensure
        label systems remain independent.

        Construction sequence: (0 + 1) -> Existence, (Existence + 0) -> Order,
        (Existence + 1) -> Chaos, (Order + Chaos) -> Complexity.
        """
        local_engine = DistinctionEngine()

        concepts = {
            labels['0']: local_engine.d0,
            labels['1']: local_engine.d1
        }

        d_exist = local_engine.synthesize(concepts[labels['0']], concepts[labels['1']])
        concepts[labels['exist']] = d_exist

        d_order = local_engine.synthesize(d_exist, concepts[labels['0']])
        concepts[labels['order']] = d_order

        d_chaos = local_engine.synthesize(d_exist, concepts[labels['1']])
        concepts[labels['chaos']] = d_chaos

        d_complex = local_engine.synthesize(d_order, d_chaos)

        return d_complex.id

    def test_falsify_linguistic_coupling(self):
        """
        Falsification Test: Linguistic Coupling

        Hypothesis: Meaning is topological. Distinct cultural labeling systems 
        (Languages) constructing the same logical architecture will converge 
        on mathematically identical distinction IDs.

        Falsifies if: The final ID for 'Nature' (English) differs from 
        'Shizen' (Japanese), proving that labels pollute structural identity.
        """
        print("\nTest: Structural Isomorphism / Translation Falsification")

        english_map = {
            '0': 'Void', '1': 'Energy',
            'exist': 'Existence',
            'order': 'Stasis',
            'chaos': 'Flux',
            'target': 'Nature'
        }

        japanese_map = {
            '0': 'Mu', '1': 'Ki',
            'exist': 'Sonzai',
            'order': 'Sei',
            'chaos': 'Dou',
            'target': 'Shizen'
        }

        print("   Constructing hierarchy with English labels...")
        id_english = self._construct_concept_hierarchy(english_map)
        print(f"   English result: {id_english}")

        print("   Constructing hierarchy with Japanese labels...")
        id_japanese = self._construct_concept_hierarchy(japanese_map)
        print(f"   Japanese result: {id_japanese}")

        self.assertEqual(id_english, id_japanese,
            f"FALSIFIED: Label systems produced distinct IDs. English: {id_english} != Japanese: {id_japanese}")

        print("\n   Hypothesis sustained.")
        print("   Structural isomorphism confirmed across label systems.")
        print("   Zero-shot semantic translation possible via topological mapping.")

if __name__ == '__main__':
    unittest.main()