import pickle

patterns = (
    "regex::test",
    "exact::test",
    "contains:cf:test",
    "glob::beep",
)


class C:
    def __init__(self, pat):
        self.patterns = [pat]


def pytest_generate_tests(metafunc):
    if 'pattern' in metafunc.fixturenames:
        metafunc.parametrize('pattern', patterns)

    if 'pickle_proto' in metafunc.fixturenames:
        metafunc.parametrize('pickle_proto', list(range(pickle.HIGHEST_PROTOCOL + 1)))


def cycle_pickle(obj, proto):
    return pickle.loads(pickle.dumps(obj, proto))


def test_compile_state(pattern, pickle_proto):
    from polymatch import pattern_registry
    compiled_pattern = pattern_registry.pattern_from_string(pattern)
    compiled_pattern.compile()

    assert compiled_pattern.is_compiled()

    uncompiled_pattern = pattern_registry.pattern_from_string(pattern)

    assert not uncompiled_pattern.is_compiled()

    pat1, pat2 = cycle_pickle((compiled_pattern, uncompiled_pattern), pickle_proto)

    assert pat1.is_compiled() is compiled_pattern.is_compiled()

    assert pat2.is_compiled() is uncompiled_pattern.is_compiled()


def test_properties(pattern, pickle_proto):
    from polymatch import pattern_registry
    pat = pattern_registry.pattern_from_string(pattern)
    pat.compile()

    inv_pat = pattern_registry.pattern_from_string('~' + pattern)
    inv_pat.compile()

    assert not pat.inverted
    assert inv_pat.inverted

    new_pat = cycle_pickle(pat, pickle_proto)
    new_inv_pat = cycle_pickle(inv_pat, pickle_proto)

    assert not new_pat.inverted
    assert new_inv_pat.inverted

    for _pat in cycle_pickle([pat], pickle_proto):
        assert not _pat.inverted

    for _pat in cycle_pickle(C(pat), pickle_proto).patterns:
        assert not _pat.inverted


def test_version_checks(pattern, pickle_proto):
    from polymatch import pattern_registry
    import polymatch
    pat = pattern_registry.pattern_from_string(pattern)
    pat.compile()

    assert pat.is_compiled()

    data = pickle.dumps(pat, pickle_proto)

    # Change version
    v = polymatch.__version__.split('.')
    v[-1] = str(int(v[-1]) + 1)
    polymatch.__version__ = '.'.join(v)

    new_pat = pickle.loads(data)

    assert new_pat.is_compiled()
