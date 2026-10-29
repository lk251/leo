# Leo

Reproducible experiments and reusable recipes for cost-effective AI orchestration, starting with NixOS engineering.

Leo asks whether a system of models can complete independently verified work more cheaply without an unacceptable loss of quality. The first focus is frontier models working with open-weight, locally hosted workers. Routing, cascades, and delegation are separate policies to compare.

Named after Leonard Bernstein.

## Status

**Foundation stage, 2026-10-29. No measured orchestration results yet.**

This repository currently contains a project charter, experimental protocol, first NixOS experiment design, source review, and a dependency-free trial-accounting tool. Its example data are synthetic. It does not yet contain a model runner, a NixOS task suite, or implemented model-provider integrations.

The intended deliverable is a collection of useful, reproducible recipes backed by task-level evidence. A recipe includes model identities, prompts, tool permissions, handoff rules, verification, stopping budgets, and a complete cost ledger.

## Start here

- [Project charter and scope](docs/charter.md)
- [Evaluation and accounting protocol](docs/evaluation-protocol.md)
- [First NixOS experiment](experiments/nixos-pilot/plan.md)
- [Copilot Fusion and reusable foundations](docs/research/2026-10-29-foundations.md)
- [Trial ledger and reporting contract](docs/ledger.md)
- [Implementation roadmap](docs/roadmap.md)
- [Contributing and independent replication](CONTRIBUTING.md)

## Run the accounting example

Python 3.10 or later; standard library only:

```bash
python3 scripts/summarize.py examples/synthetic/experiment.json examples/synthetic/trials.jsonl
python3 -B -m unittest discover -s tests -v
```

The example makes no model calls. Its fictional systems deliberately have identical costs. It demonstrates the reporting contract, not an orchestration advantage.

The reporter includes failed-trial costs and refuses to calculate cost per accepted trial when a scheduled record or cost is missing. It also reports critical failures and human-effort coverage. It cannot verify that a supplied cost includes every underlying call; trace reconciliation remains required.

## Project boundaries

Leo develops and publishes orchestration experiments. A separate internal evaluation project can use the same records and recipes to choose systems for private workloads. Autonomous web research is a separate application that may later consume Leo policies. Private tasks, unfinished products, personal machine configurations, and internal traces do not belong in this public repository.

## License

Original code and documentation are available under the [MIT License](LICENSE). Third-party tasks, models, and tools retain their own licenses; each contributed task must identify its provenance and redistribution terms.
