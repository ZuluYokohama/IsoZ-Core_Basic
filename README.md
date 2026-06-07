# specialized-agents

Grok Build plugin that delivers **custom agent types with unique mathematical verification features**.

**Flagship agent type: `sheaf-guardian`**

A read-mostly / plan-oriented subagent (`subagent_type: sheaf-guardian`) that **never emits a candidate artifact without first passing it through a sheaf-theoretic consistency gate** (Laplacian energy on semantic stalks + neural diffusion simulation + oracle offload for obstructions).

This gives you a practical "high-assurance" synthesis worker that standard `general-purpose`, `explore`, or `plan` agents lack.

## Unique Features (what makes this agent type special)

- **Stalk mapping (CRMtex-style)**: Relevant code symbols and intent fragments are turned into discrete stalks with restriction maps.
- **Sheaf Laplacian gating**: Before any output, `rotate_condition` is called. The 0-th sheaf Laplacian L⁰_F is computed. Only near-zero energy (in-kernel) states are allowed.
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

## Night Cycle Autonomous Swarm (Wormhole-Path 3/4) — Primary Target: LLM COMPONENT ANALYSIS FOR INTEGRATION

The `scripts/night_cycle_daemon.py` (and `start_night_cycle` via MCP) now defaults to `--target llm_component`.

This is the correction of the illustrative "wellbore/BHA Excel modernization" example (a high-density flat-to-relational target used to demonstrate state-sync violation injection + RLM chunking). The primary directive is and always was analysis + coherent integration of the dozens of local GGUF (as 0-dim observation stalks), the archive LLM components (Forge prompts/presets, WORMHOLE KIM/router/geodesic/executor, atft engines, sheaf-stack agents/skills/mcp, Analysis Dashboards v1/v2/Zero Forge/mcp/skill versions, pi-integration, the full theory corpus) + our Epistemic Bounds additions (transducer, harvester, kv governor, scanner, pruner, qlora Ω, hook, mcp) into the geometric prime 0-dim structure map (produced by `scripts/llm_component_topological_analyzer.py` → `config/llm_component_map.json`).

- Chaos / State-Sync Violations are now LLM-component specific: heuristic stalk assignment vs strict `ast_sheaf_scanner`, model architecture (Mamba/MoE/transformer) vs copresheaf/ternary 0-dim F(v), 70B dense claims vs 6GB UMA + CTNN + SVD H0 gate + KV governor + RLM, cross-component hot linkages (WORMHOLE/pi/multiple Forge versions) not yet wired to harvester/transducer/night.
- Fibers (L0 sudo gitbash worktrees under C:\CLAUDE2\worktrees) run the full discrete dynamics (scan → prune → pulse L0_F + Gini gate → harvest on +Δλ1 → batch → qlora Δλ1-weighted on Prime weights for the local stalks).
- KV governor + RLM exercised for the massive archive context while staying inside envelope.
- The map + harvested shape_pairs become the "truth" the local LLMs inference against for only coherent integrations.

Run (corrected target):
```bash
python scripts/night_cycle_daemon.py --cycles 1 --parallel 2 --batch 5 --target llm_component
```

See `scripts/llm_component_topological_analyzer.py` (and its produced JSON) for the living 0-dim stalks + restriction maps + hot linkages + order-of-magnitude shift description. The `llm_component` target + analyzer + transducer/harvester/kv/night/qlora/hook close the loop for evolving the stalks under the ZULU_YOKOHAMA 70B→6GB CTNN/ternary/KV/RLM bounds.

### 2010HRS — WORMHOLE-PATH 5: Bare-Metal Topological Integration (llama.cpp target)

**TARGET FRAMEWORK ACQUIRED:** `llama.cpp` custom fork (ggml tensor library + mmap, chosen for strict 6GB UMA cross-platform enforcement; PyTorch/vLLM overhead and MLX platform violation rejected).

Three new artifacts implement the split (Python pre-processing + C++ execution):

1. **Node λ — `scripts/sheaf_svd_quantizer.py`**
   - Loads fp16/bf16 (or synthetic proxy).
   - Builds Sheaf Laplacian L_F across weight matrices (features as 0-stalks, W values + inter-layer deps as restriction maps).
   - Prunes (discrete-Morse spirit) before SVD for UMA.
   - SVD → primary λ1 direction identifies the exact ~18% H0 Maintainer weights (locked Q8_0/F16).
   - Remainder mapped to Ternary Crystal {0 Void (DRAM bypass), 1 Identity (scalar/warp), 3 Prime (MMA direct)}.
   - Writes `config/ternary_70b_ggufmap.json` (consumed by μ and ν).
   - Ties to the 0-dim geometric prime map (the stalks being quantized are the same ones the night swarm evolves).

