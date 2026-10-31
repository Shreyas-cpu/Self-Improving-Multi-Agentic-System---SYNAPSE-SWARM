# Requirements: SYNAPSE-SWARM

## Functional Requirements
- **FR-1**: Multi-Agent Swarm execution supporting 5 distinct agent personas (`Architect`, `Generator`, `Critic`, `Sandbox`, `Meta-Reflector`).
- **FR-2**: Iterative self-improvement feedback loop where failure analysis generates heuristics that update prompts and memory dynamically.
- **FR-3**: Real-time event streaming via Server-Sent Events (SSE) or WebSockets to broadcast agent thoughts, state transitions, and metrics.
- **FR-4**: Interactive web dashboard with:
  - Animated Node Graph / Agent Topology.
  - Multi-iteration progress timeline with live score gauges.
  - Side-by-side comparative diff viewer (Iteration 1 vs 3).
  - Dynamic radar metrics chart (Accuracy, Speed, Safety, Cost, Constraint Satisfaction).
  - Live Evolving Knowledge Vault displaying extracted heuristic rules.
  - 1-Click Faculty Demo Presets with dual execution modes (Instant Accelerated Playback & Live Gemini API streaming).
- **FR-5**: Academic Project Report generator that produces publication-grade markdown and printable HTML/PDF report.

## Non-Functional Requirements
- **NFR-1**: High responsiveness (< 50ms UI update latency via SSE).
- **NFR-2**: Zero external frontend build tool friction (self-contained, standalone dashboard with zero bundle compile lag).
- **NFR-3**: Fault tolerance: System must never freeze or crash during a live faculty demonstration, even if network disconnects.
