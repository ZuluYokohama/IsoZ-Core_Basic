---
name: sheaf-coderabbit
description: Run a local CodeRabbit-style review focused on infiltrating verified truth and streamlining semantic linkages using the sheaf-guardian engine. Best maneuver space for infil/exfil of consistency truth.
argument-hint: [file or --artifact "..."]
allowed-tools: ["Bash", "Read"]
---

# /sheaf-coderabbit

Local reviewer (in the spirit of CodeRabbit CLI) that uses the sheaf transducer as the core "infil/exfil" mechanism.

It takes code, maps it to stalks + linkages (restriction maps), computes the Laplacian truth (energy), identifies hot problematic linkages, and produces review comments that tell you exactly where to **infiltrate** corrections and how to **streamline** the code's semantic connections.

## Examples

```bash
# Review a file (infiltrates the whole file as artifact)
/sheaf-coderabbit src/auth.py

# Review a snippet with extra "truth" (a requirement) infiltrated first
/sheaf-coderabbit --artifact "def process_payment(...)" --infil-truth "Must maintain PCI compliance invariants on token stalks"
```

The script lives at `scripts/sheaf_coderabbit.py`. It can also be run directly from the terminal for CI or local pre-PR checks:

```bash
python scripts/sheaf_coderabbit.py path/to/module.py --format markdown
```

## Why this is the right infil/exfil operation
- **Infil point**: The `pulse` / `rotate_condition` call — this is where raw code enters the truth engine.
- **Exfil point**: The returned hot_linkages + verdict + Sheaf Consistency Report — this is where verified linkage truth comes out for the reviewer/agent to act on.
- The Python engine (not the LLM) owns the "truth" about whether linkages are consistent. This makes reviews isomorphic across models (Grok, Gemini, etc.).

Use this before big changes or in combination with the `sheaf-guardian` subagent for gated synthesis.
