data = (
    (r"regex::\btest\b", "test", True),
    (r"regex::\btest\b", "test1", False),
    (r"regex::\btest\b", "test response", True),
    (r"regex:cf:\btest\b", "TEST", True),
)


def test_patterns():
    from polymatch import pattern_registry
    for pattern, text, result in data:
        matcher = pattern_registry.pattern_from_string(pattern)
        matcher.compile()
        assert bool(matcher == text) is result


def test_invert():
    from polymatch import pattern_registry
    pattern = pattern_registry.pattern_from_string("~regex::beep")
    pattern.compile()
    assert pattern.inverted
