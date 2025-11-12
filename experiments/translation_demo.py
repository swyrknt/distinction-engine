"""
Topological Semantic Mapping Demo: English <-> Japanese

Demonstrates automatic structural equivalence detection across symbolic systems.
When two systems construct identical logical structures using different labels,
matching topological IDs enable zero-shot semantic mapping without graph traversal.

Mechanism:
1. Build a concept hierarchy in English.
2. Build the same hierarchy in Japanese.
3. Match topological IDs to create translation dictionary.

This demonstrates practical application of content-addressable semantics:
identical structures produce identical IDs regardless of symbolic labels.
"""

import sys
import os
# Add parent directory to path to import engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine import Distinction, DistinctionEngine

class LinguisticMind:
    def __init__(self, language_name):
        self.language = language_name
        self.engine = DistinctionEngine()
        self.vocab = {}   # Hash -> Word
        self.concepts = {} # Word -> Hash

        self.d0 = self.engine.d0
        self.d1 = self.engine.d1

    def label_axiom(self, distinction, word):
        """Assign a word to a fundamental axiom."""
        self.vocab[distinction.id] = word
        self.concepts[word] = distinction.id

    def ponder(self, word_a, word_b, new_word):
        """
        Synthesize two concepts to create a third, then assign label.

        Retrieves distinctions by concept labels, performs synthesis,
        and maps result to new label in this language's vocabulary.
        """
        id_a = self.concepts[word_a]
        id_b = self.concepts[word_b]

        d_a = self.engine.all_distinctions[id_a]
        d_b = self.engine.all_distinctions[id_b]

        new_d = self.engine.synthesize(d_a, d_b)

        self.vocab[new_d.id] = new_word
        self.concepts[new_word] = new_d.id

        print(f"[{self.language}] Synthesized: '{word_a}' + '{word_b}' -> '{new_word}'")
        return new_d

def run_translation_experiment():
    print("\nDual-Linguistic Topology Experiment")
    print("=" * 60)

    english = LinguisticMind("ENGLISH")
    japanese = LinguisticMind("JAPANESE")

    english.label_axiom(english.d0, "Void")
    english.label_axiom(english.d1, "Energy")

    japanese.label_axiom(japanese.d0, "無")
    japanese.label_axiom(japanese.d1, "気")

    print("\nEnglish conceptualization:")
    english.ponder("Void", "Energy", "Existence")
    english.ponder("Existence", "Void", "Stasis")
    english.ponder("Existence", "Energy", "Flux")
    english.ponder("Stasis", "Flux", "Nature")

    print("\nJapanese conceptualization:")
    japanese.ponder("無", "気", "存在")
    japanese.ponder("存在", "無", "静")
    japanese.ponder("存在", "気", "動")
    japanese.ponder("静", "動", "自然")

    print("\nTopological mapping:")
    print("Scanning for structural isomorphism...")
    print("-" * 60)
    print(f"{'TOPOLOGICAL HASH (ID)':<20} | {'ENGLISH':<15} | {'JAPANESE':<15}")
    print("-" * 60)

    matches = 0
    for distinction_id, eng_word in english.vocab.items():
        if distinction_id in japanese.vocab:
            jp_word = japanese.vocab[distinction_id]
            short_id = distinction_id[:12] + "..."
            print(f"{short_id:<20} | {eng_word:<15} | {jp_word:<15}")
            matches += 1

    print("-" * 60)
    if matches == 6:
        print("Translation accuracy: 100%")
        print("Semantic mapping achieved via topological identity.")
    else:
        print(f"Translation failed. Structures diverged ({matches}/6 matches).")

if __name__ == "__main__":
    run_translation_experiment()
