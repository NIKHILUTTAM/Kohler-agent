"""Synthetic demo documents used to seed the knowledge base on first run.

Kept separate from ingestion.py so the (fairly long) text blocks don't
clutter the ingestion logic, and so a team can swap in real KOHLER policy
documents by simply pointing KOHLER_KNOWLEDGE_DIR elsewhere without touching
any code.
"""

from __future__ import annotations

DEMO_FILES: dict[str, str] = {
    "hr_policy.md": """# Demo HR Policy

## Flexible work
Employees may request flexible work arrangements through their manager and HR.
Approval depends on role requirements, business continuity, and local law.

## Annual leave
Employees should request planned leave through the approved HR system in advance.
The HR system and the employee's applicable local policy are the source of truth
for the available balance and notice period.

## Policy boundary
This demo policy is synthetic and is not an official KOHLER policy.
""",
    "finance_guidelines.md": """# Demo Finance Guidelines

## Purchase approvals
Every purchase must have a business purpose, an owner, and the approval required
by the applicable delegation-of-authority matrix. Splitting a purchase to avoid
an approval threshold is not permitted.

## Reimbursements
Expense claims should include an itemised receipt, transaction date, currency,
business purpose, and cost centre.

## Policy boundary
These are synthetic demo guidelines, not official KOHLER financial controls.
""",
    "customer_support.md": """# Demo Customer Support Playbook

## Escalation
Escalate a safety concern, suspected product defect, data privacy request, or
repeat unresolved complaint to the designated specialist queue. Include the
issue summary, product identifiers, steps already taken, and requested resolution.

## Response quality
Use plain language, avoid unsupported promises, and record the next action and owner.
""",
    "privacy_policy.md": """# Demo Privacy Policy

## Data minimisation
Collect only the information necessary for the stated business purpose. Do not
request passwords, payment card numbers, or secrets in a support conversation.

## Access requests
Route a personal-data access, correction, deletion, or objection request to the
privacy team using the approved process. Do not make a legal determination in chat.
""",
}
