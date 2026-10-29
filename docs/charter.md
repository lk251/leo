# Leo project charter

Date: 2026-10-29. Status: initial design; hypotheses remain untested.

## Purpose

Find, test, and publish model-orchestration policies that improve the cost of accepted engineering work. Start with a narrow NixOS workload and open-weight workers, then expand only when the evidence and contributor capacity justify it.

The central question is conditional: on which tasks, with which verification, budgets, and model versions, does the policy help? A recipe that saves money on module migrations may fail on architecture or diagnosis. Publish those limits with the result.

## Expected value

The work should produce several useful outcomes from the same experiments:

1. Better inference allocation for real engineering work.
2. Practical learning in evaluation, orchestration, instrumentation, and error analysis.
3. Reusable tasks, acceptance tests, and recipes for contributors.
4. A public body of evidence that earns trust and attracts technically relevant collaborators.

Audience growth is a possible consequence, not a demonstrated result or a reason to cherry-pick findings. A failed orchestration is publishable when its evidence and diagnosis are useful.

## Initial research hypothesis

A sufficiently capable open-weight worker, combined with selective frontier planning or escalation and independent verification, may reduce cost per accepted NixOS task relative to a well-configured frontier-only agent.

The alternative is equally important: planning, handoff, context replay, review, and repair can erase the worker's savings. Cheap-first escalation may beat a permanent frontier supervisor. A single strong agent may still be best for difficult or poorly verifiable work.

## What Leo contains

- Versioned orchestration recipes and their execution contracts.
- Public or purpose-built task packs with independent acceptance criteria.
- Experiment manifests, complete trial ledgers, traces, and failure analyses.
- Comparisons against strong single-agent baselines.
- Replication instructions and external replication reports.
- Small adapters and accounting tools that existing frameworks do not provide.

## Boundaries

An internal evaluation and decision system has a different owner-facing purpose: decide what model, provider, harness, or workflow to use for a particular private workload. It can consume Leo's recipe format and evidence while keeping its task sets, weights, diagnostics, and operational history private.

An autonomous research application gathers and synthesizes information. It can use a Leo policy and be evaluated by the internal system. It does not need to share Leo's repository or release schedule.

The shared interface is a versioned experiment record and recipe contract. Repository separation should not require duplicated evaluation infrastructure.

## Vocabulary

| Term | Meaning in Leo |
| --- | --- |
| Model routing | Select a model for a request or stage. |
| Cascade | Try a cheaper path, then escalate under an explicit rule. |
| Delegation | Give a worker a bounded subtask and integrate the result. |
| Orchestration | Manage decomposition, routing, dependencies, context, tools, verification, and stopping. |
| Ensemble or critique | Generate or assess multiple candidates, then select or combine them. |
| Harness | The tools, context handling, execution loop, permissions, and stopping behavior around models. |
| Evaluation | Measure behavior against a defined task and acceptance procedure. |
| Benchmark | A versioned task collection and scoring protocol for comparisons. |
| Error analysis | Explain failures and identify whether the model, tools, context, policy, verifier, or environment caused them. |
| Ablation | Remove or change one component to test its contribution. |
| Regression testing | Check whether a change damages previously working behavior. |
| Pareto comparison | Compare quality, cost, and time without pretending they reduce to one universal intelligence score. |

## First success criteria

The first milestone succeeds when another person can reproduce one task's environment and verifier, inspect every model/tool call, reconcile cost totals, and rerun the same policy. This milestone does not require the mixed-model policy to win.

A later effectiveness claim requires fresh held-out tasks, a predeclared quality tolerance, complete cost data, uncertainty estimates, and disclosure of critical failures. A public claim must name the workload and exact systems tested.

## Publication and community

Publish one useful experiment at a time: question, frozen recipe, comparator, quality and cost results, important failures, and reproduction artifacts. A short social post should link to the evidence rather than carry the whole argument.

Start collaboration with task contributions, verifier review, and independent replications. Contributors can run an assigned experiment locally and contribute evidence. A centrally managed pool of borrowed machines is a later project, justified only if compute availability becomes the limiting factor.

Evaluate community progress by successful replications, useful contributions, and adoption in real workflows as well as reach. Keep experiments small enough that the research overhead does not consume the work the savings were meant to enable.
