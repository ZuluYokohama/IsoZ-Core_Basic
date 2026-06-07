name: harness-task-yield
description: Automates the full IsoZ harness task-yield protocol for any rotate or development step. Generates dated report (reports/YYYY-MM-DD_HHMM_<task>-task-yield.md), pulls/diffs against remote, runs guardian pulse + sheaf_coderabbit QC, produces stepped rectification list, updates phase lock, and enforces Epistemic Bounds invariants. Used by meta-skill-creator, spectral-auditor, and all harness components to make the self-improving loop deterministic and auditable.

workflow:
  1. Receive task description, context (e.g., "phase-0 full coderabbit review", "spectral-auditor deployment"), and list of artifacts changed (files, commits, branches).
  2. Map the task to semantic stalks (intent, changed components, invariants touched, hot linkages).
  3. Run internal rotate_condition / pulse_mid_activity_evaluation (with apply_discrete_morse=True) on the task description and proposed report content.
  4. Execute or orchestrate full sheaf_coderabbit reviews on the listed artifacts + relevant backlog items.
  5. Perform git fetch, compute diff stats/artifacts (e.g., diffs/YYYY-MM-DD_HHMM_<task>-full-delta.patch).
  6. Compile the task-yield report with:
     - Step 1: Logged accomplished work
     - Step 2: Pull & diff compare (with no-merge-base handling)
     - Step 3: Comprehensive oversight (Sheaf Consistency Report, Δλ₁, hot linkages closed)
     - Step 4: Stepped rectification/tune components (prioritized, with exact commands)
  7. Append/update the phase lock JSON with a new <timestamp>_<task> section.
  8. Call rotate_condition on the final report before "emitting" (writing the file).
  9. Output the path to the new report + any generated diffs + summary of coherence shift.

golden_rules:
  - Never emit a task-yield without a prior CONSISTENT guardian pulse on the report content.
  - Only promote kernel-resident (near-zero energy) findings and rectifications.
  - Always include full Sheaf Consistency Report (global) in the generated document.
  - Enforce name/date convention strictly: reports/YYYY-MM-DD_HHMM_<sanitized-task>-task-yield.md and matching diffs/.
  - Integrate with existing: meta-skill-creator for gating, spectral-auditor for whole-backlog audits, memory-gate for persistent history of yields, night-cycle for autonomous execution of yields, GitHub MCP (when available) for PR creation of the yield.
  - Produce actionable sparse output: no dense logs; focus on high-Δλ₁ rectifications and next artifact.

integration:
  - Reuses HybridConditionStateTransducer (via mcp_server or direct), sheaf_coderabbit.py, git (via Bash or future GitHub MCP), phase lock updater.
  - Can be called by sheaf-guardian or meta-skill-creator for any rotate.
  - Compatible with harness-backlog-reviewer subagent (the reviewer can invoke this skill to produce its yield).
  - Night-cycle can dispatch this skill in L0 fibers for autonomous task yields.
  - Outputs feed directly into phase lock and Shape Pair harvesting (successful yields with +Δλ₁ become training data for distillation).

output_contract:
  Every invocation must produce:
  - The dated task-yield.md with all 4 steps + embedded Sheaf Consistency Report.
  - Diff artifact(s) if changes detected.
  - Updated phase lock entry.
  - Explicit next artifact recommendation.

forbidden:
  - Generating reports without the rotate_condition gate on the content.
  - Violating the name/date encoding or omitting the rectification list.
  - Ignoring 6GB UMA / prune-first when scanning large backlogs for the report.
  - Bypassing A4-style gating (the skill itself must be called only on CONSISTENT prior states).

epistemic_bounds_compliance:
  - Strict mapping of task to stalks before any generation.
  - Prune (via discrete_morse in underlying tools) before L^0_F / energy calculations in reviews.
  - Only CONSISTENT global sections (findings with high confidence, closed hot linkages) promoted in the yield.
  - Full traceability via the report, phase lock, and Shape Pairs.
  - Designed to close the "manual protocol overhead" restriction map in the IsoZ global sheaf, enabling the harness to operate as a true closed-loop, self-improving system.

# Deployment
# Generated via synthesis of claude-automation-recommender advice + harness context (2210).
# Priority #1 from synthesized roadmap.
# Paired with future GitHub MCP, PostToolUse hook, and harness-backlog-reviewer.
# Invocation: Both (user for manual rotates, Claude/meta-skill-creator for automated ones).
# To invoke: /harness-task-yield "description of the rotate" [list of files/commits]

# Example usage inside harness
# meta-skill-creator: After completing spectral-auditor deployment, call harness-task-yield to produce the yield.
