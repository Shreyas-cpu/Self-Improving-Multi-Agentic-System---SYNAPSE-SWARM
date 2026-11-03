"""Swarm Orchestrator for SYNAPSE-SWARM.

Coordinates agent lifecycles, manages iterative self-improvement loops,
and streams fine-grained real-time events to the frontend dashboard.
"""

import asyncio
from dataclasses import asdict
import json
import logging
from typing import Any, AsyncGenerator, Dict, List, Optional

from app.agents import (
    ArchitectAgent,
    CriticAgent,
    GeneratorAgent,
    MetaReflectorAgent,
    SandboxAgent,
)
from app.memory.vault import DynamicKnowledgeVault
from app.swarm.scenarios import SCENARIOS, Scenario

logger = logging.getLogger("synapse.orchestrator")


class SwarmOrchestrator:

    def __init__(self):
        self.architect = ArchitectAgent()
        self.generator = GeneratorAgent()
        self.critic = CriticAgent()
        self.sandbox = SandboxAgent()
        self.reflector = MetaReflectorAgent()
        self.vault = DynamicKnowledgeVault()
        self.current_scenario: Optional[Scenario] = None

    async def run_iteration_loop(
        self,
        scenario_id: str = "data_pipeline",
        custom_prompt: Optional[str] = None,
        mode: str = "accelerated",  # 'accelerated' or 'live'
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Main generator that executes the self-improvement loop and streams SSE events."""
        self.vault.clear()

        scenario = SCENARIOS.get(scenario_id)
        if not scenario:
            scenario = SCENARIOS["data_pipeline"]
        self.current_scenario = scenario

        problem_text = custom_prompt if custom_prompt else scenario.problem_statement

        # Initial event: Swarm initialized
        yield {
            "type": "init",
            "scenario": {
                "id": scenario.id,
                "title": scenario.title,
                "domain": scenario.domain,
                "problem": problem_text,
                "sla_target_ms": scenario.target_sla_ms,
            },
            "timestamp": "now",
        }
        await asyncio.sleep(0.3 if mode == "accelerated" else 0.8)

        # Step 1: Architect Planning Phase
        yield {
            "type": "agent_status",
            "agent": "Architect",
            "state": "ACTIVE",
            "message": "Analyzing constraints, performance budgets, and edge invariants...",
        }
        await asyncio.sleep(0.4 if mode == "accelerated" else 1.2)

        if mode == "live":
            architecture = await self.architect.plan(
                problem_text, domain=scenario.domain
            )
        else:
            architecture = self.architect.get_fallback_data(problem_text)

        yield {
            "type": "architect_plan",
            "agent": "Architect",
            "data": architecture,
        }
        yield {
            "type": "agent_status",
            "agent": "Architect",
            "state": "IDLE",
            "message": "Decomposition complete.",
        }
        await asyncio.sleep(0.3 if mode == "accelerated" else 0.6)

        prior_feedback = None
        prior_solution = None

        # Execute 3 Iterations of Self-Improvement
        for iteration in range(1, 4):
            yield {
                "type": "iteration_start",
                "iteration": iteration,
                "message": f"Commencing Iteration {iteration}/3 of Self-Improvement Loop",
            }

            # -------------------------------------------------------------
            # Stage A: Generator Agent synthesizes candidate solution
            # -------------------------------------------------------------
            yield {
                "type": "agent_status",
                "agent": "Generator",
                "state": "ACTIVE",
                "message": (
                    "Synthesizing baseline implementation..."
                    if iteration == 1
                    else "Synthesizing refactored solution with learned heuristics..."
                ),
            }
            await asyncio.sleep(0.5 if mode == "accelerated" else 1.5)

            if mode == "live":
                gen_result = await self.generator.generate_solution(
                    problem=problem_text,
                    architecture=architecture,
                    iteration=iteration,
                    learned_rules_prompt=self.vault.get_rules_as_prompt(),
                    prior_feedback=prior_feedback,
                    prior_solution=prior_solution,
                )
                candidate_code = gen_result["code"]
            else:
                # Use crafted preset iteration progression
                preset_it = scenario.preset_iterations[iteration - 1]
                candidate_code = preset_it["code"]

            prior_solution = candidate_code

            yield {
                "type": "solution_generated",
                "iteration": iteration,
                "code": candidate_code,
                "active_rules_count": len(self.vault.rules),
            }
            yield {
                "type": "agent_status",
                "agent": "Generator",
                "state": "IDLE",
                "message": "Solution generated.",
            }
            await asyncio.sleep(0.3 if mode == "accelerated" else 0.8)

            # -------------------------------------------------------------
            # Stage B: Critic / Auditor Agent audits solution
            # -------------------------------------------------------------
            yield {
                "type": "agent_status",
                "agent": "Critic",
                "state": "ACTIVE",
                "message": "Subjecting code to adversarial audit and constraint scoring...",
            }
            await asyncio.sleep(0.5 if mode == "accelerated" else 1.4)

            if mode == "live":
                audit_res = await self.critic.audit(
                    candidate_code=candidate_code,
                    architecture=architecture,
                    iteration=iteration,
                    active_rules_count=len(self.vault.rules),
                )
            else:
                preset_it = scenario.preset_iterations[iteration - 1]
                audit_res = {
                    "correctness": preset_it["scores"]["correctness"],
                    "efficiency": preset_it["scores"]["efficiency"],
                    "defensive_robustness": preset_it["scores"][
                        "defensive_robustness"
                    ],
                    "constraint_satisfaction": preset_it["scores"][
                        "constraint_satisfaction"
                    ],
                    "composite_score": preset_it["scores"]["composite"],
                    "verdict": (
                        "FAIL"
                        if iteration == 1
                        else ("PARTIAL" if iteration == 2 else "PASS")
                    ),
                    "flaws_detected": (
                        [
                            "Asymptotic O(N^2) quadratic nested loop",
                            "Missing defensive check for dirty keys",
                        ]
                        if iteration == 1
                        else (
                            ["Minor type casting risk on non-numeric strings"]
                            if iteration == 2
                            else []
                        )
                    ),
                    "critical_anti_pattern": (
                        "Unbounded nested scanning loop without indexing"
                        if iteration == 1
                        else (
                            "Unsafe direct numeric type cast"
                            if iteration == 2
                            else "Zero flaws detected. Production ready."
                        )
                    ),
                }

            prior_feedback = json.dumps(audit_res)

            yield {
                "type": "critic_audit",
                "iteration": iteration,
                "audit": audit_res,
            }
            yield {
                "type": "agent_status",
                "agent": "Critic",
                "state": "IDLE",
                "message": f"Audit complete. Score: {audit_res['composite_score']}%",
            }
            await asyncio.sleep(0.3 if mode == "accelerated" else 0.8)

            # -------------------------------------------------------------
            # Stage C: Sandbox Agent executes benchmark stress tests
            # -------------------------------------------------------------
            yield {
                "type": "agent_status",
                "agent": "Sandbox",
                "state": "ACTIVE",
                "message": "Running test suite, measuring latency and memory footprint...",
            }
            await asyncio.sleep(0.4 if mode == "accelerated" else 1.2)

            sandbox_res = await self.sandbox.execute_and_benchmark(
                candidate_code, iteration
            )

            yield {
                "type": "sandbox_result",
                "iteration": iteration,
                "sandbox": sandbox_res,
            }
            yield {
                "type": "agent_status",
                "agent": "Sandbox",
                "state": "IDLE",
                "message": f"Passed {sandbox_res['tests_passed']}/{sandbox_res['tests_total']} tests ({sandbox_res['execution_time_ms']}ms)",
            }
            await asyncio.sleep(0.3 if mode == "accelerated" else 0.8)

            # -------------------------------------------------------------
            # Stage D: Meta-Reflector Agent extracts heuristic rules (if not converged)
            # -------------------------------------------------------------
            if iteration < 3:
                yield {
                    "type": "agent_status",
                    "agent": "Meta-Reflector",
                    "state": "ACTIVE",
                    "message": "Performing causal failure analysis and synthesizing immutable rules...",
                }
                await asyncio.sleep(0.5 if mode == "accelerated" else 1.6)

                if mode == "live":
                    new_rule = await self.reflector.reflect_and_learn(
                        iteration=iteration,
                        critic_findings=audit_res,
                        sandbox_metrics=sandbox_res,
                        vault=self.vault,
                    )
                else:
                    new_rule = self.reflector.fallback_rule_generation(
                        iteration, self.vault
                    )

                yield {
                    "type": "rule_synthesized",
                    "iteration": iteration,
                    "rule": asdict(new_rule),
                    "vault_stats": self.vault.to_dict(),
                }
                yield {
                    "type": "agent_status",
                    "agent": "Meta-Reflector",
                    "state": "IDLE",
                    "message": f"Synthesized [{new_rule.rule_id}]: {new_rule.category}",
                }
                await asyncio.sleep(0.4 if mode == "accelerated" else 1.0)

            # Log this iteration in Vault
            self.vault.log_iteration(
                iteration=iteration,
                score=audit_res["composite_score"],
                metrics={
                    "correctness": audit_res["correctness"],
                    "efficiency": audit_res["efficiency"],
                    "defensive_robustness": audit_res["defensive_robustness"],
                    "constraint_satisfaction": audit_res[
                        "constraint_satisfaction"
                    ],
                    "latency_ms": sandbox_res["execution_time_ms"],
                    "pass_rate": sandbox_res["pass_rate"],
                },
                summary=f"Iteration {iteration}: Score {audit_res['composite_score']}%",
                candidate_code=candidate_code,
            )

        # -------------------------------------------------------------
        # Convergence Complete: Broadcast final summary and diff
        # -------------------------------------------------------------
        first_it_code = self.vault.evolution_history[0]["candidate_code"]
        final_it_code = self.vault.evolution_history[-1]["candidate_code"]
        initial_score = self.vault.evolution_history[0]["score"]
        final_score = self.vault.evolution_history[-1]["score"]

        yield {
            "type": "swarm_converged",
            "scenario_id": scenario.id,
            "convergence_summary": {
                "initial_score": initial_score,
                "final_score": final_score,
                "score_gain": round(final_score - initial_score, 1),
                "total_rules_learned": len(self.vault.rules),
                "latency_reduction_pct": round(
                    (
                        (
                            self.vault.evolution_history[0]["metrics"][
                                "latency_ms"
                            ]
                            - self.vault.evolution_history[-1]["metrics"][
                                "latency_ms"
                            ]
                        )
                        / max(
                            self.vault.evolution_history[0]["metrics"][
                                "latency_ms"
                            ],
                            1,
                        )
                    )
                    * 100,
                    1,
                ),
            },
            "comparison": {
                "baseline_code": first_it_code,
                "final_code": final_it_code,
            },
            "vault": self.vault.to_dict(),
        }
