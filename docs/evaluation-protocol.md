# Evaluation and accounting protocol

Version: 0.1, 2026-10-29. Status: design contract; no benchmark has run.

## 1. Unit of work and acceptance

A task is a fixed problem at a fixed repository/environment snapshot. A trial is one scheduled execution of one system on one task, with its own declared budget. Retries, reviews, escalations, and repairs inside that execution are part of the same trial. They must not become extra independent successes.

Acceptance is determined outside the agent's editable workspace. Use executable checks for observable behavior and a documented review rubric when tests cannot capture a requirement. An LLM's approval alone is insufficient for a deterministic NixOS behavior that can be tested. A trial with a critical regression cannot be accepted.

Before using a task, show that its broken starting state fails the intended check, its reference solution passes, and at least one plausible inadequate patch is rejected. Preserve grader identities and hashes. Agent-visible development checks may help iteration; evaluator-only final checks must not be exposed through the agent's tools or retrieval sources.

## 2. Comparisons

Start with four arms:

| Arm | Policy | Question |
| --- | --- | --- |
| F | Frontier model alone | What does the strong baseline actually achieve? |
| O | Open-weight model alone | How much work needs frontier help at all? |
| C | Open-weight attempt, then rule-based frontier escalation | Does a cheap-first cascade suffice? |
| D | Frontier planning and integration with open-weight workers | Does explicit delegation justify its overhead? |

Use the same task inputs, repository snapshots, tool access, retrieval rules, acceptance procedure, and declared resource ceilings. Policy-specific prompts are part of the intervention and must be recorded. Tune each arm fairly on development tasks, then freeze it.

Prefer an existing harness that can express all four arms. Where different harnesses are necessary, label the result as a whole-system comparison; do not attribute its difference solely to orchestration. A later frontier-with-frontier-workers arm can isolate the value of decomposition from the effect of cheaper workers.

Compare quality/cost curves across sensible budgets after the first pilot. Equal token counts are not inherently equal cost or equal opportunity across models.

## 3. Primary outcomes

For a complete scheduled cohort:

```
success_rate = accepted_trials / scheduled_trials
cost_per_accepted_trial = total_cost_of_all_scheduled_trials / accepted_trials
```

The numerator includes failed work. If no trial is accepted, report no finite observed cost per success; do not report zero. If a cost or scheduled trial is missing, withhold the ratio and expose the known subtotal and coverage. With repetitions, call the unit an accepted trial; also report results per unique task and do not imply that repeats are new task types.

Report alongside the primary figures:

- Success and critical failures by task family.
- Median and tail wall time, not just aggregate time saved.
- Human intervention and review minutes, including unsuccessful work.
- Frontier calls/tokens, worker calls/tokens, escalation rate, and review/repair cost.
- Provider errors, timeouts, refusals, malformed tool calls, and infrastructure failures.
- Trace and cost coverage, and all exclusions or reruns.

Classify a provider refusal as a task failure with a reason in the trace; classify transient endpoint failure as infrastructure error. Retain the cost in either case. Report deployment yield including infrastructure failures; an additional agent-only diagnostic may exclude independently verified infrastructure faults if the exclusion rule was fixed in advance and the complete ledger remains visible.

## 4. Cost ledgers

Keep distinct accounting bases. Never switch bases silently between systems.

| Basis | Include | Required explanation |
| --- | --- | --- |
| Marginal cash | Actual paid inference/tool charges, incremental measured local energy, and other incremental execution charges. | Tariff, metering boundary, currency, and billing records or rates. |
| API equivalent | A stated API price applied to a matching model's measured usage. | Exact price snapshot and exclusions; this is not subscription spend. |
| Fully loaded | Marginal costs plus declared allocations for hardware/infrastructure and, if chosen, human labor. | Amortization/utilization assumptions and whether labor is monetized. |

For local quantized models with no matching metered endpoint, an API-equivalent figure may be undefined. Do not price them as a different full-precision cloud model. Measure local costs under the other bases instead.

Record subscription allowance consumption separately when it can be observed. If its relationship to tokens is unknown, say unknown. Allocating a monthly fee is a stated management assumption, not a measurement of per-task quota use. A lower API-equivalent cost does not prove a lower subscription allowance charge.

