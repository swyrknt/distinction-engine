# Commenting Standard

## Philosophy

Comments should be **minimal, complete, and matter-of-fact**. Every comment must justify its existence by providing information not immediately evident from the code itself. Prefer self-documenting code over explanatory comments.

## Tone

- **Professional and concise**: Avoid informal language, dramatic punctuation, or unnecessary emphasis.
- **Direct**: State facts without hedging or embellishment.
- **Axiomatic**: Frame concepts in terms of fundamental principles and their logical consequences.
- **Uniform**: Maintain consistent structure and phrasing across the codebase.

## Structure

### Module-Level Docstrings

Every module should begin with a docstring that provides:

1. **Purpose**: One-sentence description of the module's role.
2. **Axioms/Principles**: Numbered list of fundamental concepts (if applicable).
3. **Context**: Brief explanation of how the module fits into the larger system.

**Example:**

```python
"""
Distinction Engine: A minimal axiomatic system for emergent computation.

Axioms:
1. Identity: A distinction is defined solely by its unique identifier.
2. Nontriviality: The system initializes with two distinct entities (0, 1).
3. Synthesis: Two distinctions combine deterministically to create a third.
4. Symmetry: Relationships are bidirectional and order-independent.
5. Irreflexivity: A distinction synthesized with itself yields itself.

This module implements a timeless, self-consistent graph where all entities
and relationships emerge from repeated application of the synthesis operation.
"""
```

### Class Docstrings

Classes should have docstrings that:

1. **State the core concept**: What the class represents or governs.
2. **Describe responsibilities**: What state or behavior it maintains.
3. **Note key properties**: Invariants, constraints, or emergent characteristics.

**Example:**

```python
class DistinctionEngine:
    """
    The singular process governing all state transformations.

    Maintains the complete universe state: all existing distinctions
    and their relationships. Operations are deterministic and local.
    Time is an emergent property, not a primitive.
    """
```

### Method/Function Docstrings

Methods should have docstrings when they:

- Implement a core axiom or principle
- Have non-obvious behavior or side effects
- Serve as public API endpoints

**Format:**

```python
def synthesize(self, a: Distinction, b: Distinction) -> Distinction:
    """
    Axiom: Synthesis.

    Combine two distinctions to produce a third. This is the sole
    generative operation. Deterministic, local, and parameter-free.
    Implements irreflexivity: synthesizing a distinction with itself
    returns the original distinction unchanged.
    """
```

For simple methods, keep it brief:

```python
def _add_relationship(self, id_a: str, id_b: str):
    """Axiom: Symmetry. Store relationships in canonical order."""
```

### Inline Comments

Use inline comments sparingly, only when:

- The code implements a subtle algorithmic detail
- There's a non-obvious reason for a particular approach
- Clarifying intent prevents future misunderstanding

**Format:**

```python
# Return existing distinction if already synthesized (timeless consistency)
existing = self.all_distinctions.get(new_id)
```

### Avoid

- **Redundant comments**: Do not describe what the code obviously does.

  ```python
  # BAD: Increment counter
  counter += 1
  ```

- **Procedural narration**: Do not number or enumerate steps unless they correspond to a formal algorithm.

  ```python
  # BAD:
  # 1. Create a new distinction
  # 2. Add it to the dictionary
  # 3. Return it
  ```

- **Informal language**: Avoid "just", "simply", "basically", asterisks for emphasis, or conversational tone.

- **Explanatory comments for poor code**: Refactor instead.

## Axiom References

When a comment references an axiom:

- Use the format: `Axiom: [Name].`
- Follow with a concise description if the connection is not obvious.
- Reference axioms defined in the module docstring when applicable.

## Examples

### Good

```python
def __init__(self):
    """Axiom: Nontriviality. Initialize the primordial pair."""
    self.d0 = Distinction(id="0")
    self.d1 = Distinction(id="1")
```

```python
@dataclass(frozen=True)
class Distinction:
    """
    Axiom: Identity.

    A distinction is defined solely by its unique identifier.
    All properties emerge from relationships with other distinctions.
    """
    id: str
```

### Bad

```python
# --- AXIOM 1: THE "THING" ---
# A Distinction is just its identity. It has no other properties.
```

```python
# We must now track distinctions *by their ID*
self.all_distinctions: Dict[str, Distinction] = {}
```

```python
# 1. Create a new, deterministic identity.
# 2. Check if this distinction *already exists*
#    This is a critical part of a timeless, self-consistent graph
```

## Summary

**Minimal**: Only comment what cannot be expressed in code.
**Complete**: Provide all necessary context for understanding.
**Matter-of-fact**: State what is, not what you think about it.