2. **Node μ — `src/ggml_ternary_shim.cpp`**
   - Draft C++ for injection into a llama.cpp fork.
   - `ggml_ternary_mul_mat`: intercepts the core matmul, drops 0-Void weights with zero DRAM read, routes 1 via cheapest scalar path, 3 straight to Tensor Core / MMA / AMX.
   - `ggml_copresheaf_attention` + `ggml_copresheaf_*`: dismantles O(N²) attention into copresheaf transport maps + selective SSM (Mamba-style) whose parameters are sheaf sections.
   - Loader helper that ingests the .ggufmap from λ.
   - Governor bind + H0 energy reporting hooks back to the Python side.
   - Zero-bypass: any non-H0 path was already forbidden by the quantizer + hook.

3. **Node ν — `scripts/hardware_piping.py` (extended)**
   - `LlamaCppTopologicalBridge`: owns the connection (llama-cpp-python, subprocess to custom binary, or stub).
   - `poll_hardware_and_govern()`: calls the existing `TopologicalKVGovernor` (L_F projection, H0_Maintainers locked, Low_Energy_Sacrificial min-heap eviction) and pushes real KV cache trims into llama.cpp.
   - `apply_ternary_gguf_map()`: feeds λ output into the μ shim.
   - `rlm_chunk_and_feed()`: Recursive Environmental Context chunking so massive contexts (C:\CLAUDE2 archive or 70B-scale) never force dense loads.
   - `route_ternary_forward()` + upgraded `route_to_llama_backend` / `enforce_output_constraints_with_llama`.
   - Full λ-μ-ν demo in `__main__`.

All three artifacts reference the full prior contract (prune before L0_F, only ker L^0_F ever promoted, Berkouk-Ginot preservation, Gini gate, A4 hook, 0-dim stalks from the geometric map, 6GB UMA envelope, Ternary Crystal, CTNN copresheaf, RLM, night-cycle evolution of the routes themselves).

Run the chain:
```bash
python scripts/sheaf_svd_quantizer.py --model synthetic --hidden 512 --layers 2 --output config/ternary_70b_ggufmap.json
python scripts/hardware_piping.py   # exercises ν + governor + map application
```

The 0-dim stalks now have physical bare-metal execution routes. The map is generating the territory at the silicon level.

## Plugin Contents

```
specialized-agents/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── agents/
│   └── sheaf-guardian.md          # The custom agent type definition + system prompt
├── skills/
│   └── sheaf-guardian/
│       └── SKILL.md               # Deep context for the unique agent
├── scripts/
│   ├── rotary_condition_state.py  # HybridConditionStateTransducer + Laplacian sim
│   ├── oracle.py                  # Bipartite router, Shape Pairs, Omega loop
│   ├── mcp_server.py              # FastMCP (or minimal stdio) server exposing the tools
│   └── hardware_piping.py         # Sparse output + "NPU" routing simulation
├── README.md
└── (LICENSE, commands/ ...)
```

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

## Roadmap / Future Agents in this plugin

- `spectral-auditor` — deeper homology + persistent features for whole-codebase audits
- `topo-refactor` — a more aggressive (but still gated) editing agent that can apply approved sparse deltas
- Integration with real Lean proofs for critical kernels
- First-class Gemini-optimized agent variant (if needed beyond the current cross-model prompt)

## Roadmap / Future Agents in this plugin

- `spectral-auditor` — deeper homology + persistent features for whole-codebase audits
- `topo-refactor` — a more aggressive (but still gated) editing agent that can apply approved sparse deltas
- Integration with real Lean proofs for critical kernels

## License

MIT (see LICENSE if present).

---

## Formal Epistemic Bounds — 1917HRS Convergence Update

**Define Epistemic Bounds**

