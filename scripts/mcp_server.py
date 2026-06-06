#!/usr/bin/env python3
"""
scripts/mcp_server.py
FastMCP Unified Runtime for the Sheaf Condition MCP.

Exposes:
  - rotate_condition(artifact, context?) -> condition pulse result + gating decision
  - read_condition_state() -> current transducer + oracle state

This server is launched by Grok Build (via .mcp.json) as a stdio MCP server.
The sheaf-guardian agent type is expected to call these tools before emitting
significant generated content.

Implements the "rotate_condition" and "read_condition_state" tools described in the spec.
"""

from __future__ import annotations
import asyncio
import json
import os
import sys
from typing import Any, Dict

# Prefer fastmcp if installed; fall back to a minimal stdio JSON-RPC loop that is MCP-compatible enough.
# Users: pip install "mcp[cli]" or "fastmcp"

try:
    from fastmcp import FastMCP  # type: ignore
    HAVE_FASTMCP = True
except Exception:
    HAVE_FASTMCP = False

# Import our local engine (must be in PYTHONPATH or same dir)
try:
    from rotary_condition_state import pulse, read_state, TRANSDUCER
    from oracle import handle_obstruction, ORACLE
except ImportError:
    # Allow running from within scripts/ dir
    sys.path.insert(0, os.path.dirname(__file__))
    from rotary_condition_state import pulse, read_state, TRANSDUCER  # type: ignore
    from oracle import handle_obstruction, ORACLE  # type: ignore


def _make_tool_response(result: Dict[str, Any]) -> Dict[str, Any]:
    # MCP tool responses are usually just the structured content
    return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}


# --------------------------------------------------------------------------------------
# FastMCP path (preferred)
# --------------------------------------------------------------------------------------
if HAVE_FASTMCP:
    mcp = FastMCP("sheaf-condition-mcp")

    @mcp.tool()
    def rotate_condition(artifact: str, context: str = "agent-generation") -> Dict[str, Any]:
        """
        Primary gating tool. The agent MUST call this (or read after) on candidate outputs.
        Runs the HybridConditionStateTransducer pulse + oracle handling if obstructed.
        """
        pulse_result = pulse(artifact, context)

        decision = {
            "verdict": pulse_result["verdict"],
            "energy": pulse_result["energy"],
            "kernel_member": pulse_result["kernel_member"],
            "obstruction": pulse_result.get("obstruction"),
            "delta_lambda": pulse_result["delta_lambda"],
            "consistency_radius": TRANSDUCER.ComputeConsistencyRadius(),
            # CodeRabbit-style linkage review info - best "maneuver space" for infil/exfil of truth
            "hot_linkages": pulse_result.get("hot_linkages", {}),
            "linkage_review": "Review these high-disagreement restriction maps (edges) between semantic stalks for refactoring opportunities to streamline truth.",
        }

        if not pulse_result["kernel_member"] and pulse_result.get("obstruction"):
            oracle_action = handle_obstruction(
                pulse_result["energy"],
                pulse_result.get("obstruction"),
                list(TRANSDUCER.state.stalks.keys()),
            )
            decision["oracle_action"] = oracle_action
            decision["recommendation"] = "DO NOT EMIT. Resolve obstruction or request oracle correction first. Focus infil/exfil at the hot_linkages above."

        decision["pulse_summary"] = pulse_result
        return decision

    @mcp.tool()
    def read_condition_state() -> Dict[str, Any]:
        """Returns full current transducer state + oracle stats for inspection / debugging."""
        state = read_state()
        state["oracle"] = ORACLE.get_stats()
        state["transducer_class"] = "HybridConditionStateTransducer"
        return state

    def main():
        print("Starting FastMCP sheaf-condition server...", file=sys.stderr)
        mcp.run()

# --------------------------------------------------------------------------------------
# Minimal stdio MCP-compatible fallback (no external deps beyond stdlib)
# This speaks a subset of MCP JSON-RPC over stdio so Grok can still use the tools.
# --------------------------------------------------------------------------------------
else:
    class MinimalMCP:
        def __init__(self):
            self.tools = {
                "rotate_condition": {
                    "description": "Run sheaf condition pulse / Laplacian energy gate on an artifact. Returns verdict + oracle resolution if needed.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "artifact": {"type": "string"},
                            "context": {"type": "string", "default": "agent-generation"},
                        },
                        "required": ["artifact"],
                    },
                },
                "read_condition_state": {
                    "description": "Read current global sheaf condition state, energy, stalks, oracle stats.",
                    "inputSchema": {"type": "object", "properties": {}},
                },
            }

        def handle_request(self, req: Dict[str, Any]) -> Dict[str, Any] | None:
            method = req.get("method")
            params = req.get("params") or {}
            rid = req.get("id")

            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": rid,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "sheaf-condition-mcp", "version": "0.1.0"},
                    },
                }

            if method == "tools/list":
                tools_list = []
                for name, meta in self.tools.items():
                    tools_list.append({
                        "name": name,
                        "description": meta["description"],
                        "inputSchema": meta["inputSchema"],
                    })
                return {"jsonrpc": "2.0", "id": rid, "result": {"tools": tools_list}}

            if method == "tools/call":
                name = params.get("name")
                arguments = params.get("arguments") or {}

                if name == "rotate_condition":
                    artifact = arguments.get("artifact", "")
                    context = arguments.get("context", "agent-generation")
                    result = rotate_condition_fallback(artifact, context)  # type: ignore[name-defined]
                    return {"jsonrpc": "2.0", "id": rid, "result": result}

                if name == "read_condition_state":
                    result = read_condition_state_fallback()  # type: ignore[name-defined]
                    return {"jsonrpc": "2.0", "id": rid, "result": result}

                return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"Unknown tool {name}"}}

            # notifications etc. - ignore for minimal
            return None

    def rotate_condition_fallback(artifact: str, context: str = "agent-generation") -> Dict[str, Any]:
        pulse_result = pulse(artifact, context)
        decision: Dict[str, Any] = {
            "verdict": pulse_result["verdict"],
            "energy": pulse_result["energy"],
            "kernel_member": pulse_result["kernel_member"],
            "obstruction": pulse_result.get("obstruction"),
            "delta_lambda": pulse_result["delta_lambda"],
            "consistency_radius": TRANSDUCER.ComputeConsistencyRadius(),
            "pulse_summary": pulse_result,
        }
        if not pulse_result["kernel_member"] and pulse_result.get("obstruction"):
            decision["oracle_action"] = handle_obstruction(
                pulse_result["energy"], pulse_result.get("obstruction"), list(TRANSDUCER.state.stalks.keys())
            )
            decision["recommendation"] = "DO NOT EMIT until obstruction resolved."
        return decision

    def read_condition_state_fallback() -> Dict[str, Any]:
        state = read_state()
        state["oracle"] = ORACLE.get_stats()
        state["transducer_class"] = "HybridConditionStateTransducer (minimal)"
        return state

    def main():
        server = MinimalMCP()
        # Simple line-based JSON-RPC loop
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
            except Exception:
                continue
            resp = server.handle_request(req)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    main()
