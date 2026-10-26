"""The tagging engine: evidence in, one outcome out."""
from __future__ import annotations

from .models import Call, Outcome
from . import rules as R


def tag(call: Call) -> Outcome:
    evidence = []
    extracted = {}

    text_lines = list(call.lines())
    body = "\n".join(text_lines)
    if not body.strip():
        return Outcome(R.NO_ANSWER, 0.0, ["empty transcript"], {}, "log and move on")

    # 1. Evidence scan
    scores = {name: [] for name in R.RULES}
    for line in text_lines:
        for outcome, patterns in R.RULES.items():
            for pat in patterns:
                m = pat.search(line)
                if m:
                    scores[outcome].append((pat.pattern, line))
                    evidence.append(f"{outcome}: {line}")

    # 2. Extraction (facts a CRM row needs)
    dm = R.DATETIME.search(body)
    if dm:
        extracted["when"] = dm.group(0)
    nm = R.NAME.search(body)
    if nm:
        extracted["caller_name"] = nm.group(1)
    sm = R.SERVICE.search(body)
    if sm:
        extracted["service"] = sm.group(2).lower()

    # 3. Pick the outcome
    if R.URGENT_BEATS_EVERYTHING and scores[R.URGENT]:
        outcome = R.URGENT
    else:
        outcome = max(scores, key=lambda k: len(scores[k]))
        if not scores[outcome]:
            outcome = R.OTHER
    matched = scores.get(outcome, [])
    confidence = round(min(1.0, 0.4 + 0.2 * len(matched)), 2)

    next_step = {
        R.BOOKED: "sync booking to calendar + CRM",
        R.RESCHEDULED: "update the existing calendar entry",
        R.URGENT: "page the on-call team immediately",
        R.DECLINED: "log as lost, stop follow-ups",
        R.CALLBACK: "queue a follow-up task for staff",
        R.NO_ANSWER: "log as no-answer, retry once later",
        R.OTHER: "log for human review",
    }[outcome]

    return Outcome(outcome, confidence, evidence, extracted, next_step)
