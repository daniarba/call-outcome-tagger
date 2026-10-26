"""Data models for call outcome tagging."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Call:
    """A call transcript as lines of speaker text."""
    transcript: str
    caller_phone: str = ""
    duration_sec: int = 0
    started_at: str = ""  # ISO timestamp, passed through untouched

    def lines(self):
        for raw in self.transcript.splitlines():
            line = raw.strip()
            if line:
                yield line


@dataclass
class Outcome:
    """The tagged result of one call."""
    outcome: str                 # booked | rescheduled | declined | urgent | no_answer | callback | other
    confidence: float = 0.0      # 0..1, based on how many rules fired
    matched_evidence: list = field(default_factory=list)
    extracted: dict = field(default_factory=dict)   # datetime, name, service, etc.
    next_step: str = ""          # suggested routing for the business


OUTCOME_RULES_ORDER = ("booked", "rescheduled", "urgent", "declined", "callback", "no_answer")
