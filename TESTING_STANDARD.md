# Testing Standards

## Philosophy

The Distinction Engine test suite employs falsification methodology. Tests are designed to attack hypotheses, not validate them. A hypothesis is considered sustained only when rigorous attempts to falsify it fail.

**Core principle**: Truth is established through failure to prove wrong, not through attempts to prove right.

## Falsification Approach

### Structure

Every research test must contain three components:

1. **Hypothesis**: Clear statement of the expected emergent property or behavior
2. **Falsification Target**: Specific condition that would prove the hypothesis wrong
3. **Measurement**: Precise methodology for detecting the falsification condition

### Example

```python
"""
Arrow of Time Test Suite

Tests whether causal radius increases monotonically during evolution,
indicating irreversible time arrow rather than stagnant dynamics.

Falsification Target:
Time reversal - causal radius decreases between epochs, proving
reversible or stagnant temporal dynamics.
"""
```

## Writing Tests

### Test Method Structure

```python
def test_falsify_hypothesis_name(self):
    """
    Falsification Test: Hypothesis Name

    Hypothesis: Clear statement of expected emergent behavior.

    Falsifies if: Specific threshold or condition that indicates failure.

    Measurement:
    - Methodology step 1
    - Methodology step 2
    - Comparison against threshold
    """
```

### Assertion Format

Assertions must explicitly state the falsification condition:

```python
self.assertGreater(value, threshold,
    f"FALSIFIED: Description of what failed (metric: {value:.2f}).")
```

The assertion message must:
- Start with "FALSIFIED:"
- Explain what condition was violated
- Include relevant metric values

### Output Format

Test output must be professional, concise, and scientific:

**Good:**
```python
print("\nTest: Structural Fragmentation Falsification")
print("   Executing 1000 synthesis operations...")
print(f"   Largest component ratio: {ratio:.2%}")
print("\n   Hypothesis sustained.")
```

**Bad:**
```python
print("🧪 ATTACKING THE THEORY!")
print("⚠️ Running the 'Big Test'...")
print("✨ Theory VALIDATED! ✨")
```

Avoid:
- Emojis or special characters
- Informal language ("attacking", "validated", scare quotes)
- Dramatic emphasis
- Numbered procedural comments in code

## Measurement Methodology

### Standard Helpers

Use consistent helper methods across tests:

```python
def _build_graph(self):
    """Convert engine state snapshot to NetworkX graph for analysis."""
    state = self.engine.get_state_snapshot()
    g = nx.Graph()
    g.add_nodes_from([d.id for d in state[0]])
    g.add_edges_from(state[1])
    return g
```

### Evolution Functions

Implement evolution logic specific to your test:

```python
def _evolve_substrate(self, steps: int):
    """
    Execute synthesis operations with [selection strategy].

    [Description of selection bias: random, degree-weighted, spatial, etc.]
    """
```

### Metric Selection

Choose metrics that directly measure the falsification target:

- **Causal radius**: `nx.shortest_path_length(g, origin, node)`
- **Clustering**: `nx.clustering(g, node)`
- **Connectivity**: `len(max(nx.connected_components(g), key=len))`
- **Degree distribution**: `dict(g.degree())`

## Rigor Requirements

### Statistical Validity

- Generate sufficient data (typically 1000+ synthesis operations)
- Use appropriate sample sizes for correlation tests
- Verify graph size meets minimum threshold before measurement

### Isolation

- Each test must be independent
- Use `setUp()` to create fresh engine instances
- Do not rely on state from other tests

### Reproducibility

- Set random seeds when determinism is required
- Document any probabilistic elements
- Ensure tests pass consistently across runs

## Failure Reporting

When a test fails, the output must clearly indicate:

1. Which hypothesis was falsified
2. What metric violated the threshold
3. The actual measured value

Example:

```
FAILED tests/test_time.py::TestTimeDynamics::test_falsify_arrow_of_time
AssertionError: FALSIFIED: Causal radius decreased from 12 to 11.
```

## Success Reporting

When a test passes, report sustained hypothesis with measured values:

```python
print(f"\n   Hypothesis sustained.")
print(f"   Causal radius increases monotonically (final radius: {final_radius}).")
```

## Template

Reference `tests/test_example.py` for a complete implementation demonstrating all standards.

## Key Principles

1. **Attack, don't validate**: Design tests to find failure modes
2. **Be specific**: Define precise falsification conditions
3. **Be honest**: Let the data determine outcomes
4. **Be clear**: Use professional, scientific language
5. **Be rigorous**: Generate sufficient data for statistical validity

Truth emerges from surviving rigorous attack, not from gentle confirmation.
