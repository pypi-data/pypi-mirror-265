import pytest
from hoptest.hoptest import commit_message_format


@pytest.mark.parametrize(
    "msg,result",
    (
        ("hello\n\nworld", True),
        ("[prefix]: hello\n\nworld", True),
        ("hello\nworld", False),
        ("h" * 53 + "\n\ntext", False),
        ("h" + "\n\n" + "z" * 71 + "\n\nanother line", True),
        ("h" + "\n\n" + "z" * 79, False),
    ),
)
def test_commit_message_regex(msg, result):
    assert commit_message_format(msg) is result
