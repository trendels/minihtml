from minihtml import safe, text


def test_text_is_escaped():
    n = text("hi there & goodbye")

    assert str(n) == "hi there &amp; goodbye"


def test_safe_text_is_not_escaped():
    n = safe("hi there & goodbye")

    assert str(n) == "hi there & goodbye"
