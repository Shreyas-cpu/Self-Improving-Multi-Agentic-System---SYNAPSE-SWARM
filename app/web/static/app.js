/**
 * SYNAPSE-SWARM Interactive Front-End Controller
 * Manages Canvas agent topology animation, Chart.js radar, SSE streaming,
 * dynamic code diffs, and knowledge vault inspection.
 */

// Global State
let currentMode = "accelerated";
let currentScenario = "data_pipeline";
let eventSource = null;
let radarChart = null;
let iterationCodes = { it1: "", it2: "", it3: "" };
let initialScore = 0;
let currentTab = "it1";
let reportMarkdown = "";

// Agent definitions for Topology Canvas
const AGENTS = {
  Architect: { x: 120, y: 115, color: "#6366f1", label: "Architect", role: "Planner", state: "IDLE", pulse: 0 },
  Generator: { x: 300, y: 65,  color: "#10b981", label: "Generator", role: "Synthesizer", state: "IDLE", pulse: 0 },
  Critic:    { x: 480, y: 65,  color: "#ef4444", label: "Critic", role: "Auditor", state: "IDLE", pulse: 0 },
  Sandbox:   { x: 480, y: 165, color: "#f59e0b", label: "Sandbox", role: "Benchmark", state: "IDLE", pulse: 0 },
  "Meta-Reflector": { x: 300, y: 165, color: "#a855f7", label: "Meta-Reflector", role: "Learner", state: "IDLE", pulse: 0 }
};

const CONNECTIONS = [
  ["Architect", "Generator"],
  ["Generator", "Critic"],
  ["Generator", "Sandbox"],
  ["Critic", "Meta-Reflector"],
  ["Sandbox", "Meta-Reflector"],
  ["Meta-Reflector", "Generator"]
];

let particles = [];

// Initialize Dashboard
document.addEventListener("DOMContentLoaded", () => {
  initRadarChart();
  initCanvas();
  setupScenarioListener();
});

// Mode Toggle
function setMode(mode) {
  currentMode = mode;
  document.getElementById("modeAccel").classList.toggle("active", mode === "accelerated");
  document.getElementById("modeLive").classList.toggle("active", mode === "live");
  logMessage("SYSTEM", `Execution mode switched to: ${mode.toUpperCase()}`);
}

function setupScenarioListener() {
  const select = document.getElementById("scenarioSelect");
  select.addEventListener("change", (e) => {
    currentScenario = e.target.value;
    logMessage("SYSTEM", `Scenario selected: ${select.options[select.selectedIndex].text}`);
    resetMetrics();
  });
}

function resetMetrics() {
  document.getElementById("metricScore").innerText = "0.0%";
  document.getElementById("metricGain").innerText = "+0.0% gain";
  document.getElementById("metricLatency").innerText = "-- ms";
  document.getElementById("metricPassRate").innerText = "0 / 5";
  document.getElementById("metricPassPct").innerText = "0%";
  document.getElementById("metricRulesCount").innerText = "0";
  document.getElementById("vaultBadge").innerText = "0 RULES STORED";
  document.getElementById("vaultList").innerHTML = `
    <div style="color: var(--text-muted); font-size: 0.8rem; text-align: center; padding: 2rem 0;">
      No heuristics stored yet. As agents reflect on failures, distilled rules will appear here in real-time.
    </div>
  `;
  iterationCodes = { it1: "", it2: "", it3: "" };
  resetRadar();
}

