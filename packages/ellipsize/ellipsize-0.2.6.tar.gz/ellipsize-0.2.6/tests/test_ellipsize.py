from ellipsize.ellipsize import Dots, ellipsize, format_ellipsized, print_ellipsized


def test_ellipsize():
    a = [1, 2, 3]
    assert ellipsize(a, max_items_to_show=10) == a
    assert str(ellipsize(a, max_items_to_show=2)) == "[1, 2, ..]"
    assert str(ellipsize(a, max_items_to_show=3)) == str(a)
    assert ellipsize({"a": "12345", "b": a}, max_item_length=4, max_items_to_show=2) == {
        "a": "1234..",
        "b": [1, 2, Dots()],
    }
    assert (
        str(
            ellipsize(
                {"a": "12345", "b": a, "c": {"d": a}}, max_item_length=4, max_items_to_show=2
            )
        )
        == "{'a': '1234..', 'b': [1, 2, ..], 'c': {'d': [1, 2, ..]}}"
    )
    assert ellipsize(
        {"a": "12345", "b": a, "c": [{"d": a}, {}, {}]}, max_item_length=4, max_items_to_show=2
    ) == {"a": "1234..", "b": [1, 2, Dots()], "c": [{"d": [1, 2, Dots()]}, {}, Dots()]}


def test_format_ellipsized():
    a = [1, 2, 3]
    assert format_ellipsized(a, max_items_to_show=2) == "[1, 2, ..]"


def test_print_ellipsized(capsys):
    a = [1, 2, 3]
    print_ellipsized(a, max_items_to_show=2)
    assert capsys.readouterr().out == "[1, 2, ..]\n"

    print_ellipsized(a, "2nd", max_items_to_show=2, end="", sep="?")
    assert capsys.readouterr().out == "[1, 2, ..]?'2nd'"
