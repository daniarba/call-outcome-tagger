import unittest

from call_outcome_tagger import Call, tag


def t(text, **kw):
    return tag(Call(text, **kw))


class OutcomeTests(unittest.TestCase):
    def test_booked(self):
        r = t("AI: I have Tuesday 3 pm open. You're booked.\nCaller: Great, see you Tuesday.")
        self.assertEqual(r.outcome, "booked")
        self.assertGreaterEqual(r.confidence, 0.6)
        self.assertIn("calendar", r.next_step)

    def test_rescheduled(self):
        r = t("Caller: Something came up, can we move it to Friday?\nAI: Sure, I moved you to Friday 10 am.")
        self.assertEqual(r.outcome, "rescheduled")

    def test_urgent_beats_booking(self):
        r = t("Caller: My water pipe is leaking everywhere, right now!\nAI: I'm booked, send someone today.")
        self.assertEqual(r.outcome, "urgent")

    def test_declined(self):
        r = t("Caller: Not interested, we already have someone. Stop calling.")
        self.assertEqual(r.outcome, "declined")

    def test_callback(self):
        r = t("Caller: I'll think about it, call me back tomorrow.")
        self.assertEqual(r.outcome, "callback")

    def test_no_answer_empty(self):
        r = t("")
        self.assertEqual(r.outcome, "no_answer")
        self.assertEqual(r.confidence, 0.0)

    def test_no_answer_voicemail_marker(self):
        r = t("[voicemail]")
        self.assertEqual(r.outcome, "no_answer")

    def test_extraction(self):
        r = t("Caller: Hi, this is Omar, calling for a cleaning on Tuesday the 3rd at 2:30 pm.\nAI: You're booked.")
        self.assertEqual(r.extracted.get("caller_name"), "Omar")
        self.assertEqual(r.extracted.get("service"), "cleaning")
        self.assertIn("Tuesday", r.extracted.get("when", ""))

    def test_other(self):
        r = t("Caller: What are your opening hours?")
        self.assertEqual(r.outcome, "other")


if __name__ == "__main__":
    unittest.main()