// -----------------------------------------------------------------------------
// Canvas Topology Visualizer & Animation Loop
// -----------------------------------------------------------------------------
function initCanvas() {
  const canvas = document.getElementById("topologyCanvas");
  const ctx = canvas.getContext("2d");

  function resize() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = 230;

    // Responsive scaling of agent coordinates
    const w = canvas.width;
    AGENTS.Architect.x = w * 0.15;
    AGENTS.Generator.x = w * 0.40;
    AGENTS.Critic.x = w * 0.82;
    AGENTS.Sandbox.x = w * 0.82;
    AGENTS["Meta-Reflector"].x = w * 0.40;
  }
  window.addEventListener("resize", resize);
  resize();

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Draw Connection Lines
    CONNECTIONS.forEach(([fromKey, toKey]) => {
      const from = AGENTS[fromKey];
      const to = AGENTS[toKey];
      ctx.beginPath();
      ctx.moveTo(from.x, from.y);
      ctx.lineTo(to.x, to.y);
      ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
      ctx.lineWidth = 2;
      ctx.stroke();
    });

    // 2. Animate and Draw Flow Particles
    particles = particles.filter(p => p.progress < 1.0);
    particles.forEach(p => {
      p.progress += 0.02;
      const x = p.from.x + (p.to.x - p.from.x) * p.progress;
      const y = p.from.y + (p.to.y - p.from.y) * p.progress;
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.shadowColor = p.color;
      ctx.shadowBlur = 10;
      ctx.fill();
      ctx.shadowBlur = 0;
    });

    // 3. Draw Agent Nodes
    Object.keys(AGENTS).forEach(key => {
      const agent = AGENTS[key];
      const isActive = agent.state === "ACTIVE";

      // Pulsing effect
      if (isActive) {
        agent.pulse += 0.08;
        const pulseRadius = 26 + Math.sin(agent.pulse) * 6;
        ctx.beginPath();
        ctx.arc(agent.x, agent.y, pulseRadius, 0, Math.PI * 2);
        ctx.fillStyle = agent.color + "33"; // 20% opacity
        ctx.fill();
      }

      // Outer Ring
      ctx.beginPath();
      ctx.arc(agent.x, agent.y, 22, 0, Math.PI * 2);
      ctx.fillStyle = "#0f172a";
      ctx.strokeStyle = isActive ? agent.color : "rgba(255, 255, 255, 0.2)";
      ctx.lineWidth = isActive ? 3 : 1.5;
      if (isActive) {
        ctx.shadowColor = agent.color;
        ctx.shadowBlur = 16;
      }
      ctx.fill();
      ctx.stroke();
      ctx.shadowBlur = 0;

      // Inner Core
      ctx.beginPath();
      ctx.arc(agent.x, agent.y, 9, 0, Math.PI * 2);
      ctx.fillStyle = agent.color;
      ctx.fill();

      // Labels
      ctx.font = "bold 11px Inter, sans-serif";
      ctx.fillStyle = isActive ? "#fff" : "#94a3b8";
      ctx.textAlign = "center";
      ctx.fillText(agent.label, agent.x, agent.y - 28);

      ctx.font = "9px JetBrains Mono, monospace";
      ctx.fillStyle = isActive ? agent.color : "#64748b";
      ctx.fillText(`[${agent.state}]`, agent.x, agent.y + 36);
    });

    requestAnimationFrame(animate);
  }

  animate();
}

function spawnParticle(fromKey, toKey, color) {
  const from = AGENTS[fromKey];
  const to = AGENTS[toKey];
  if (from && to) {
    particles.push({ from, to, color: color || from.color, progress: 0 });
  }
}

// -----------------------------------------------------------------------------
// Radar Chart (Chart.js)
// -----------------------------------------------------------------------------
function initRadarChart() {
  const ctx = document.getElementById("radarChart").getContext("2d");
  radarChart = new Chart(ctx, {
    type: "radar",
    data: {
      labels: ["Correctness", "Efficiency", "Robustness", "Constraint Sat."],
      datasets: [
        {
          label: "Iteration 1 (Baseline)",
          data: [0, 0, 0, 0],
          borderColor: "rgba(239, 68, 68, 0.7)",
          backgroundColor: "rgba(239, 68, 68, 0.15)",
          pointBackgroundColor: "#ef4444",
          borderWidth: 1.5
        },
        {
          label: "Iteration 2 (Refined)",
          data: [0, 0, 0, 0],
          borderColor: "rgba(245, 158, 11, 0.8)",
          backgroundColor: "rgba(245, 158, 11, 0.15)",
          pointBackgroundColor: "#f59e0b",
          borderWidth: 1.5
        },
        {
          label: "Iteration 3 (Optimized)",
          data: [0, 0, 0, 0],
          borderColor: "rgba(16, 185, 129, 1)",
          backgroundColor: "rgba(16, 185, 129, 0.25)",
          pointBackgroundColor: "#10b981",
          borderWidth: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 0,
          max: 100,
          ticks: { display: false, stepSize: 25 },
          grid: { color: "rgba(255, 255, 255, 0.07)" },
          angleLines: { color: "rgba(255, 255, 255, 0.1)" },
          pointLabels: {
            color: "#94a3b8",
            font: { size: 10, family: "Inter, sans-serif" }
          }
        }
      },
      plugins: {
        legend: {
          position: "bottom",
          labels: { boxWidth: 10, font: { size: 10 }, color: "#cbd5e1" }
        }
      }
    }
  });
}

