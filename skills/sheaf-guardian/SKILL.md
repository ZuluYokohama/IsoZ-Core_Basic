---
name: sheaf-guardian
description: Activate when working with the sheaf-guardian agent type, topological verification, sheaf Laplacians, neural diffusion condition gating, rotary_condition_state, or when you need the unique mathematical guardrails for synthesis / refactoring. Provides the full context on the HybridConditionStateTransducer, oracle routing, and output constraints.
---

# Sheaf Guardian Skill

This skill supplies the detailed operational knowledge for the `sheaf-guardian` custom agent type provided by this plugin.

## When Grok Automatically Loads This
- User mentions "sheaf", "laplacian", "condition state", "topological guard", "spectral", "H1 knot", "oracle offload", "rotary condition", or "sheaf-guardian".
- The main agent decides to spawn `subagent_type: sheaf-guardian`.
- You are about to perform non-trivial generation that should be gated.

## The Unique Value of This Agent Type
Standard agents (general-purpose, explore, plan) can hallucinate or produce locally plausible but globally inconsistent changes.

`sheaf-guardian` adds a hard **topological consistency layer**:

- Maps semantic intent + code symbols to **discrete stalks** (CRMtex-style).
- Builds a **sheaf** over a Vietoris-Rips complex derived from the relevant code fragment.
- Before any output, pulses the **HybridConditionStateTransducer** (via MCP `rotate_condition`).
- Computes a **Sheaf Laplacian** L⁰_F. Only zero-energy (in-kernel) states are allowed to proceed.
- Obstructions (H¹ knots) are packaged as Shape Pairs and routed via the **Bipartite Oracle** (simulated remote resolution + coherence shift Δλ₁).
- Final artifacts are forced through **sparse geometric** (not dense tensor) representations and hardware routing simulation (Prime actuator).

This gives a practical approximation of "provable" or at least "spectrally verified" generations on edge hardware with strict memory bounds.

## Core MCP Tools (always available when this plugin is active)
- `rotate_condition(artifact: string, context?: string)` → Runs pulse, returns energy, kernel_member, obstruction, oracle_action if needed, and a clear VERDICT.
- `read_condition_state()` → Full current stalks, energy history, oracle stats, consistency radius.

**Golden Rule**: In a `sheaf-guardian` session, **call rotate_condition on every major candidate fragment** before presenting it to the user or writing files. Respect the verdict.

## Recommended Workflow When Using the Agent
1. Parent agent identifies a high-risk task.
2. Spawn `subagent_type: sheaf-guardian` (optionally with a persona like `implementer` or `researcher` layered if supported).
3. The guardian will:
   - Explore (read-only first).
   - Map symbols to stalks.
   - Pulse conditions frequently.
   - Only emit plans/patches that are CONSISTENT.
   - Produce the mandatory **Sheaf Consistency Report** section.
4. On obstruction, the guardian surfaces the Shape Pair / oracle result. Parent can decide to iterate, simplify the change, or ask for human guidance.
5. Handoff to a regular implementer subagent only with the guardian's approved artifacts + report.

## Implementation Notes (for plugin authors / advanced users)
- The MCP server lives at `scripts/mcp_server.py` (FastMCP preferred, minimal JSON-RPC stdio fallback included).
- Core math lives in `rotary_condition_state.py` (transducer + laplacian sim) + `oracle.py` + `hardware_piping.py`.
- Real deployments would wire:
  - `neural-sheaf-diffusion` (PyTorch Geometric Bundle Neural Networks)
  - `persistent-sheaf-laplacian` (Lean 4 verified)
  - Actual NPU / ioSurface zero-copy + RISC-V Torus routing
- The 6GB UMA envelope and "no dense tensors" rule are first-class constraints in the agent's system prompt.

## Testing the Guard
Inside a Grok Build session with this plugin loaded:

```
/plugins list
# should show specialized-agents providing the sheaf-guardian agent and the MCP

# Then ask something risky
"Use the sheaf-guardian to design a safe incremental refactor of <complex module>"
```

The agent should proactively call the rotate_condition tool (visible in tool call log) and include the Sheaf Consistency Report.

## References in this plugin
- agents/sheaf-guardian.md — the actual agent definition and full system prompt
- scripts/*.py — the complete (simulated but functional) engine
- .mcp.json — how the server is registered

This combination gives Grok Build a genuinely unique agent type that no other current offering has: **spectrally and topologically gated code synthesis**.