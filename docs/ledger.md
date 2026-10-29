# Trial ledger v0.1

The accounting tool is a small descriptive reporter, not an orchestration runtime, verifier, billing auditor, or statistical inference package.

## Input contract

`schemas/experiment.schema.json` describes the manifest. `schemas/trial.schema.json` describes a JSONL row. The CLI validates the corresponding contract using the Python standard library and enforces cross-record rules that JSON Schema alone does not express.

The manifest names an experiment, task-suite revision, systems, and task/replicate pairs. Its expected roster is the Cartesian product of all systems and all task/replicate pairs. This prevents a missing expensive failure from silently disappearing from a reported cohort.

One JSONL row represents one whole scheduled trial. Aggregate its internal model calls, reviews, retries, recoveries, verification, and failure costs according to the manifest's declared accounting basis. Do not feed both the whole trial and its child calls into this reporter.

`cost`, `wall_seconds`, and `human_minutes` use `null` for unknown values. Zero is a known measured/defined zero. `trace_ref` points to supporting evidence; the tool does not fetch or audit that evidence.

The manifest contains one currency and one cost basis. Use separate manifests/ledgers for different bases, identifying their relationship in the report. Preserve underlying event data to avoid recomputing costs from guessed token counts.

## Output behavior

- Missing scheduled rows are listed and suppress that system's success rate and cost-per-accepted-trial ratio.
- Unknown costs suppress the ratio while preserving the known subtotal and its coverage.
- Costs from failed, timed-out, and infrastructure-error trials remain in the numerator.
- Zero accepted trials produces a `null` ratio with an explicit reason, never zero cost per success.
- An accepted trial cannot have `critical_failure: true`.
- Duplicate or unexpected roster keys, mismatched experiment identifiers, unknown fields, invalid numeric values, and duplicate JSON keys are rejected.
- Synthetic/measured provenance is retained in the output.
- Timing and human effort are descriptive sums/means over known values, accompanied by coverage.

Top-level `complete` means all scheduled trial records are present. Per-system `cost_complete` additionally requires every cost to be known. Neither flag establishes the truth of a supplied acceptance decision or cost.

Repeated executions count as trials. `cost_per_accepted_trial` is deliberately not named cost per unique solved task; this tool does not implement pass@k, task-clustered confidence intervals, or noninferiority analysis. Unequal replication counts can reweight tasks, so confirmatory manifests should use a balanced design or an explicitly defined weighting analysis outside this tool.

## Example and verification

```bash
python3 scripts/summarize.py examples/synthetic/experiment.json examples/synthetic/trials.jsonl
python3 -B -m unittest discover -s tests -v
```

The fictional example is an interface demonstration. It is not a pilot result and must not be used in promotional savings claims.

The companion experiment documentation must supply model/harness/policy identities, prices and conversion rules, trace contents, acceptance criteria, budgets, and task provenance. The schemas intentionally do not pretend that a minimal accounting row captures the entire experiment.