function updateRadar(iteration, scores) {
  if (!radarChart) return;
  const idx = iteration - 1;
  if (radarChart.data.datasets[idx]) {
    radarChart.data.datasets[idx].data = [
      scores.correctness,
      scores.efficiency,
      scores.defensive_robustness,
      scores.constraint_satisfaction
    ];
    radarChart.update();
  }
}

function resetRadar() {
  if (!radarChart) return;
  radarChart.data.datasets.forEach(ds => ds.data = [0, 0, 0, 0]);
  radarChart.update();
}

// -----------------------------------------------------------------------------
// SSE Swarm Stream Execution
// -----------------------------------------------------------------------------
function startSwarm() {
  const runBtn = document.getElementById("runBtn");
  runBtn.disabled = true;
  document.getElementById("swarmStateBadge").innerText = "SWARM ACTIVE";
  document.getElementById("swarmStateBadge").style.color = "var(--accent-emerald)";
  resetMetrics();

  const url = `/api/stream?scenario_id=${currentScenario}&mode=${currentMode}`;
  if (eventSource) {
    eventSource.close();
  }

  eventSource = new EventSource(url);

  eventSource.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data);
      handleSwarmEvent(data);
    } catch (err) {
      console.error("Error parsing SSE event:", err);
    }
  };

  eventSource.onerror = (err) => {
    console.error("SSE Error:", err);
    eventSource.close();
    runBtn.disabled = false;
    document.getElementById("swarmStateBadge").innerText = "COMPLETED";
    document.getElementById("swarmStateBadge").style.color = "var(--accent-cyan)";
    logMessage("SYSTEM", "Swarm execution sequence completed.");
  };
}

