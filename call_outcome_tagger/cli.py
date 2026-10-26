"""CLI: tag a transcript from a file or run the built-in demo."""
from __future__ import annotations

import argparse
import json
import sys

from .models import Call
from .tagger import tag

DEMO = """[voicemail]
AI: Thank you for calling Brightside Dental, this is the automated receptionist. How can I help?
Caller: Hi, this is Omar. I need a filling for Thursday the 5th at 2:30 pm, it's getting quite painful.
AI: Noted. I have Thursday the 5th at 2:30 pm open with Dr. Chen. You're booked.
Caller: Perfect, thank you.
AI: You're all set. See you Thursday.
"""


def build_parser():
    p = argparse.ArgumentParser(prog="call-outcome-tagger", description="Tag call transcripts with an outcome.")
    p.add_argument("--file", help="path to a .txt transcript")
    p.add_argument("--json", action="store_true", help="emit JSON")
    p.add_argument("--demo", action="store_true", help="run the built-in demo transcript")
    return p


def _emit(result, as_json):
    if as_json:
        print(json.dumps({
            "outcome": result.outcome,
            "confidence": result.confidence,
            "extracted": result.extracted,
            "next_step": result.next_step,
            "evidence": result.matched_evidence,
        }, indent=2))
    else:
        print(f"outcome:     {result.outcome}")
        print(f"confidence:  {result.confidence}")
        if result.extracted:
            print("extracted:   " + ", ".join(f"{k}={v}" for k, v in result.extracted.items()))
        print(f"next step:   {result.next_step}")
        for e in result.matched_evidence:
            print(f"  - {e}")


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.demo or not args.file:
        call = Call(DEMO, caller_phone="+15550001111", duration_sec=48)
    else:
        try:
            with open(args.file, encoding="utf-8") as f:
                call = Call(f.read())
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
    _emit(tag(call), args.json)
    return 0
