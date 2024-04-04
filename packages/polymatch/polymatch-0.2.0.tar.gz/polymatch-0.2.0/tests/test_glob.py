data = (
    ("glob::*", "", True),
    ("glob::*?", "", False),
    ("glob::*?", "a", True),
    ("glob:cf:*!*@thing", "itd!a@thing", True),
)


def test_patterns():
    from polymatch import pattern_registry
    for pattern, text, result in data:
        matcher = pattern_registry.pattern_from_string(pattern)
        matcher.compile()
        assert bool(matcher == text) is result


def test_invert():
    from polymatch import pattern_registry
    pattern = pattern_registry.pattern_from_string("~glob::beep")
    pattern.compile()
    assert pattern.inverted
