"""Dynamic Knowledge Vault (Heuristic Memory Store).

Stores learned rules, anti-patterns, and reflection synthesis across swarm iterations.
Provides live inspection and dynamic context injection for subsequent generations.
"""

from dataclasses import asdict, dataclass, field
import datetime
from typing import Any, Dict, List


@dataclass
class HeuristicRule:
    rule_id: str
    iteration_discovered: int
    category: str  # e.g., "Edge-Case Guard", "Algorithmic Complexity", "Constraint Safety"
    description: str
    anti_pattern: str
    recommended_solution: str
    impact_score: float  # Expected score boost (e.g., +15.5)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


class DynamicKnowledgeVault:

    def __init__(self):
        self.rules: List[HeuristicRule] = []
        self.evolution_history: List[Dict[str, Any]] = []

    def clear(self):
        self.rules.clear()
        self.evolution_history.clear()

    def add_rule(
        self,
        category: str,
        description: str,
        anti_pattern: str,
        recommended_solution: str,
        iteration: int,
        impact_score: float = 10.0,
    ) -> HeuristicRule:
        rule_id = f"RULE-{len(self.rules) + 1:03d}"
        rule = HeuristicRule(
            rule_id=rule_id,
            iteration_discovered=iteration,
            category=category,
            description=description,
            anti_pattern=anti_pattern,
            recommended_solution=recommended_solution,
            impact_score=impact_score,
        )
        self.rules.append(rule)
        return rule

    def get_rules_as_prompt(self) -> str:
        if not self.rules:
            return "No prior learned rules in vault. Proceed with first-principles generation."

        lines = [
            "### LEARNED KNOWLEDGE VAULT (Mandatory Heuristics from Prior Iterations):"
        ]
        for r in self.rules:
            lines.append(
                f"- [{r.rule_id}] [{r.category}] NEVER DO: {r.anti_pattern} | INSTEAD: {r.recommended_solution} (Reason: {r.description})"
            )
        return "\n".join(lines)

    def log_iteration(
        self,
        iteration: int,
        score: float,
        metrics: Dict[str, float],
        summary: str,
        candidate_code: str,
    ):
        self.evolution_history.append(
            {
                "iteration": iteration,
                "score": score,
                "metrics": metrics,
                "summary": summary,
                "candidate_code": candidate_code,
                "rules_active": len(self.rules),
                "timestamp": datetime.datetime.now().isoformat(),
            }
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_rules": len(self.rules),
            "rules": [asdict(r) for r in self.rules],
            "evolution_history": self.evolution_history,
        }