function handleSwarmEvent(event) {
  switch (event.type) {
    case "init":
      logMessage("SYSTEM", `Initialized Swarm for scenario: ${event.scenario.title}`);
      logMessage("SYSTEM", `Domain: ${event.scenario.domain} | Target SLA: <${event.scenario.sla_target_ms}ms`);
      break;

    case "agent_status":
      if (AGENTS[event.agent]) {
        AGENTS[event.agent].state = event.state;
      }
      logMessage(event.agent, event.message);

      // Trigger visual particle dispatch
      if (event.state === "ACTIVE") {
        if (event.agent === "Generator") spawnParticle("Architect", "Generator");
        if (event.agent === "Critic") spawnParticle("Generator", "Critic");
        if (event.agent === "Sandbox") spawnParticle("Generator", "Sandbox");
        if (event.agent === "Meta-Reflector") {
          spawnParticle("Critic", "Meta-Reflector");
          spawnParticle("Sandbox", "Meta-Reflector");
        }
      }
      break;

    case "architect_plan":
      logMessage("Architect", `Plan established. Constraints: ${event.data.constraints.length} invariants mapped.`);
      break;

    case "iteration_start":
      logMessage("SYSTEM", `=== STARTING ITERATION ${event.iteration} / 3 ===`);
      break;

    case "solution_generated":
      const itKey = `it${event.iteration}`;
      iterationCodes[itKey] = event.code;
      if (currentTab === itKey) {
        document.getElementById("singleCodeView").innerText = event.code;
      }
      logMessage("Generator", `Candidate synthesized (${event.code.split("\n").length} lines of code).`);
      break;

    case "critic_audit":
      const audit = event.audit;
      const score = audit.composite_score;
      if (event.iteration === 1) initialScore = score;

      document.getElementById("metricScore").innerText = `${score}%`;
      const gain = (score - initialScore).toFixed(1);
      document.getElementById("metricGain").innerText = `${gain >= 0 ? "+" : ""}${gain}% gain`;

      updateRadar(event.iteration, audit);
      logMessage("Critic", `Audit complete. Score: ${score}% | Verdict: ${audit.verdict}`);
      if (audit.critical_anti_pattern && audit.verdict !== "PASS") {
        logMessage("Critic", `Identified Flaw: ${audit.critical_anti_pattern}`);
      }
      break;

    case "sandbox_result":
      const sb = event.sandbox;
      document.getElementById("metricLatency").innerText = `${sb.execution_time_ms} ms`;
      document.getElementById("metricPassRate").innerText = `${sb.tests_passed} / ${sb.tests_total}`;
      document.getElementById("metricPassPct").innerText = `${sb.pass_rate}% pass rate`;
      logMessage("Sandbox", `Execution benchmark: ${sb.tests_passed}/${sb.tests_total} passed in ${sb.execution_time_ms}ms.`);
      break;

    case "rule_synthesized":
      addVaultRuleCard(event.rule);
      const count = document.querySelectorAll(".vault-card").length;
      document.getElementById("metricRulesCount").innerText = count;
      document.getElementById("vaultBadge").innerText = `${count} RULES STORED`;
      spawnParticle("Meta-Reflector", "Generator", "#a855f7");
      logMessage("Meta-Reflector", `[LEARNED HEURISTIC]: ${event.rule.category} -> ${event.rule.recommended_solution}`);
      break;

    case "swarm_converged":
      eventSource.close();
      document.getElementById("runBtn").disabled = false;
      document.getElementById("swarmStateBadge").innerText = "CONVERGED (OPTIMAL)";
      document.getElementById("swarmStateBadge").style.color = "var(--accent-emerald)";
      
      // Update Diff View
      document.getElementById("diffLeft").innerText = event.comparison.baseline_code;
      document.getElementById("diffRight").innerText = event.comparison.final_code;

      logMessage("SYSTEM", `🏆 Swarm successfully converged! Initial: ${event.convergence_summary.initial_score}% -> Final: ${event.convergence_summary.final_score}% (+${event.convergence_summary.score_gain}% gain).`);
      logMessage("SYSTEM", `Execution latency reduced by ${event.convergence_summary.latency_reduction_pct}%. Click 'Project Report' for academic export.`);
      break;
  }
}

// -----------------------------------------------------------------------------
// Terminal Logging Helper
// -----------------------------------------------------------------------------
function logMessage(sender, text) {
  const container = document.getElementById("streamLog");
  const time = new Date().toTimeString().split(" ")[0];

  let badgeColor = "#818cf8";
  let bgBadge = "rgba(99, 102, 241, 0.2)";

  if (sender === "Generator") { badgeColor = "#34d399"; bgBadge = "rgba(16, 185, 129, 0.2)"; }
  else if (sender === "Critic") { badgeColor = "#f87171"; bgBadge = "rgba(239, 68, 68, 0.2)"; }
  else if (sender === "Sandbox") { badgeColor = "#fbbf24"; bgBadge = "rgba(245, 158, 11, 0.2)"; }
  else if (sender === "Meta-Reflector") { badgeColor = "#c084fc"; bgBadge = "rgba(168, 85, 247, 0.2)"; }

  const entry = document.createElement("div");
  entry.className = "log-entry";
  entry.innerHTML = `
    <span class="log-time">${time}</span>
    <span class="log-badge" style="background: ${bgBadge}; color: ${badgeColor};">${sender}</span>
    <span class="log-text">${escapeHtml(text)}</span>
  `;

  container.appendChild(entry);
  container.scrollTop = container.scrollHeight;
}

