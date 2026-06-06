# specialized-agents

Grok Build plugin that delivers **custom agent types with unique mathematical verification features**.

**Flagship agent type: `sheaf-guardian`**

A read-mostly / plan-oriented subagent (`subagent_type: sheaf-guardian`) that **never emits a candidate artifact without first passing it through a sheaf-theoretic consistency gate** (Laplacian energy on semantic stalks + neural diffusion simulation + oracle offload for obstructions).

This gives you a practical "high-assurance" synthesis worker that standard `general-purpose`, `explore`, or `plan` agents lack.

## Unique Features (what makes this agent type special)

- **Stalk mapping (CRMtex-style)**: Relevant code symbols and intent fragments are turned into discrete stalks with restriction maps.
- **Sheaf Laplacian gating**: Before any output, `rotate_condition` is called. The 0-th sheaf Laplacian L°_F is computed. Only near-zero energy (in-kernel) states are allowed.
- **Bipartite Oracle + Omega Loop**: H¹ cohomological obstructions are packaged as Shape Pairs, offloaded (simulated), and coherence shifts (Δλ₁) are applied.
- **Sparse-only output contract**: Dense representations are forbidden. Outputs are described in terms of sparse global sections + Ternary Crystal basis routing.
- **Hardware piping simulation**: Time-slice flush + ioSurface-style handoff concepts are part of the contract (real NPU path in future hardware).
- **Mandatory Sheaf Consistency Report** in every significant response (energy, obstructions, verdict, handoff data).
- **Best-of-N within bounds**: Multiple micro-strategies can be evaluated; only the best kernel-resident one proceeds.
- Works beautifully with worktrees, personas (layer `implementer` or `reviewer` on top when the guardian has approved a plan), and the normal Grok Build subagent machinery.

## Installation (local development)

From inside this directory (or any project):

```bash
grok plugin add .
# or
grok --plugin-dir . 
```

Or install permanently for your user:

```bash
grok plugin install ./  --trust     # after you trust it
```

From a git repo later:

```bash
grok plugin install github:your-org/specialized-agents --trust
```

Check:

```bash
grok plugin list
grok inspect
# or inside TUI: Ctrl+L → Plugins tab
```

You should see:
- Agent: `sheaf-guardian`
- MCP server: `sheaf-condition-mcp`
- Skill: `sheaf-guardian`

## Usage

### Via subagent (recommended)

The parent agent will automatically discover `sheaf-guardian` as a valid `subagent_type`.

Natural language examples that should trigger it:

- "Use the sheaf-guardian to design a safe refactor of the auth + billing modules"
- "Have the sheaf-guardian review this large change for semantic consistency"
- "Implement the new query planner but run it through the topological guard first"

Inside the agent you will see tool calls to `rotate_condition` and `read_condition_state`.

### Direct invocation (if supported by your Grok Build version)

Some builds allow explicit agent selection in the `/agents` modal or via task tool parameters.

### The supporting skill

The `sheaf-guardian` skill loads automatically when relevant and gives the model (and you) the full background on the transducer, Laplacian math, and exact workflow.

### CodeRabbit-style CLI for Infil/Exfil of Truth & Linkages

We also ship `scripts/sheaf_coderabbit.py` (and the `/sheaf-coderabbit` command) — a local reviewer in the CodeRabbit CLI spirit.

It is explicitly built around the **best maneuver space** for this kind of work:

- **Infil operation**: Feed artifacts (code snippets or files) into `pulse` / `rotate_condition`. This is the controlled entry point where "truth" (external requirements, specs, or previous verdicts) can be infiltrated via `infiltrated_truth`.
- **Exfil operation**: Get back precise `hot_linkages` (the restriction maps / semantic edges with the highest disagreement energy), the Laplacian verdict, and structured suggestions.

This lets you (or an agent) **infiltrate** verified facts and **streamline** the actual linkages in the code at exactly the right points (function boundaries, call sites, symbol definitions — the natural infil/exfil boundaries of the program).

Run it directly:
```bash
python scripts/sheaf_coderabbit.py src/core.py
```

