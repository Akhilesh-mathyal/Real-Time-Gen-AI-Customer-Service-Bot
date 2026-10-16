from service import fallback_reply, relevant_context

def test_relevant_context_matches_shipping():
    assert "3–5 business days" in relevant_context("when will delivery arrive?")

def test_fallback_unknown_offers_human_help():
    assert "support agent" in fallback_reply("Can I order a helicopter?")