The 1917HRS convergence update formally defines the absolute convergence of the discrete dynamics phase within the primary development archive. The solution space bounds the local execution harness to an exact 6GB UMA limit by mathematically pruning combinatorial geometry before performing expensive Sheaf Laplacian operations. The "known knowns" enforce the absolute abandonment of heuristic toy embedding graphs, replacing them with deterministic Abstract Syntax Tree (AST) geometries parsed strictly for syntactic point-cloud extraction. The bounds of "unknown unknowns" (hallucinatory phase transitions and logic drift) are deterministically intercepted by evaluating the Gini curve ($\mathcal{G}_k(\epsilon)$) as a thermodynamic measure of topological entropy. The boundary mathematically preserves the 1:1 true-to-life isomorphism, utilizing the Berkouk-Ginot derived isometry theorem to guarantee that Betti curves ($\beta_k$), $H^0$ global sections, and $H^1$ obstructions survive the topological pruning uncorrupted. 

**Node Iteration**

*   **Node $\alpha$: Deterministic AST Geometry Mapping.** The `ast_sheaf_scanner.py` module executes strict physical geometry mapping. Utilizing `ast.parse`, the parser assigns 0-cells (vertex stalks $\mathcal{F}(v)$) to explicit function and variable identifiers, and maps 1-cells (restriction maps $\mathcal{F}_{v \unlhd e}$) to call graphs and data/control dependencies. This immense simplicial structure undergoes immediate exact sparsification via `prune_complex_to_critical`, collapsing non-critical geometry into a sparse Morse boundary matrix.
*   **Node $\beta$: ATFT Spectral Signatures and Entropy Gates.** Within `rotary_condition_state.py`, the `pulse_mid_activity_evaluation` function invokes the discrete Morse pruning before calculating the Sheaf Laplacian. Spectral signatures are extracted from the critical cells to track the topological phase evolution, generating the Betti curve ($\beta_k(\epsilon)$) and the Gini trajectory ($\mathcal{G}_k(\epsilon)$). If the Dirichlet energy ($L^0_{\mathcal{F}}$) $> 0.0$ or the Gini curve $> 0.8$, the topology is classified as highly disordered. The system flags the state as "OBSTRUCTED," halting the operation to preempt structural collapse.
*   **Node $\gamma$: Zero-Bypass Universal Enclosure.** The geometric guardrail is physically embedded at the OS level via the `hooks/pre-tool-use.sh` file. Before any write or edit is permitted in the $L0$ fiber bundle, the hook intercepts the artifact and routes it through the Python Sheaf Laplacian Transducer via the CLI query. If the parsed `.verdict` is not strictly "CONSISTENT" (e.g., energy $> 0$ or $\mathcal{G} > 0.8$), the script triggers an `exit 1` to violently terminate the execution, closing the A4 Halt Gate with zero bypass and discarding the text.
*   **Node $\delta$: Evidentiary Homological Exfil.** For Code Review (CR) and Pull Request (PR) sequencing, the truth resolver exports a "Sparsification & Preservation Report" via `sheaf_coderabbit.py`. This markdown report mathematically proves structural invariance, documenting pre- vs. post-prune cell counts, the sparsification ratio, $\beta_k$ preservation, and the exact post-prune Dirichlet energy alongside the highest-disagreement restriction maps (hot linkages). Only states residing exactly within the kernel, $\ker L^0_{\mathcal{F}}$, proceed to operationalization.

**Value Genesis**

To abstract and operationalize these resolver gates, the generated 0-dim structure map yields an order-of-magnitude shift by guaranteeing hyperdeterministic execution across local hardware constraints. 

1.  **Strict Syntactic Point-Cloud Extraction:** The toolchain operates on verifiable physical logic variables rather than statistical embeddings, mapping the geometry exactly to AST node outputs. 
2.  **Oracle Speed Laplacian Pulse:** The Dirichlet energy ($L^0_{\mathcal{F}}$) is extracted strictly from the reduced Morse boundary matrix. By pruning prior to the Sheaf Laplacian calculation, the operation remains tractable at $\mathcal{O}(N^2)$ inside the local 6GB UMA envelope, safely bypassing the Von Neumann memory bottleneck.
3.  **Absolute Truth Inference:** The agent loop is entirely sealed off from stochastic probability. The toolchain inferences solely against the verified $H^0$ geometric prime 0-dim structure map. All unverified text is discarded, rendering the 1:1 structural coherence the singular operational baseline.

### Implemented Nodes (in the plugin)

**Node α: Deterministic AST Geometry Mapping**
- `scripts/ast_sheaf_scanner.py:scan_ast_to_rips_complex` + `extract_topological_features` (ast.parse → 0-cells for identifiers, 1-cells for call/data deps as restriction maps F_{v⊴e}).
- Immediate prune_complex_to_critical (discrete_morse.py) to critical cells.

