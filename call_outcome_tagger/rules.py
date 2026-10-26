"""Outcome rules: regex evidence patterns per outcome class.

Each rule maps one outcome to evidence phrases an AI receptionist call
actually produces. Rules are additive: more matches, higher confidence.
"""
from __future__ import annotations

import re

BOOKED = "booked"
RESCHEDULED = "rescheduled"
URGENT = "urgent"
DECLINED = "declined"
CALLBACK = "callback"
NO_ANSWER = "no_answer"
OTHER = "other"

BOOKED_PATTERNS = [
    r"\b(you'?re|you are|we'?ve got you|i'?ve got you) (booked|all set|on the calendar)\b",
    r"\bbooked (you|for|on)\b",
    r"\bconfirmed (your|the) (appointment|booking|slot|reservation)\b",
    r"\bappointment is (set|confirmed|booked)\b",
    r"\bslot (is )?(reserved|yours|confirmed)\b",
    r"\bsee you (on|at|this) \b",
    r"\bi'?ll (add|put) (you|that) (on the )?calendar\b",
]

RESCHEDULED_PATTERNS = [
    r"\b(reschedul(e|ed|ing)|move (you|it|that) to|push(ed)? (it|that|the appointment) to)\b",
    r"\bwhat about (another|a different) (day|time)\b",
    r"\bchange (your|the) appointment\b",
    r"\bcan we move\b",
]

URGENT_PATTERNS = [
    r"\b(emergency|urgent|right now|as soon as possible|asap)\b",
    r"\b(water|pipe|gas) (is )?(everywhere|leaking|leak|smell)\b",
    r"\b(serve|send) (someone|a tech|a technician|emergency)\b",
    r"\bcan'?t wait\b",
    r"\b(severe|bad) (pain|bleeding)\b",
    r"\bknock(ed)? (out|down) (a )?(power|line|pole)\b",
]

DECLINED_PATTERNS = [
    r"\b(not interested|no thanks|no thank you|pass for now)\b",
    r"\b(already (have|got)|we (use|have)) (someone|another|a different)\b",
    r"\bdon'?t (book|schedule) anything\b",
    r"\bcancel (my|the|that) (appointment|booking|order)\b",
    r"\bstop calling\b",
]

CALLBACK_PATTERNS = [
    r"\b(call (you|me) (back|later)|we'?ll call (you|me) back|call me back)\b",
    r"\b(get back to (you|me)|follow up (later|tomorrow|next week))\b",
    r"\bi'?ll (think about it|check my schedule|call you later)\b",
    r"\breach(ed)? out (later|tomorrow)\b",
]

NO_ANSWER_PATTERNS = [
    r"^\[?(voicemail|no answer|not picked up|line busy|caller hung up before answer)\]?$",
    r"\bleft (a )?voicemail\b",
    r"\bno (one|body) (answered|picked up)\b",
]

RULES = {
    BOOKED: [re.compile(p, re.IGNORECASE) for p in BOOKED_PATTERNS],
    RESCHEDULED: [re.compile(p, re.IGNORECASE) for p in RESCHEDULED_PATTERNS],
    URGENT: [re.compile(p, re.IGNORECASE) for p in URGENT_PATTERNS],
    DECLINED: [re.compile(p, re.IGNORECASE) for p in DECLINED_PATTERNS],
    CALLBACK: [re.compile(p, re.IGNORECASE) for p in CALLBACK_PATTERNS],
    NO_ANSWER: [re.compile(p, re.IGNORECASE) for p in NO_ANSWER_PATTERNS],
}

# Extraction helpers: pull the facts a CRM row needs.
DATETIME = re.compile(
    r"\b(mon|tue|tues|wed|thu|thur|thurs|fri|sat|sun)[a-z]*day?\s*,?\s*"
    r"(the\s*)?(\d{1,2})(st|nd|rd|th)?\b"
    r"|\b(\d{1,2})(st|nd|rd|th)?\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b"
    r"|\b(tomorrow|today|next week)\b"
    r"|\b(\d{1,2}):(\d{2})\s*(am|pm)\b",
    re.IGNORECASE,
)
NAME = re.compile(r"\b(?:this is|my name is|it'?s)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)")
SERVICE = re.compile(r"\b(?:for|about|regarding)\s+(a\s+)?(cleaning|filling|extraction|checkup|consultation|check|repair|quote|estimate|trim|cut|cleaning service|inspection)\b", re.IGNORECASE)

URGENT_BEATS_EVERYTHING = True  # an urgent call routes first, whatever else it contains