Track cached, uncached, cache-write, reasoning, and output usage according to each provider's billing semantics, avoiding double counting reasoning already included in output. Include supervisor, worker, judge, compaction, approval, retry, recovery, and verifier calls. Publish temporary credits and discounts separately from the undiscounted comparison.

Local inference is not costless simply because no invoice arrives per request. Record energy, runtime, concurrency, and hardware configuration. Report amortization separately from incremental energy so owners of existing hardware can make their own decision. Disclose whether idle power is included and how shared-machine energy is allocated.

Use one currency per comparison with a dated conversion rule for any foreign-currency input. Preserve original bill currency and rate evidence in the trace bundle. The small v0.1 reporter reads whole-trial totals; it does not perform billing reconciliation or currency conversion.

## 5. Frozen identity and provenance

Every measured experiment needs a companion configuration bundle containing:

- Task roster, task and verifier revisions, starting repository commits, and retrieval policy.
- Model provider, requested and observed served identifiers, checkpoint revision, and dates.
- For local models: artifact hash, quantization, context/KV settings, inference-runtime commit, expert-routing or other approximate optimizations, and hardware.
- Harness commit, system prompts, model-role mappings, tool contracts, generation parameters, context management, and policy budgets.
- Nixpkgs/flake lock, host architecture, virtualization support, binary-cache policy, and cold/warm state.
- Price snapshots, cost basis, exchange rates, energy measurement method, and any subsidy.
- Command/patch/tool traces, final artifacts, acceptance outputs, exclusions, and content hashes.

Pin approximate inference settings separately from orchestration. Changing quantization or expert routing at the same time changes the system being evaluated. A similarly named cloud model is not a substitute for the tested local artifact.

Explicitly verify that each model role reaches the intended served model; some bridges fall back when an alias is unrecognized. Inspect's current bridge behavior is documented in the [source review](research/2026-10-29-foundations.md).

Do not promise identical stochastic outputs on rerun. Reproducibility means another person can reconstruct the experiment and assess whether the result persists within its uncertainty and declared environmental differences.

## 6. Development, confirmation, and uncertainty

Use development tasks to repair the runner, tune prompts, estimate costs, and discover failure modes. Do not publish those tuning scores as held-out evidence.

Before a confirmatory run, freeze the policy, roster, budgets, acceptance rules, primary outcome, exclusions, noninferiority margin, and stopping rule. Use fresh held-out task families/instances with meaningful separation from development material. After publication a public task set is a replication set, not a permanently uncontaminated holdout.

Pair systems on the same tasks and randomize or interleave execution order. Keep warm-cache advantages and provider load from systematically favoring an arm. Repetitions are clustered within tasks: uncertainty estimates must resample/analyze tasks rather than treating every repeat as an unrelated problem.

For a claimed preservation of quality, use a predeclared noninferiority test. A nonsignificant difference is not proof of equivalence. The allowable absolute loss must be explicit and appropriate to the task risk. Select confirmatory sample size from pilot disagreement/variance estimates and the required power; a small pilot will usually be inconclusive for a narrow margin.

Never infer zero severe-regression risk from observing none. Report the count, exposure, and an uncertainty bound when estimating risk. Keep critical requirements as separate gates instead of allowing easy tasks to average them away.

## 7. Verification tiers and limits

NixOS tasks can have several acceptance layers: syntax/evaluation, build, VM boot, service behavior, and specified cross-machine behavior. Passing a build is not evidence for all later layers. The official [NixOS VM testing guide](https://nix.dev/tutorials/nixos/integration-testing-using-virtual-machines.html) provides declarative QEMU-based testing primitives.

Begin with tasks that these environments can reproduce. Device-specific suspend, GPU, firmware, audio hardware, and power-management behavior require a later hardware track and explicit machine manifests. Do not use production-host deployment as the initial benchmark runner.

## 8. Publication gate

A result is ready when the roster is accounted for, acceptance evidence is independently inspectable, costs reconcile, privacy/provenance checks are complete, and the write-up states its scope and uncertainty. A colleague should be able to reproduce one trial from a fresh checkout before a recipe is promoted.

Publish unsuccessful experiments too. Do not select the best seed or omit expensive failures. Keep model preferences or commercial affiliations separate from empirical outcomes.
