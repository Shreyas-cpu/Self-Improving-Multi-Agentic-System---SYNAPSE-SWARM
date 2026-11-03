"""Meta-Reflector Agent for SYNAPSE-SWARM.

The core cognitive engine of the self-improvement loop.
Conducts root-cause failure analysis and extracts immutable heuristic rules
to immunize subsequent agent generations.
"""

import json
from typing import Any, Dict, List
from app.agents.base import BaseAgent
from app.memory.vault import DynamicKnowledgeVault, HeuristicRule


class MetaReflectorAgent(BaseAgent):

    def __init__(self):
        system_prompt = (
            "You are the Meta-Reflective Learning Agent in an autonomous self-improving multi-agent system. "
            "Your critical task is meta-cognition: analyzing why earlier agent outputs failed or scored poorly, "
            "identifying the systemic root cause, and synthesizing actionable, generalized heuristic rules "
            "that prevent the swarm from repeating those mistakes. "
            "Output your synthesized heuristic as clean JSON."
        )
        super().__init__(
            name="Meta-Reflector",
            role="Self-Improvement & Heuristic Synthesizer",
            system_instruction=system_prompt,
            color="#a855f7",  # Purple
            avatar="sparkles",
        )

    async def reflect_and_learn(
        self,
        iteration: int,
        critic_findings: Dict[str, Any],
        sandbox_metrics: Dict[str, Any],
        vault: DynamicKnowledgeVault,
    ) -> HeuristicRule:
        prompt = (
            f"Analyze the failures from Iteration {iteration}:\n"
            f"Critic Flaws: {json.dumps(critic_findings.get('flaws_detected', []))}\n"
            f"Critical Anti-Pattern: {critic_findings.get('critical_anti_pattern')}\n"
            f"Sandbox Failures: {json.dumps(sandbox_metrics.get('failure_logs', []))}\n\n"
            f"Synthesize ONE high-impact heuristic rule in JSON format:\n"
            f"{{\n"
            f'  "category": "Algorithmic Complexity / Defensive Boundary / Type Safety",\n'
            f'  "description": "Why this rule is essential",\n'
            f'  "anti_pattern": "What mistake was made",\n'
            f'  "recommended_solution": "The exact best practice to mandate",\n'
            f'  "impact_score": 18.5\n'
            f"}}"
        )
        raw_res = await self.call_llm(prompt)
        try:
            cleaned = (
                raw_res.strip()
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )
            data = json.loads(cleaned)
            rule = vault.add_rule(
                category=data.get("category", "Defensive Optimization"),
                description=data.get(
                    "description", "Heuristic derived from failure analysis"
                ),
                anti_pattern=data.get(
                    "anti_pattern", "Unbounded or unverified operations"
                ),
                recommended_solution=data.get(
                    "recommended_solution", "Strict defensive guard pattern"
                ),
                iteration=iteration,
                impact_score=float(data.get("impact_score", 15.0)),
            )
            return rule
        except Exception:
            return self.fallback_rule_generation(iteration, vault)

    def get_fallback_response(self, prompt: str) -> str:
        return "Reflection completed."

    def fallback_rule_generation(
        self, iteration: int, vault: DynamicKnowledgeVault
    ) -> HeuristicRule:
        if iteration == 1:
            return vault.add_rule(
                category="Asymptotic Efficiency & Guards",
                description="Nested linear searches cause O(N^2) latency explosion under high-volume streaming inputs.",
                anti_pattern="Nested scanning loops without indexed hash lookups and missing dictionary key existence checks.",
                recommended_solution="Pre-index incoming streams into a hashmap/defaultdict(float) in O(N) time and defensively validate key existence.",
                iteration=iteration,
                impact_score=28.5,
            )
        else:
            return vault.add_rule(
                category="Strict Type Coercion & Schema Defense",
                description="Direct float() or int() conversion raises unhandled ValueError on dirty or corrupt telemetry feeds.",
                anti_pattern="Assuming clean numeric types without safe exception containment or fallback defaults.",
                recommended_solution="Implement defensive try/except parsing or regex number validation with explicit fallback to 0.0.",
                iteration=iteration,
                impact_score=14.0,
            )
