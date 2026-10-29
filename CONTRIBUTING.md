# Contributing

Useful contributions include task fixtures, stronger acceptance tests, careful failure analysis, independent replications, and cheaper or more reliable recipes.

## Task contribution

Provide a public or purpose-built starting repository, an exact revision, a clear request, redistribution terms, a reference solution, and acceptance checks. Demonstrate that the broken state fails, the reference state passes, and a plausible incomplete solution fails. Explain which real workload the task represents.

Do not contribute private configurations, personal data, credentials, or unapproved third-party material. Keep final evaluators outside the agent's editable task workspace. Publicly released tasks are suitable for replication; later confirmation requires fresh tasks.

## Recipe or result contribution

Include the system and model identities, prompts, tools, handoffs, stopping rules, full trial roster, trace evidence, and all costs and outcomes. State your hardware and local inference settings. Report failures and missing measurements explicitly. Separate measured, estimated, and synthetic values.

Use the [evaluation protocol](docs/evaluation-protocol.md) and [ledger contract](docs/ledger.md). Make no equality or savings claim from an incomplete cohort or a small inconclusive pilot.

## Independent replication

Begin with an agreed fixed subset and run it on infrastructure you control. Preserve the experiment revision and disclose differences in hardware, providers, caching, model versions, or price assumptions. Contributing logs does not require giving others access to your machine or inference credentials.

Inspect traces before sharing; protect private data without silently removing scientific evidence. Document necessary redactions and their effect on reproducibility. An experiment that cannot be disclosed can remain internal rather than being presented as publicly reproducible.

## Development

```bash
python3 -B -m unittest discover -s tests -v
```

Changes to accounting should include a regression check for a concrete risk, such as omitted failures, incomplete costs, duplicate trials, or contradictory acceptance records.
