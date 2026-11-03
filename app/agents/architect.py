"""Architect / Planner Agent for SYNAPSE-SWARM.

Deconstructs problem statements, formulates operational constraints,
identifies performance targets, and establishes invariants.
"""

import json
from typing import Any, Dict
from app.agents.base import BaseAgent


class ArchitectAgent(BaseAgent):

    def __init__(self):
        system_prompt = (
            "You are the Lead Systems Architect in an autonomous multi-agent swarm. "
            "Your role is to deconstruct complex problem statements into formal constraints, "
            "performance budgets (latency, memory, safety), and edge-case invariants. "
            "Always return clean structured JSON with fields: 'objective', 'constraints', "
            "'risk_vectors', 'target_metrics'."
        )
        super().__init__(
            name="Architect",
            role="System Decomposer & Planner",
            system_instruction=system_prompt,
            color="#6366f1",  # Indigo
            avatar="compass",
        )

    async def plan(
        self, problem_statement: str, domain: str = "general"
    ) -> Dict[str, Any]:
        prompt = (
            f"Analyze this problem specification:\n"
            f"Domain: {domain}\n"
            f"Problem: {problem_statement}\n\n"
            f"Provide a structured decomposition in JSON format:\n"
            f"{{\n"
            f'  "objective": "Concise core goal",\n'
            f'  "constraints": ["constraint 1", "constraint 2"],\n'
            f'  "risk_vectors": ["risk 1", "risk 2"],\n'
            f'  "performance_budget": {{"latency_ms": 50, "memory_complexity": "O(N)", "target_accuracy": 98.0}}\n'
            f"}}"
        )
        raw_res = await self.call_llm(prompt)
        try:
            # Strip markdown fences if present
            cleaned = (
                raw_res.strip()
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )
            return json.loads(cleaned)
        except Exception:
            return self.get_fallback_data(problem_statement)

    def get_fallback_response(self, prompt: str) -> str:
        return json.dumps(self.get_fallback_data("General Optimization"))

    def get_fallback_data(self, problem: str) -> Dict[str, Any]:
        return {
            "objective": f"Architectural plan for: {problem[:80]}",
            "constraints": [
                "Strict time complexity bound: sub-linear or linear O(N)",
                "Zero memory leak & thread-safe state guarantees",
                "Total defensive boundary checks for null, empty, and negative bounds",
            ],
            "risk_vectors": [
                "Unbounded recursion / Stack overflow under burst inputs",
                "Lock contention in shared buffer queue",
                "Silent degradation during unexpected edge schemas",
            ],
            "performance_budget": {
                "latency_ms": 45,
                "memory_complexity": "O(N)",
                "target_accuracy": 98.5,
            },
        }