function escapeHtml(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// -----------------------------------------------------------------------------
// Knowledge Vault Card Builder
// -----------------------------------------------------------------------------
function addVaultRuleCard(rule) {
  const list = document.getElementById("vaultList");
  // Clear placeholder if first rule
  if (list.querySelector("div[style*='text-align: center']")) {
    list.innerHTML = "";
  }

  const card = document.createElement("div");
  card.className = "vault-card";
  card.innerHTML = `
    <div class="vault-card-header">
      <span class="rule-id">[${rule.rule_id}] ${rule.category}</span>
      <span class="rule-impact">+${rule.impact_score} pts</span>
    </div>
    <div class="rule-anti"><strong>Avoid:</strong> ${escapeHtml(rule.anti_pattern)}</div>
    <div class="rule-solution"><strong>Synthesized Heuristic:</strong> ${escapeHtml(rule.recommended_solution)}</div>
  `;
  list.prepend(card);
}

// -----------------------------------------------------------------------------
// Tab Switching
// -----------------------------------------------------------------------------
function switchTab(tab) {
  currentTab = tab;
  const tabs = document.querySelectorAll(".tab-btn");
  tabs.forEach(t => t.classList.remove("active"));

  const singleView = document.getElementById("singleCodeView");
  const diffView = document.getElementById("diffView");

  if (tab === "diff") {
    singleView.style.display = "none";
    diffView.style.display = "grid";
    tabs[3].classList.add("active");
  } else {
    singleView.style.display = "block";
    diffView.style.display = "none";

    if (tab === "it1") {
      tabs[0].classList.add("active");
      singleView.innerText = iterationCodes.it1 || "# Iteration 1 code pending...";
    } else if (tab === "it2") {
      tabs[1].classList.add("active");
      singleView.innerText = iterationCodes.it2 || "# Iteration 2 code pending...";
    } else if (tab === "it3") {
      tabs[2].classList.add("active");
      singleView.innerText = iterationCodes.it3 || "# Iteration 3 code pending...";
    }
  }
}

// -----------------------------------------------------------------------------
// Academic Project Report Modal
// -----------------------------------------------------------------------------
async function openReportModal() {
  const modal = document.getElementById("reportModal");
  const body = document.getElementById("reportBody");
  modal.style.display = "flex";
  body.innerHTML = "<em>Compiling latest empirical metrics into Academic Project Report...</em>";

  try {
    const res = await fetch(`/api/report?scenario_id=${currentScenario}`);
    const data = await res.json();
    reportMarkdown = data.markdown;
    body.innerHTML = formatMarkdownToHtml(data.markdown);
  } catch (err) {
    body.innerHTML = `<span style="color: #ef4444;">Failed to load report: ${err}</span>`;
  }
}

function closeReportModal() {
  document.getElementById("reportModal").style.display = "none";
}

function copyReportMarkdown() {
  navigator.clipboard.writeText(reportMarkdown).then(() => {
    alert("Project Report markdown copied to clipboard!");
  });
}

function printReport() {
  const printWindow = window.open("", "_blank");
  printWindow.document.write(`
    <html>
      <head>
        <title>SYNAPSE-SWARM Academic Project Report</title>
        <style>
          body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 2rem; color: #111; line-height: 1.6; }
          h1, h2, h3 { color: #1e293b; margin-top: 1.5rem; }
          table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 0.9rem; }
          th, td { border: 1px solid #cbd5e1; padding: 0.6rem; text-align: left; }
          th { background: #f1f5f9; }
          code, pre { font-family: monospace; background: #f8fafc; padding: 0.2rem 0.4rem; border-radius: 4px; }
        </style>
      </head>
      <body>
        ${formatMarkdownToHtml(reportMarkdown)}
      </body>
    </html>
  `);
  printWindow.document.close();
  printWindow.focus();
  setTimeout(() => printWindow.print(), 500);
}

function formatMarkdownToHtml(md) {
  let html = md
    .replace(/^# (.*$)/gim, "<h1>$1</h1>")
    .replace(/^## (.*$)/gim, "<h2>$1</h2>")
    .replace(/^### (.*$)/gim, "<h3>$1</h3>")
    .replace(/\*\*(.*?)\*\*/gim, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/gim, "<em>$1</em>")
    .replace(/```([\s\S]*?)```/gim, "<pre><code>$1</code></pre>")
    .replace(/\n\n/gim, "<br><br>")
    .replace(/\|(.+)\|/gim, (match) => {
      const cols = match.split("|").filter(c => c.trim() !== "");
      return "<tr>" + cols.map(c => `<td>${c.trim()}</td>`).join("") + "</tr>";
    });
  return html;
}
