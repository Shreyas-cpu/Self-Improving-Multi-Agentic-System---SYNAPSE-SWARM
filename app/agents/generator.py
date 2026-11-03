"""Generator Agent for SYNAPSE-SWARM.

Produces candidate algorithmic code and operational strategies.
Actively ingests learned rules from the Dynamic Knowledge Vault.
"""

from typing import Any, Dict, List, Optional
from app.agents.base import BaseAgent


class GeneratorAgent(BaseAgent):

    def __init__(self):
        system_prompt = (
            "You are the Lead Generator & Synthesis Agent in an autonomous self-improving multi-agent swarm. "
            "Your objective is to craft high-quality Python algorithms and solutions satisfying all architectural constraints. "
            "CRITICAL: When the Dynamic Knowledge Vault provides learned heuristics, you MUST strictly adhere to them "
            "and eliminate all anti-patterns spotted in earlier iterations."
        )
        super().__init__(
            name="Generator",
            role="Solution & Code Synthesizer",
            system_instruction=system_prompt,
            color="#10b981",  # Emerald Green
            avatar="code",
        )

    async def generate_solution(
        self,
        problem: str,
        architecture: Dict[str, Any],
        iteration: int,
        learned_rules_prompt: str,
        prior_feedback: Optional[str] = None,
        prior_solution: Optional[str] = None,
    ) -> Dict[str, Any]:
        prompt = (
            f"Problem Statement:\n{problem}\n\n"
            f"Architectural Plan:\n{architecture}\n\n"
            f"Current Iteration: {iteration}\n"
            f"{learned_rules_prompt}\n\n"
        )
        if prior_feedback and prior_solution:
            prompt += (
                f"### PRIOR FAILURE FEEDBACK:\n{prior_feedback}\n\n"
                f"### PRIOR SUB-OPTIMAL SOLUTION:\n{prior_solution}\n\n"
                f"Refactor and optimize the solution, resolving all defects and obeying all learned rules.\n"
            )
        else:
            prompt += (
                "Provide an initial functional implementation. Format clearly in Python.\n"
            )

        raw_res = await self.call_llm(prompt, temperature=0.3)
        return {
            "code": raw_res.strip(),
            "iteration": iteration,
            "rules_applied": (
                ["Active heuristics ingested"] if iteration > 1 else []
            ),
        }

    def get_fallback_response(self, prompt: str) -> str:
        # High quality fallback solution with standard progression
        if "Iteration: 1" in prompt:
            return (
                "# Iteration 1: Baseline Naive Implementation\n"
                "def solve_pipeline(data_stream):\n"
                "    results = []\n"
                "    # Naive nested loop O(N^2) without null checking\n"
                "    for item in data_stream:\n"
                "        val = item['metric']\n"
                "        for prev in results:\n"
                "            if prev['id'] == item['id']:\n"
                "                val += prev['metric']\n"
                "        results.append({'id': item['id'], 'aggregated': val})\n"
                "    return results"
            )
        else:
            return (
                "# Iteration 2/3: Self-Optimized & Hardened Solution\n"
                "from collections import defaultdict\n"
                "from typing import List, Dict, Any\n\n"
                "def solve_pipeline(data_stream: List[Dict[str, Any]]) -> List[Dict[str, Any]]:\n"
                "    # HEURISTIC INJECTED: O(N) Hashmap Lookup & Defensive Guards\n"
                "    if not data_stream:\n"
                "        return []\n\n"
                "    agg_map = defaultdict(float)\n"
                "    for item in data_stream:\n"
                "        if not isinstance(item, dict) or 'id' not in item or 'metric' not in item:\n"
                "            continue  # Defensive boundary guard\n"
                "        agg_map[item['id']] += float(item['metric'] or 0.0)\n\n"
                "    return [{'id': k, 'aggregated': v} for k, v in agg_map.items()]"
            )
