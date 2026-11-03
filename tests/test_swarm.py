"""Automated Integration & Unit Test Suite for SYNAPSE-SWARM.

Uses standard Python unittest for zero external test harness dependencies.
"""

import asyncio
import unittest
from fastapi.testclient import TestClient
from app.memory.vault import DynamicKnowledgeVault
from app.report.generator import AcademicReportGenerator
from app.swarm.orchestrator import SwarmOrchestrator
from app.swarm.scenarios import SCENARIOS
from app.web.server import app


class TestSynapseSwarm(unittest.TestCase):

    def test_scenarios_loaded(self):
        self.assertIn("data_pipeline", SCENARIOS)
        self.assertIn("healthcare_triage", SCENARIOS)
        self.assertIn("financial_arbitrage", SCENARIOS)

    def test_knowledge_vault_operations(self):
        vault = DynamicKnowledgeVault()
        self.assertEqual(len(vault.rules), 0)

        rule = vault.add_rule(
            category="Algorithmic Complexity",
            description="Prevent O(N^2) loops",
            anti_pattern="Nested scans",
            recommended_solution="Use O(N) hashmap",
            iteration=1,
            impact_score=25.0,
        )
        self.assertEqual(rule.rule_id, "RULE-001")
        self.assertEqual(len(vault.rules), 1)
        self.assertIn("RULE-001", vault.get_rules_as_prompt())

        vault.log_iteration(
            iteration=1,
            score=45.0,
            metrics={"latency_ms": 400.0},
            summary="Baseline run",
            candidate_code="def naive(): pass",
        )
        self.assertEqual(len(vault.evolution_history), 1)
        self.assertEqual(vault.evolution_history[0]["score"], 45.0)

    def test_swarm_orchestrator_loop(self):
        async def run_test():
            orchestrator = SwarmOrchestrator()
            events = []

            async for event in orchestrator.run_iteration_loop(
                scenario_id="data_pipeline", mode="accelerated"
            ):
                events.append(event)

            types = [e["type"] for e in events]
            self.assertIn("init", types)
            self.assertIn("architect_plan", types)
            self.assertIn("solution_generated", types)
            self.assertIn("critic_audit", types)
            self.assertIn("sandbox_result", types)
            self.assertIn("rule_synthesized", types)
            self.assertIn("swarm_converged", types)

            scores = [
                e["audit"]["composite_score"]
                for e in events
                if e["type"] == "critic_audit"
            ]
            self.assertEqual(len(scores), 3)
            self.assertGreater(scores[-1], scores[0])
            self.assertGreaterEqual(scores[-1], 90.0)

        asyncio.run(run_test())

    def test_academic_report_generator(self):
        report_md = AcademicReportGenerator.generate_markdown("data_pipeline")
        self.assertIn("SYNAPSE-SWARM", report_md)
        self.assertIn("Academic Project Report", report_md)
        self.assertIn("Dynamic Knowledge Vault", report_md)
        self.assertIn("Abstract", report_md)

    def test_api_endpoints(self):
        client = TestClient(app)

        res_root = client.get("/")
        self.assertEqual(res_root.status_code, 200)
        self.assertIn("SYNAPSE-SWARM", res_root.text)

        res_scenarios = client.get("/api/scenarios")
        self.assertEqual(res_scenarios.status_code, 200)
        sc_data = res_scenarios.json()
        self.assertEqual(len(sc_data), 3)

        res_report = client.get("/api/report?scenario_id=data_pipeline")
        self.assertEqual(res_report.status_code, 200)
        self.assertIn("markdown", res_report.json())


if __name__ == "__main__":
    unittest.main()
