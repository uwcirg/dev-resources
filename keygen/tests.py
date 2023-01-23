from .populate_keys import match, single_line

key = "__KEYCLOAK_FAKE_SECRET"
line_w_existing = f"{key}=existing-value"


def test_ignore_existing_match():
    assert match(line_w_existing, False) is False
    assert match(line_w_existing, True) == key+'='


def test_ignore_replace():
    assert single_line(line_w_existing, False) == line_w_existing
    assert single_line(line_w_existing, True) != line_w_existing
