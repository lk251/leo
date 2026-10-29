# Implementation roadmap

## Foundation delivered

- Project charter and separation from internal workload evaluation.
- Evaluation/cost protocol and a four-arm NixOS pilot design.
- Review of current evidence and reusable frameworks.
- Expected-roster manifest, whole-trial ledger, and dependency-free reporter.
- Focused accounting tests and clearly synthetic example data.

## Next: one end-to-end task

1. Compare Inspect AI and Harbor against the exact chosen harness and NixOS VM requirements. Prefer one; document the decision and pinned version.
2. Create one public fixture, reference patch, immutable acceptance checks, and Nixpkgs lock. Verify the intended broken/passing outcomes.
3. Add a runner adapter and event ledger, with explicit model-role mapping and observed served identifiers.
4. Reconcile model, tool, local-resource, and verifier costs into the whole-trial recording contract.
5. Execute the small four-arm wiring experiment under a declared budget and publish its limitations.

## Then: useful evidence

Expand the development task set, diagnose failures, freeze a candidate, size and run a fresh holdout, and obtain independent replication. Package a successful policy as a runnable recipe, or publish why it failed.

## Deferred until justified

- Learned routers or automated policy search.
- Broad comparisons across many models and quantizations.
- Production deployment automation and hardware-specific tasks.
- Centralized community compute scheduling.
- Dashboards, leaderboards, and scheduled public reports.
- A custom general-purpose orchestration runtime.
- Study [DeepLearning.AI](https://www.deeplearning.ai/courses) courses on agentic systems, multi-agent orchestration, and evaluation. Suggested progression: [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai) (planning, reflection, tool use, multi-agent patterns), [Multi AI Agent Systems with crewAI](https://www.deeplearning.ai/courses/multi-ai-agent-systems-with-crewai) and [AI Agents in LangGraph](https://www.deeplearning.ai/courses/ai-agents-in-langgraph) (orchestration patterns), then [Evaluating AI Agents](https://www.deeplearning.ai/courses/evaluating-ai-agents) and [Building and Evaluating Data Agents](https://www.deeplearning.ai/courses/building-and-evaluating-data-agents) (tracing, evaluation, error analysis). Review [Orchestrating Workflows for GenAI Applications](https://www.deeplearning.ai/courses/orchestrating-workflows-for-genai-applications) selectively: it focuses on Airflow pipelines rather than adaptive model delegation. Capture practical lessons and experiment ideas, not an automatic dependency commitment.

The work should first prove one complete, honest experiment and one useful recipe. Expand according to measured bottlenecks.