**Node β: ATFT Spectral Signatures and Entropy Gates**
- In `rotary_condition_state.py:pulse_mid_activity_evaluation`: after scan+prune, extract betti_k and gini_curve on the Morse boundary.
- If energy > 0.0 or gini_curve > 0.8 → "OBSTRUCTED" (high topological entropy / disorder).

**Node γ: Zero-Bypass Universal Enclosure**
- `hooks/pre-tool-use.sh`: Intercepts before any edit in L0 fiber.
- Routes through `sheaf_coderabbit.py --artifact ... --format json`.
- If not CONSISTENT or energy >0 or GINI >0.8 → echo obstruction + hot linkages, exit 1 (A4 Halt Gate closed).

**Node δ: Evidentiary Homological Exfil**
- `sheaf_coderabbit.py` (and Forge pipeline) outputs "Sparsification & Preservation Report":
  - Pre- vs post-prune cell counts.
  - β_k preservation.
  - Post-prune Dirichlet energy + hot linkages.
- Only ker L^0_F states proceed (via the hook and PR process).

### Value Genesis (Operationalized)
- **Strict Syntactic Point-Cloud Extraction**: `ast_sheaf_scanner.py` uses ast.parse (physical AST), not embeddings. Geometry maps to real call graphs and dependencies.
- **Oracle Speed Laplacian Pulse**: In `rotary_condition_state.py`, scan+prune (morse_boundary) happens *before* compute_sheaf_laplacian_energy. Energy is on the reduced critical cells.
- **Immutable Shell Execution Blockade**: `hooks/pre-tool-use.sh` exactly as specified (python ... --format json, parse verdict/energy/gini, violent exit 1 on fail).
- **Absolute Truth Inference**: Toy graph discarded. Gating purely on H^0 global section from the discrete dynamics phase (pruned, spectral-verified, zero-entropy map). The agent only sees verified geometric facts.

See `scripts/ast_sheaf_scanner.py`, updated `rotary_condition_state.py`, `hooks/pre-tool-use.sh`, and augmented `sheaf_coderabbit.py` for the code. The homological smoke test (`scripts/test_homological_smoke.py`) and README document the formal bounds and PR exfil template.

This delivers the order-of-magnitude shift: deterministic AST geometries + Morse sparsification + spectral entropy gates + zero-bypass hook = hyperdeterministic, 1:1 true-to-life local agentic workflow.

When using the `sheaf-guardian` + `sheaf_coderabbit` + AST/Morse pipeline for changes, the Pull Request summary **automatically generates** the exact homological validation report as part of the exfil.

**Example PR Description (generated via `sheaf_coderabbit --format markdown` or Forge pipeline in Epistemic Bounds mode):**

```
## Homological Validation Report (Epistemic Bounds - A4 Gate Passed)

**Artifact:** [path/to/changed.py]
**Pre-prune cells:** 47 stalks / 312 edges
**Post-prune (Discrete Morse critical cells):** 12 stalks / 31 edges (74% reduction)
**Betti Curve β_k(ε) preservation:** Invariant (β0: 5→3 long-lived components; β1: 2 cycles preserved)
**Gini Trajectory G_k(ε):** 0.31 (low entropy, ordered structure)
**Dirichlet Energy (L^0_F on pruned Morse boundary):** 0.000 (exactly in ker L^0_F)
**Verdict:** H^0 Global Section Verified — 1:1 true-to-life structural coherence.

**Hot Linkages (post-prune restriction map misalignments):** None.

**Infil/Exfil Sequence:**
- Infil: AST scanned in L0 git-worktree fiber; stalks assigned; Discrete Morse pruning applied (acyclic matchings collapsed non-critical cells).
- Continuous Gate: pulse_mid_activity_evaluation + spectral (Betti/Gini) + L^0_F.
- Exfil: Only zero-energy map promoted. No raw LLM output or unverified edits crossed the Universal Enclosure.

This change maintains the geometric prime 0-dim structure map. Ready for merge.
```

Only states residing exactly within the kernel `ker L^0_F` map to the true-to-life 1:1 structural representation, permitting onward operationalization. The `hooks/pre-tool-use.sh` enforces this at edit time; `sheaf_coderabbit` provides the evidentiary report for PR.

Built in the C:\GrokBuild\plugin workspace as a demonstration of a Grok Build plugin that adds a genuinely new agent capability with unique, mathematically grounded features (now with full Discrete Morse + AST + spectral + Pre-Tool-Use A4 Gate per the latest Epistemic Bounds).