See `commands/sheaf-coderabbit.md` for the slash command version and more details on using it for pre-PR or CI "truth linkage" reviews. It works great alongside the `sheaf-guardian` subagent.

## Gemini Compatibility (Isomorphic Behavior)

The `sheaf-guardian` agent type is designed to deliver **isomorphic** (structurally equivalent) behavior whether the driving model is Grok or **Google Gemini**.

### Why it works isomorphically
The critical "guard" logic lives in the Python MCP server (`rotate_condition`, `read_condition_state`, the HybridConditionStateTransducer, Laplacian calculations, and Oracle).  
This server-side math is **completely independent** of the LLM. The only model-dependent part is the LLM's ability to:
- Know when to call the guard tools
- Respect the `CONSISTENT` / `OBSTRUCTED` verdicts
- Produce the required **Sheaf Consistency Report**

Gemini (especially `gemini-2.5-pro`) is actually excellent at the long, structured, step-by-step reasoning this agent requires.

### Recommended Configuration
Copy the relevant parts from `config/gemini-example.toml` into your `~/.grok/config.toml` or project `.grok/config.toml`:

```toml
[subagents.models]
sheaf-guardian = "gemini-2.5-pro"
```

You can keep your normal parent agent on Grok (or any model) while routing only the high-assurance `sheaf-guardian` work to Gemini.

### Tips for best results with Gemini
- The agent prompt already contains Gemini-specific guidance (strong numbered procedures, explicit tool call statements, and reinforced output contract).
- Prefer `gemini-2.5-pro` for complex refactors or anything where the stalk complex will be large.
- Use `gemini-2.0-flash` (or flash-thinking variants) for lighter guarded tasks where speed matters.
- Always verify that the MCP tool calls appear in the transcript — if the model skips `rotate_condition`, the isomorphism guarantee is lost.

### Launching with Gemini
```bash
# Entire session on Gemini
grok --model gemini-2.5-pro

# Or just let the subagent routing in config.toml do the work
grok
```

The mathematical core (sheaf theory, condition state, sparse routing) remains identical — only the "brain" deciding when to invoke it changes. This is what "isomorphic in Gemini" means for IsoZ-Core.

## Development & Validation

1. After changes to the agent definition, re-read or reload plugins (`r` in the plugins modal or `/plugins reload`).
2. Test the MCP server directly:

```bash
cd C:\GrokBuild\plugin
python scripts/mcp_server.py   # (will wait for JSON-RPC on stdin; use another terminal or test harness)
```

3. Exercise the engine:

```bash
python -c "
from scripts.rotary_condition_state import pulse, read_state
print(pulse('def process(x): return x*2 + 1'))
print(read_state())
"
```

4. To simulate a full guarded flow, ask Grok Build (with the plugin active) to perform a non-trivial task using the guardian.

## Requirements for full fidelity (optional)

The current implementation is pure-Python and self-contained (no heavy deps required to start using the agent type).

For production-grade spectral work you would add:

- `torch`, `torch-geometric`, `neural-sheaf-diffusion` or equivalent BuNN layers
- `scipy` (real sparse matrices)
- Lean 4 + `persistent-sheaf-laplacian` mathlib formalization
- Actual NPU / accelerator bindings for the hardware piping layer

The scripts contain clear extension points.

## Safety & Trust

This plugin registers an MCP server (`sheaf-condition-mcp`). Grok Build will ask you to trust it the first time (because it executes local Python code).

The agent itself is intentionally **plan / read-mostly** by default (permission_mode: plan) — it is designed to propose safe, verified plans and patches rather than blindly editing.

## Roadmap / Future Agents in this plugin

- `spectral-auditor` — deeper homology + persistent features for whole-codebase audits
- `topo-refactor` — a more aggressive (but still gated) editing agent that can apply approved sparse deltas
- Integration with real Lean proofs for critical kernels

## License

MIT (see LICENSE if present).

---

Built in the C:\GrokBuild\plugin workspace as a demonstration of a Grok Build plugin that adds a genuinely new agent capability with unique, mathematically grounded features.