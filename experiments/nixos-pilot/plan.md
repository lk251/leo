# NixOS pilot: selective frontier assistance

Status: **design only**. No task fixtures, pinned model configuration, budget, or real run has been created. This document is not a claim of preregistered confirmatory results.

## Question

Can open-weight local workers with selective frontier assistance reduce cost per accepted NixOS engineering trial while preserving a declared level of correctness and keeping critical regressions visible?

## Initial task design

Create 12 development tasks: two in each family below. Use purpose-built public fixtures with explicit provenance. These are candidate task specifications, not an existing benchmark.

| Family | Example requirement | Acceptance evidence |
| --- | --- | --- |
| Module-option migration | Repair an obsolete or incorrect option while retaining required behavior. | Evaluation plus relevant VM behavior. |
| Service configuration | Enable a service with a stated account, directory, and startup behavior. | Boot and service assertions. |
| Packaging/build repair | Repair a small derivation under pinned dependencies. | Build and an executable smoke check. |
| Home Manager change | Change a user configuration while preserving declared generated files or behavior. | Evaluation/build and targeted behavioral checks. |
| Integration diagnosis | Fix one fault in a two-node service/network scenario. | Positive and negative connectivity assertions. |
| Module refactor | Remove duplication while maintaining behavior across two configurations. | Both configurations evaluate/build; relevant runtime tests pass. |

Validate broken and reference states before model use. Keep final graders outside the editable agent checkout. Avoid tasks whose solution is already available through the permitted retrieval path. Record dependencies and whether external documentation is available.

## Four arms

1. **Frontier only:** the selected Astra checkpoint/configuration in one agent harness.
2. **Open-weight only:** one exact local model artifact and quantization in that harness.
3. **Cheap-first cascade:** the local model attempts the task; a fixed visible check or stop condition escalates to the frontier model; the final hidden acceptance procedure is unchanged.
4. **Frontier-supervised workers:** frontier planning creates bounded work; a local worker produces a patch and evidence; frontier integration/review uses a bounded budget; independent verification determines the final outcome.

Use one worker candidate for the first experiment. Testing multiple models, quantizations, runtimes, prompt families, and policies at once would obscure the first answer and multiply cost. Candidate model labels must be replaced by exact provider/artifact identities before any measured run.

For the cascade, declare whether escalation continues from the patch or starts from a clean snapshot. For delegation, define what context crosses the handoff, how conflicts are resolved, and which evidence the reviewer sees. Do not treat a prose worker summary as proof that tests passed.

## Stages

### A. No-inference preflight

Implement one fixture and its reference patch. Run its verifier against the broken state, reference state, and a plausible inadequate patch. Check that the runner exports the full expected roster and that cost totals can be traced back to events. Prove model-role resolution with a controlled integration check before the full pilot.

### B. Small wiring run

Execute one task across the four arms under an explicit experiment spend and wall-time limit. Stop to fix instrumentation if served model identities, acceptance evidence, or cost coverage are missing. This run is development evidence.

### C. Development pilot

Run the 12-task roster across the four arms: 48 scheduled trials for one repetition. Add repetitions only to resolve observed instability and keep those choices visible. Account for all tuning, diagnostics, and reruns as experiment development expenditure, even though they are not included in the frozen candidate's task-efficiency metric.

Estimate success, disagreement patterns, cost, time, and review overhead. Inspect failures before choosing the policy for confirmation. If the supervisor costs more than it saves, test the simpler cascade before expanding the architecture.

### D. Frozen confirmation

Build a separate fresh holdout, predeclare a tolerable absolute quality loss and confidence procedure, and determine the required task count using pilot estimates. The intended quality loss should be narrow enough to support the actual claim; an exploratory example of a two-percentage-point margin is not an assertion that the pilot can establish it.

Freeze model identities, policies, grader, prices, budgets, and holdout roster before results are visible. Report uncertainty and task-family differences. If evidence is insufficient, publish an inconclusive result.

### E. Independent replication and recipe

Have a contributor rerun a small fixed subset with their own environment manifest and then replicate the complete experiment if practical. Explain environmental differences. Publish the tested recipe and useful negative results.

## Experiment record before launch

The recording manifest must be accompanied by the exact configurations and cost evidence described in the [protocol](../../docs/evaluation-protocol.md). The following remain intentionally unresolved until the execution environment is inspected:

- Selected harness and tested adapter compatibility.
- Exact frontier model access and billing basis.
- Local checkpoint, quantization, runtime, and inference optimizations.
- Task-fixture revisions and Nixpkgs lock.
- Explicit total spend, per-trial limits, concurrency, and stopping rules.
- Energy metering and subscription-usage visibility.

No background schedule or autonomous paid run is part of this foundation commit.
