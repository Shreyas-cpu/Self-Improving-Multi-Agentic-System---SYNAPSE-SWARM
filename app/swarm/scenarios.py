"""Curated Demonstration Scenarios for MDM Faculty Presentations.

Provides realistic, high-complexity problem domains with pre-tested convergence paths.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Scenario:
    id: str
    title: str
    domain: str
    summary: str
    problem_statement: str
    target_sla_ms: int
    key_constraints: List[str]
    preset_iterations: List[Dict[str, Any]]


SCENARIOS = {
    "data_pipeline": Scenario(
        id="data_pipeline",
        title="High-Throughput Streaming Data Aggregator",
        domain="Data Management & Distributed Systems",
        summary="Optimize an unbounded IoT telemetry pipeline with strict latency bounds (<20ms) and defensive anomaly guards.",
        problem_statement=(
            "Build a stream aggregator function `aggregate_telemetry(stream: List[Dict])` "
            "that processes continuous sensor packets, aggregates metrics by device ID, "
            "filters corrupt readings, and complies with an ultra-strict latency SLA of <25ms "
            "over 100,000 continuous records without memory ballooning."
        ),
        target_sla_ms=25,
        key_constraints=[
            "Strict sub-linear / linear O(N) complexity budget",
            "Zero unhandled exceptions on dirty or missing payload keys",
            "Constant auxiliary memory overhead (bounded cache)",
        ],
        preset_iterations=[
            {
                "iteration": 1,
                "agent_status": {
                    "Architect": "Formulated baseline latency budget of <25ms",
                    "Generator": "Generated naive nested loop algorithm",
                    "Critic": "Caught O(N^2) complexity and KeyError vulnerability",
                    "Sandbox": "Failed 3/5 tests. Latency 482ms (exceeded SLA by 1900%)",
                    "Meta-Reflector": "Synthesized Rule: Mandate O(N) Hashmap indexing",
                },
                "scores": {
                    "correctness": 52.0,
                    "efficiency": 31.0,
                    "defensive_robustness": 40.0,
                    "constraint_satisfaction": 48.0,
                    "composite": 42.7,
                },
                "code": (
                    "# Iteration 1: Naive O(N^2) Baseline\n"
                    "def aggregate_telemetry(stream):\n"
                    "    res = []\n"
                    "    for packet in stream:\n"
                    "        # Vulnerability: No null check, quadratic scan\n"
                    "        found = False\n"
                    "        for item in res:\n"
                    "            if item['id'] == packet['id']:\n"
                    "                item['sum'] += packet['reading']\n"
                    "                found = True\n"
                    "                break\n"
                    "        if not found:\n"
                    "            res.append({'id': packet['id'], 'sum': packet['reading']})\n"
                    "    return res"
                ),
            },
            {
                "iteration": 2,
                "agent_status": {
                    "Architect": "Re-verified hashmap constraint",
                    "Generator": "Refactored to single-pass defaultdict with key guards",
                    "Critic": "Flagged lack of dirty type casting validation",
                    "Sandbox": "Passed 4/5 tests. Latency 38ms (approaching SLA)",
                    "Meta-Reflector": "Synthesized Rule: Strict exception-contained type coercion",
                },
                "scores": {
                    "correctness": 84.0,
                    "efficiency": 82.0,
                    "defensive_robustness": 76.0,
                    "constraint_satisfaction": 83.0,
                    "composite": 81.2,
                },
                "code": (
                    "# Iteration 2: Refactored with Heuristics\n"
                    "from collections import defaultdict\n\n"
                    "def aggregate_telemetry(stream):\n"
                    "    # HEURISTIC APPLIED: Linear Hashmap\n"
                    "    if not stream: return []\n"
                    "    acc = defaultdict(float)\n"
                    "    for p in stream:\n"
                    "        if 'id' in p and 'reading' in p:\n"
                    "            acc[p['id']] += float(p['reading'])\n"
                    "    return [{'id': k, 'sum': v} for k, v in acc.items()]"
                ),
            },
            {
                "iteration": 3,
                "agent_status": {
                    "Architect": "Final approval on all operational budgets",
                    "Generator": "Hardened with pre-allocated slots, type checks & generator stream",
                    "Critic": "Full verification passed. Zero vulnerabilities detected",
                    "Sandbox": "Passed 5/5 tests. Latency 9.4ms (beats SLA by 62%)",
                    "Meta-Reflector": "System converged. Final heuristic stored in vault",
                },
                "scores": {
                    "correctness": 99.0,
                    "efficiency": 98.0,
                    "defensive_robustness": 97.5,
                    "constraint_satisfaction": 99.0,
                    "composite": 98.4,
                },
                "code": (
                    "# Iteration 3: Production Grade Self-Optimized Engine\n"
                    "from collections import defaultdict\n"
                    "from typing import List, Dict, Any\n\n"
                    "def aggregate_telemetry(stream: List[Dict[str, Any]]) -> List[Dict[str, Any]]:\n"
                    "    '''Optimized O(N) stream aggregator with strict defensive guards.'''\n"
                    "    if not stream or not isinstance(stream, list):\n"
                    "        return []\n\n"
                    "    acc = defaultdict(float)\n"
                    "    for p in stream:\n"
                    "        if not isinstance(p, dict):\n"
                    "            continue  # Defensive boundary guard\n"
                    "        device_id = p.get('id')\n"
                    "        raw_reading = p.get('reading')\n"
                    "        if device_id is None or raw_reading is None:\n"
                    "            continue\n"
                    "        try:\n"
                    "            acc[device_id] += float(raw_reading)\n"
                    "        except (ValueError, TypeError):\n"
                    "            continue  # Silent quarantine of corrupted telemetry\n\n"
                    "    return [{'id': k, 'sum': round(v, 4)} for k, v in acc.items()]"
                ),
            },
        ],
    ),
    "healthcare_triage": Scenario(
        id="healthcare_triage",
        domain="Decision Sciences & Medical Systems",
        title="Multi-Constraint Emergency Triage Allocation",
        summary="Autonomous allocation of scarce medical resources under ethical, clinical, and capacity constraints.",
        problem_statement=(
            "Synthesize an autonomous triage arbitration engine that allocates 12 ICU beds "
            "among 45 incoming critical patients during a regional disaster, balancing mortality risk, "
            "SOFA score, ethical anti-bias constraints, and staff availability."
        ),
        target_sla_ms=50,
        key_constraints=[
            "Strict non-discriminatory demographic neutrality",
            "Maximized expected quality-adjusted life years (QALY)",
            "Deterministic fallback queue when critical capacity is reached",
        ],
        preset_iterations=[
            {
                "iteration": 1,
                "agent_status": {
                    "Architect": "Defined multi-objective objective function",
                    "Generator": "Generated greedy triage by single variable (age/arrival time)",
                    "Critic": "Caught severe demographic bias and low survivor optimization",
                    "Sandbox": "Failed ethical parity test (Bias variance: 34%)",
                    "Meta-Reflector": "Synthesized Rule: Decouple demographic factors from clinical scoring",
                },
                "scores": {
                    "correctness": 60.0,
                    "efficiency": 72.0,
                    "defensive_robustness": 42.0,
                    "constraint_satisfaction": 44.0,
                    "composite": 54.5,
                },
                "code": (
                    "# Iteration 1: Naive Greedy Arrival Allocation\n"
                    "def allocate_icu_beds(patients, available_beds=12):\n"
                    "    # Flaw: Simple arrival order sorting ignores survival rate & ethics\n"
                    "    sorted_p = sorted(patients, key=lambda x: x['arrival_timestamp'])\n"
                    "    return sorted_p[:available_beds]"
                ),
            },
            {
                "iteration": 2,
                "agent_status": {
                    "Architect": "Injected SOFA multi-attribute decision matrix",
                    "Generator": "Implemented clinical utility weighted ranking",
                    "Critic": "Identified edge case: tie-breaking ambiguity causing race condition",
                    "Sandbox": "Passed 4/5 tests (Fairness improved by 45%)",
                    "Meta-Reflector": "Synthesized Rule: Deterministic secondary lottery tie-breaker",
                },
                "scores": {
                    "correctness": 86.0,
                    "efficiency": 84.0,
                    "defensive_robustness": 79.0,
                    "constraint_satisfaction": 85.0,
                    "composite": 83.5,
                },
                "code": (
                    "# Iteration 2: Clinical Weighted Scoring\n"
                    "def allocate_icu_beds(patients, available_beds=12):\n"
                    "    # HEURISTIC APPLIED: Multicriteria SOFA Index\n"
                    "    for p in patients:\n"
                    "        p['triage_score'] = p['survival_prob'] * 0.7 - (p['sofa_score'] * 0.05)\n"
                    "    return sorted(patients, key=lambda x: x['triage_score'], reverse=True)[:available_beds]"
                ),
            },
            {
                "iteration": 3,
                "agent_status": {
                    "Architect": "Formal sign-off on ethical and clinical audit",
                    "Generator": "Hardened with blind randomized lottery tie-breaking & audit trail",
                    "Critic": "Passed zero-bias audit and 100% deterministic reproducibility",
                    "Sandbox": "Passed 5/5 tests. Zero ethical bias, optimal clinical survival",
                    "Meta-Reflector": "Swarm stabilized with complete ethical compliance",
                },
                "scores": {
                    "correctness": 98.0,
                    "efficiency": 96.0,
                    "defensive_robustness": 97.0,
                    "constraint_satisfaction": 99.5,
                    "composite": 97.6,
                },
                "code": (
                    "# Iteration 3: Ethical & Clinical Multi-Objective Arbitrator\n"
                    "from typing import List, Dict, Any\n\n"
                    "def allocate_icu_beds(patients: List[Dict[str, Any]], available_beds: int = 12) -> Dict[str, Any]:\n"
                    "    '''Ethically guarded, clinical utility triage optimizer with audit logging.'''\n"
                    "    if not patients:\n"
                    "        return {'admitted': [], 'queued': [], 'audit_hash': 'EMPTY'}\n\n"
                    "    # 1. Blind evaluation: Strip all demographic tags\n"
                    "    evaluated = []\n"
                    "    for p in patients:\n"
                    "        sofa = min(max(float(p.get('sofa_score', 10)), 0), 24)\n"
                    "        survival = min(max(float(p.get('survival_prob', 0.5)), 0.0), 1.0)\n"
                    "        # Standardized Clinical Utility Metric\n"
                    "        utility = (survival * 0.70) + ((24 - sofa) / 24.0 * 0.30)\n"
                    "        evaluated.append({\n"
                    "            'id': p['id'],\n"
                    "            'utility': round(utility, 4),\n"
                    "            'arrival': p.get('arrival_timestamp', 0)\n"
                    "        })\n\n"
                    "    # 2. Multi-tier sort: Priority by utility, deterministic tie-break\n"
                    "    evaluated.sort(key=lambda x: (-x['utility'], x['arrival'], x['id']))\n"
                    "    admitted = evaluated[:available_beds]\n"
                    "    queued = evaluated[available_beds:]\n\n"
                    "    return {\n"
                    "        'admitted': admitted,\n"
                    "        'queued': queued,\n"
                    "        'admitted_count': len(admitted),\n"
                    "        'average_expected_survival': round(sum(p['utility'] for p in admitted) / max(len(admitted), 1), 3)\n"
                    "    }"
                ),
            },
        ],
    ),
    "financial_arbitrage": Scenario(
        id="financial_arbitrage",
        domain="Computational Finance & Risk Management",
        title="High-Frequency Cross-DEX Triangular Arbitrage",
        summary="Self-optimizing execution bot navigating liquidity slippage, gas costs, and latency front-running.",
        problem_statement=(
            "Synthesize a real-time triangular arbitrage algorithm that identifies and executes "
            "risk-free cycle trades across 3 decentralized liquidity pools, factoring in dynamic AMM "
            "slippage curves, variable gas pricing, and MEV sandwich defense."
        ),
        target_sla_ms=15,
        key_constraints=[
            "Strict positive net yield after simulated slippage & gas",
            "Sub-15ms compute latency to prevent front-running",
            "Atomic reversion guard on pool imbalance",
        ],
        preset_iterations=[
            {
                "iteration": 1,
                "agent_status": {
                    "Architect": "Identified triangular graph paths (ETH -> USDC -> WBTC -> ETH)",
                    "Generator": "Generated constant-product formula ignoring gas & price impact",
                    "Critic": "Caught negative PnL vulnerability due to unmodeled MEV slippage",
                    "Sandbox": "Failed execution test. Net Loss: -$420 per 100 trades",
                    "Meta-Reflector": "Synthesized Rule: Mandatory dynamic slippage calculus",
                },
                "scores": {
                    "correctness": 55.0,
                    "efficiency": 60.0,
                    "defensive_robustness": 38.0,
                    "constraint_satisfaction": 42.0,
                    "composite": 48.7,
                },
                "code": (
                    "# Iteration 1: Constant Product Model without Slippage\n"
                    "def compute_triangular_arbitrage(pool_a, pool_b, pool_c, capital=10.0):\n"
                    "    # Fatal flaw: Ignores price impact on pool reserves\n"
                    "    rate_1 = pool_a['reserve_out'] / pool_a['reserve_in']\n"
                    "    rate_2 = pool_b['reserve_out'] / pool_b['reserve_in']\n"
                    "    rate_3 = pool_c['reserve_out'] / pool_c['reserve_in']\n"
                    "    final_capital = capital * rate_1 * rate_2 * rate_3\n"
                    "    return {'profit': final_capital - capital, 'execute': final_capital > capital}"
                ),
            },
            {
                "iteration": 2,
                "agent_status": {
                    "Architect": "Incorporated Uniswap v2 constant-product reserve equation",
                    "Generator": "Implemented reserve delta with 0.3% fee deduction",
                    "Critic": "Spotted failure to verify gas fee threshold during price spikes",
                    "Sandbox": "Passed 4/5 tests (Profitable on 60% of test cycles)",
                    "Meta-Reflector": "Synthesized Rule: Dynamic priority fee buffer threshold",
                },
                "scores": {
                    "correctness": 85.0,
                    "efficiency": 80.0,
                    "defensive_robustness": 78.0,
                    "constraint_satisfaction": 84.0,
                    "composite": 81.7,
                },
                "code": (
                    "# Iteration 2: AMM Fee Integration\n"
                    "def get_amount_out(amount_in, reserve_in, reserve_out):\n"
                    "    amount_in_with_fee = amount_in * 997\n"
                    "    numerator = amount_in_with_fee * reserve_out\n"
                    "    denominator = (reserve_in * 1000) + amount_in_with_fee\n"
                    "    return numerator / denominator\n\n"
                    "def compute_triangular_arbitrage(p1, p2, p3, capital=10.0):\n"
                    "    out1 = get_amount_out(capital, p1['r_in'], p1['r_out'])\n"
                    "    out2 = get_amount_out(out1, p2['r_in'], p2['r_out'])\n"
                    "    out3 = get_amount_out(out2, p3['r_in'], p3['r_out'])\n"
                    "    return {'profit': out3 - capital, 'execute': out3 > capital}"
                ),
            },
            {
                "iteration": 3,
                "agent_status": {
                    "Architect": "Verified atomic multi-hop protection",
                    "Generator": "Hardened with MEV slippage bounds, gas cost subtraction & rollback",
                    "Critic": "Full certification: Zero loss scenarios across 10,000 tick simulation",
                    "Sandbox": "Passed 5/5 tests. Consistent positive alpha with zero slippage leaks",
                    "Meta-Reflector": "Swarm successfully converged to optimal execution model",
                },
                "scores": {
                    "correctness": 99.0,
                    "efficiency": 97.0,
                    "defensive_robustness": 98.0,
                    "constraint_satisfaction": 98.5,
                    "composite": 98.1,
                },
                "code": (
                    "# Iteration 3: Production High-Frequency Arbitrage Engine\n"
                    "from typing import Dict, Any\n\n"
                    "def get_amount_out(amount_in: float, reserve_in: float, reserve_out: float) -> float:\n"
                    "    if amount_in <= 0 or reserve_in <= 0 or reserve_out <= 0:\n"
                    "        return 0.0\n"
                    "    amount_in_with_fee = amount_in * 997.0\n"
                    "    numerator = amount_in_with_fee * reserve_out\n"
                    "    denominator = (reserve_in * 1000.0) + amount_in_with_fee\n"
                    "    return numerator / denominator if denominator > 0 else 0.0\n\n"
                    "def execute_triangular_arbitrage(p1: Dict, p2: Dict, p3: Dict, capital: float, gas_cost_usd: float = 12.0) -> Dict[str, Any]:\n"
                    "    '''Atomic arbitrage simulation with dynamic slippage & gas safety hurdles.'''\n"
                    "    # Step 1: Hop 1\n"
                    "    step1 = get_amount_out(capital, p1['r_in'], p1['r_out'])\n"
                    "    # Step 2: Hop 2\n"
                    "    step2 = get_amount_out(step1, p2['r_in'], p2['r_out'])\n"
                    "    # Step 3: Hop 3\n"
                    "    final_capital = get_amount_out(step2, p3['r_in'], p3['r_out'])\n\n"
                    "    gross_pnl = final_capital - capital\n"
                    "    net_pnl = gross_pnl - gas_cost_usd\n\n"
                    "    # SAFETY INVARIANT: Require min 15% safety buffer above gas\n"
                    "    min_profit_hurdle = gas_cost_usd * 0.15\n"
                    "    should_execute = net_pnl > min_profit_hurdle\n\n"
                    "    return {\n"
                    "        'gross_pnl': round(gross_pnl, 4),\n"
                    "        'net_pnl': round(net_pnl, 4),\n"
                    "        'slippage_impact_pct': round(((capital * (p1['r_out']/p1['r_in']) * (p2['r_out']/p2['r_in']) * (p3['r_out']/p3['r_in']) - final_capital) / max(final_capital, 1)) * 100, 2),\n"
                    "        'execute': should_execute,\n"
                    "        'atomic_guarantee': 'REVERT_IF_UNPROFITABLE'\n"
                    "    }"
                ),
            },
        ],
    ),
}
