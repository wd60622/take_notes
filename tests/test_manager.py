import pytest


def test_available(note_manager):
    print(note_manager.NOTES_DIR)
    assert note_manager.available_notes == ["Test Note"]


def test_empty(empty_note_manager):
    assert empty_note_manager.no_notes
    assert empty_note_manager.available_notes == []


@pytest.mark.parametrize(
    "topic, expected", [("Test Note", True), ("Another Note", False)]
)
def test_exists(topic, expected, note_manager):
    assert note_manager.already_exists(topic) == expected


@pytest.mark.parametrize("topic, n, expected", [("Test Note", 1, "First keyword"), ("Test Note", 3, "First keyword\n\nThis is a test note. Second keyword found here")])
def test_view(topic, n, expected, note_manager):
    assert note_manager.view_existing_notes(topic, n) == expected


@pytest.mark.parametrize(
    "keyword, expected",
    [
        ("First keyword", ["First keyword"]),
        (
            "Second keyword",
            ["This is a test note. Second keyword found here"],
        ),
        (
            "Third keyword",
            ["Surrounding text\nLooking for a Third keyword here.\nOther text"],
        ),
        (
            "keyword",
            [
                "First keyword",
                "This is a test note. Second keyword found here",
                "Surrounding text\nLooking for a Third keyword here.\nOther text",
            ],
        ),
        ("missing keyword", []),
    ],
)
def test_search(keyword, expected, note_manager):
    results = note_manager.search_notes("Test Note", keyword)
    assert results == expected
