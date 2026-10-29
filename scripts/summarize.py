#!/usr/bin/env python3
"""Validate an experiment ledger and report descriptive trial-level accounting.

No model calls are made. One ledger row represents an entire scheduled trial,
including its child calls, reviews, retries, verification, and failed work.
"""

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path


MANIFEST_FIELDS = {
    "schema_version", "experiment_id", "data_kind", "currency", "cost_basis",
    "task_suite_id", "task_suite_revision", "systems", "trials",
}
TRIAL_FIELDS = {
    "schema_version", "experiment_id", "system_id", "task_id", "replicate",
    "outcome", "cost", "wall_seconds", "human_minutes", "critical_failure",
    "trace_ref",
}
OUTCOMES = ("accepted", "failed", "timeout", "infrastructure_error")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, expected, context):
    require(isinstance(value, dict), f"{context}: expected an object")
    require(set(value) == expected,
            f"{context}: fields must be exactly {', '.join(sorted(expected))}")


def nonempty_string(value, context):
    require(isinstance(value, str) and bool(value.strip()),
            f"{context}: expected a nonempty string")


def trial_key(value, context):
    nonempty_string(value["task_id"], f"{context}.task_id")
    replicate = value["replicate"]
    valid = ((type(replicate) is int and replicate > 0)
             or (type(replicate) is float and math.isfinite(replicate)
                 and replicate > 0 and replicate.is_integer()))
    require(valid,
            f"{context}.replicate: expected a positive integer")
    return value["task_id"], int(replicate)


def nullable_nonnegative(value, context):
    if value is None:
        return
    require(type(value) in (int, float),
            f"{context}: expected a number or null (not a boolean)")
    try:
        valid = math.isfinite(value) and value >= 0
    except OverflowError:
        valid = False
    require(valid, f"{context}: expected a finite nonnegative number or null")


def validate_manifest(manifest):
    fields(manifest, MANIFEST_FIELDS, "manifest")
    require(manifest["schema_version"] == "0.1", "manifest: unsupported schema_version")
    for field in ("experiment_id", "task_suite_id", "task_suite_revision"):
        nonempty_string(manifest[field], f"manifest.{field}")
    for field, choices in (
        ("data_kind", ("synthetic", "measured")),
        ("currency", ("EUR", "USD")),
        ("cost_basis", ("api_equivalent", "marginal_cash", "fully_loaded")),
    ):
        require(manifest[field] in choices, f"manifest.{field}: expected one of {choices}")
    systems = manifest["systems"]
    require(isinstance(systems, list) and bool(systems),
            "manifest.systems: expected a nonempty list")
    for system in systems:
        nonempty_string(system, "manifest.systems item")
    require(len(set(systems)) == len(systems), "manifest.systems: duplicate system")
    trials = manifest["trials"]
    require(isinstance(trials, list) and bool(trials),
            "manifest.trials: expected a nonempty list")
    keys = []
    for index, trial in enumerate(trials):
        context = f"manifest.trials[{index}]"
        fields(trial, {"task_id", "replicate"}, context)
        keys.append(trial_key(trial, context))
    require(len(set(keys)) == len(keys), "manifest.trials: duplicate task/replicate")
    return keys


def metric_summary(rows, field, scheduled):
    values = [row[field] for row in rows if row[field] is not None]
    total = math.fsum(values)
    return {
        "known_trials": len(values),
        "missing_or_unknown_trials": scheduled - len(values),
        "known_total": total,
        "mean_known": total / len(values) if values else None,
    }


def summarize(manifest, records):
    """Return a report, rejecting malformed, duplicate, or unexpected records."""
    keys = validate_manifest(manifest)
    expected = {(system, *key) for system in manifest["systems"] for key in keys}
    observed = {}
    for index, record in enumerate(records):
        context = f"record {index + 1}"
        fields(record, TRIAL_FIELDS, context)
        require(record["schema_version"] == "0.1", f"{context}: unsupported schema_version")
        require(record["experiment_id"] == manifest["experiment_id"],
                f"{context}: experiment_id does not match manifest")
        nonempty_string(record["system_id"], f"{context}.system_id")
        key = (record["system_id"], *trial_key(record, context))
        require(key in expected, f"{context}: unexpected system/task/replicate {key}")
        require(key not in observed, f"{context}: duplicate system/task/replicate {key}")
        require(record["outcome"] in OUTCOMES, f"{context}: invalid outcome")
        require(type(record["critical_failure"]) is bool,
                f"{context}.critical_failure: expected a boolean")
        require(not (record["outcome"] == "accepted" and record["critical_failure"]),
                f"{context}: an accepted trial cannot have a critical failure")
        nonempty_string(record["trace_ref"], f"{context}.trace_ref")
        for field in ("cost", "wall_seconds", "human_minutes"):
            nullable_nonnegative(record[field], f"{context}.{field}")
        observed[key] = record

    reports = []
    for system in manifest["systems"]:
        rows = [observed[(system, *key)] for key in keys if (system, *key) in observed]
        missing = [{"task_id": key[0], "replicate": key[1]}
                   for key in keys if (system, *key) not in observed]
        counts = Counter(row["outcome"] for row in rows)
        accepted = counts["accepted"]
        known_costs = [row["cost"] for row in rows if row["cost"] is not None]
        known_total = math.fsum(known_costs)
        reasons = []
        if missing:
            reasons.append("missing_trials")
        if len(known_costs) != len(rows):
            reasons.append("unknown_costs")
        if not accepted:
            reasons.append("zero_accepted_trials")
        reports.append({
            "system_id": system,
            "scheduled_trials": len(keys),
            "observed_trials": len(rows),
            "missing_trials": missing,
            "complete": not missing,
            "accepted_trials": accepted,
            "outcome_counts": {outcome: counts[outcome] for outcome in OUTCOMES},
            "critical_failures": sum(row["critical_failure"] for row in rows),
            "success_rate": accepted / len(keys) if not missing else None,
            "known_cost_total": known_total,
            "known_cost_trials": len(known_costs),
            "cost_complete": not missing and len(known_costs) == len(rows),
            "cost_per_accepted_trial": known_total / accepted if not reasons else None,
            "cost_per_accepted_trial_unavailable_reasons": reasons,
            "wall_seconds": metric_summary(rows, "wall_seconds", len(keys)),
            "human_minutes": metric_summary(rows, "human_minutes", len(keys)),
        })
    report = {key: value for key, value in manifest.items() if key not in ("systems", "trials")}
    report["scheduled_trial_roster"] = [
        {"task_id": task_id, "replicate": replicate} for task_id, replicate in keys
    ]
    report["complete"] = all(item["complete"] for item in reports)
    report["systems"] = reports
    return report


def reject_constant(value):
    raise ValueError(f"invalid JSON numeric constant: {value}")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def read_json(text):
    return json.loads(text, parse_constant=reject_constant, object_pairs_hook=unique_object)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    parser.add_argument("trials", type=Path)
    args = parser.parse_args()
    try:
        manifest = read_json(args.experiment.read_text(encoding="utf-8"))
        records = [read_json(line) for line in args.trials.read_text(encoding="utf-8").splitlines()
                   if line.strip()]
        report = summarize(manifest, records)
        print(json.dumps(report, indent=2, allow_nan=False))
    except (OSError, ValueError, OverflowError) as error:
        print(f"Invalid experiment ledger: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
