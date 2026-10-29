# Initial evidence and reusable foundations

Research date: 2026-10-29. This is an initial source review, not a systematic literature review or a Leo benchmark result. Availability and managed-model policies can change.

## Trigger and retrieval limits

The [linked X post](https://x.com/sabaka_339/status/2115599094194598309) asks for practitioners who measure orchestration errors and euros per successfully completed task. Its text was recovered using X's public oEmbed endpoint. The reply list was not retrievable in this research pass. The Copilot claim below was checked independently; other recommendations must not be attributed to unseen replies.

## Copilot Fusion: what the evidence establishes

Artificial Analysis's current [direct comparison](https://artificialanalysis.ai/agents/coding-agents/comparisons/claude-code-vs-github-copilot) reports:

| Measure | Copilot CLI: Fusion Max | Claude Code: Opus 5.5 Max, default fallback |
| --- | ---: | ---: |
| Coding Agent Index v2.0 | 60 | 62 |
| FrontierCode v1.1 | 51% | 56% |
| Terminal-Bench 4.0 | 71% | 63% |
| SWE-Atlas-QnA-AA | 57% | 66% |
| Average API cost per task | USD 5.59 | USD 11.42 |
| Average task time | 36.1 minutes | 1.0 hour |

The observed cost reduction is approximately 51%. This is a promising whole-system comparison. The different component scores do not demonstrate uniform quality preservation, and the changing harness/model mix prevents attributing the entire difference to orchestration alone.

The [AA methodology](https://artificialanalysis.ai/methodology/coding-agents-benchmarking) distinguishes an equal-weight benchmark index from pooled per-attempt cost. FrontierCode also uses graded scores. Consequently, dividing 5.59 by 0.60 would not recover verified cost per successful task. AA's costs use API pricing, not consumer subscription consumption. Leo needs the actual accepted-trial denominator and complete cost coverage.

GitHub's [launch announcement](https://github.blog/changelog/2026-10-28-route-and-orchestrate-models-with-github-copilot-fusion/) describes single-model execution, a draft-and-escalate cascade, and critique/revision. These are useful experimental patterns. They need independent ablations on Leo's workload.

GitHub's [Fusion documentation](https://docs.github.com/en/enterprise-cloud%40latest/copilot/concepts/models/copilot-fusion) describes local Qwen3.8 Flash Next eligibility in Fusion Standard through Copilot CLI on Linux, macOS, and Windows, identified as `qwen3.8-flash-next-local`. This preview does not establish that the evaluated Fusion Max used open/local models. Fusion also operates separately from subagents. Its model pool is managed and can change.

The [CLI model-provider documentation](https://docs.github.com/en/enterprise-cloud%40latest/copilot/how-tos/copilot-cli/customize-copilot/add-llm-models) describes local/Ollama and manually configured providers. Having a custom endpoint in a client is distinct from being eligible for automatic Fusion routing. The exact local runtime configuration must be tested; no Leo compatibility is established by these documents.

**Decision:** keep Fusion as a potentially useful external comparator. Do not describe its full policy as a verified open-source implementation or assume its results transfer to a different local quantization.

## Reuse candidates

These are roles and recommendations, not dependencies already installed in Leo.

| Candidate | Evidence and role | Initial decision |
| --- | --- | --- |
| [Inspect AI](https://inspect.aisi.org.uk/) | Evaluation components, scorers, agents, model/tool logging; [agent bridge](https://inspect.aisi.org.uk/agent-bridge.html) for existing harnesses. | Preferred candidate for a small adapter feasibility check. |
| [Harbor](https://github.com/harbor-framework/harbor) | Agent-evaluation framework from the Terminal-Bench creators, with task environments and verifiers. | Alternative to Inspect; verify NixOS/KVM needs before choosing. |
| [RouteLLM](https://github.com/lm-sys/RouteLLM) | Research-backed serving/evaluation of learned strong/weak-model routers, including local-model paths. | Useful routing baseline after the simple policies work; not a task-delegation runtime. |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful orchestration and persistent execution. | Add only if the existing harness cannot express the needed policy. |
| [LiteLLM](https://github.com/BerriAI/litellm) | Provider compatibility, fallbacks, and usage/cost integrations. | Optional adapter; its API cost records do not establish local energy or subscription quota cost. |

Do not assemble all five frameworks before running a useful experiment. The first candidate stack is one existing agent harness, one experiment layer, a NixOS acceptance adapter, and the small accounting contract.

Inspect's [multi-agent methodology](https://inspect.aisi.org.uk/multi-agent.html) recommends a simple agent baseline and warns that multi-agent systems often fail to improve on it. That supports testing a cheap-first cascade and a well-tuned single agent before assuming a supervisor-worker design wins.

The current [Inspect bridge documentation](https://inspect.aisi.org.uk/agent-bridge.html) says unmatched sandbox model names fall back to the evaluation model. Explicitly map each supervisor/worker alias and verify served identities. Generation settings also require inspection. This is a concrete way an intended heterogeneous experiment could accidentally measure a different system.

Inspect can publish a [bundled log viewer](https://inspect.aisi.org.uk/log-viewer.html). If chosen, this could provide inspectable traces behind short social posts without first building a dashboard. Redaction and provenance review would still be necessary.

## Why start with NixOS

The official [NixOS VM testing guide](https://nix.dev/tutorials/nixos/integration-testing-using-virtual-machines.html) provides declarative machines and Python assertions over QEMU. Leo can use these primitives to test services and multi-machine behavior under pinned inputs.

The proposed advantage is methodological: useful tasks can have executable acceptance evidence. A build pass alone does not establish service behavior, and generic VMs cannot reproduce every firmware or device issue. Start with reproducible module, package, and service tasks; add a separately characterized hardware track later.

## Questions left open

- Which existing harness can support the four experimental arms faithfully on the available model endpoints?
- Is Inspect or Harbor the simpler fit for NixOS execution and model-role telemetry?
- How much verification and frontier review is needed before local work can be accepted?
- Do cascades outperform an always-present frontier supervisor on the chosen task distribution?
- Which errors survive tests, and how much human review remains?
- What is the real local energy cost, and what subscription consumption can actually be observed?

Answer these experimentally. The sources establish useful components and precedent; they do not establish Leo's quality or savings.
