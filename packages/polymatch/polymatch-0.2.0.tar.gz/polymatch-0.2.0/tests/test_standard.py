data = (
    ("exact::a", "a", True),
    ("exact::b", "n", False),
    ("exact::cc", "cc", True),
    ("contains::air", "i", False),
    ("contains::i", "air", True),
)


def test_patterns():
    from polymatch import pattern_registry
    for pattern, text, result in data:
        matcher = pattern_registry.pattern_from_string(pattern)
        matcher.compile()
        assert bool(matcher == text) is result


def test_invert():
    from polymatch import pattern_registry
    pattern = pattern_registry.pattern_from_string("~exact::beep")
    pattern.compile()
    assert pattern.inverted
