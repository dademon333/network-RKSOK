"""Just a crutch to display non-ascii symbols in pytest reports correctly"""


def pytest_make_parametrize_id(config, val):
    return repr(val)
