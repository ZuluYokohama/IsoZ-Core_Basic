---
name: sheaf-status
description: Show current condition state of the sheaf transducer (energy, kernel membership, recent oracle activity). Useful for debugging the sheaf-guardian agent.
argument-hint: [optional extra context]
allowed-tools: []
---

# /sheaf-status

Reads the live state from the sheaf-condition-mcp (via the tools exposed by this plugin) and prints a human-readable summary.

The model will call `read_condition_state` and format the result, including:

- Current stalk / edge counts
- Last Laplacian energy + kernel verdict
- Consistency radius
- Oracle offload stats
- Recent Δλ₁ coherence shifts

Use this when you want to inspect whether the topological guard is currently happy with the workspace state or carrying obstructions.