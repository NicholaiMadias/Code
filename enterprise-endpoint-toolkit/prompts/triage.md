# Redacted AI prompt library (offline templates only)

Do not include device serial numbers, UPNs, user names, emails, bearer tokens, tenant domains, raw logs, or exported inventory. Review redaction and organizational AI policies before using any third-party model.

## Compliance triage

You are an endpoint engineer. Analyze the following **aggregated, synthetic** counts:
- High-risk noncompliant devices: {count_high}
- Stale devices: {count_stale}
- Unknown state: {count_unknown}

Return likely categories of root causes, safe read-only verification checks, and a human approval checklist. Do not invent tenant-specific facts or recommend bulk remediation without a change plan.

## Change review

Given a proposed endpoint-policy change, produce: impact summary, test ring, rollback conditions, monitoring checkpoints, security/privacy review, and explicit approval requirements. State what cannot be verified from aggregate data.
