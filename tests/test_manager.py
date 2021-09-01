import pytest


def test_available(note_manager):
    print(note_manager.NOTES_DIR)
    assert note_manager.available_notes == ["Test Note"]


@pytest.mark.parametrize(
    "topic, expected", [("test note", "Test Note"), ("fdajfldajfdkajfda", "")]
)
def test_closest(topic, expected, note_manager):
    assert note_manager.closest_note(topic) == expected


def test_empty(empty_note_manager):
    assert empty_note_manager.no_notes
    assert empty_note_manager.available_notes == []


@pytest.mark.parametrize(
    "topic, expected", [("Test Note", True), ("Another Note", False)]
)
def test_exists(topic, expected, note_manager):
    assert note_manager.already_exists(topic) == expected


@pytest.mark.parametrize(
    "topic, n, expected",
    [
        ("Test Note", 1, "First keyword"),
        (
            "Test Note",
            3,
            "First keyword\n\nThis is a test note. Second keyword found here",
        ),
    ],
)
def test_view(topic, n, expected, note_manager):
    assert note_manager.view_existing_notes(topic, n) == expected


@pytest.mark.parametrize(
    "keyword, size, expected",
    [
        ("First keyword", 0, ["0 First keyword"]),
        ("First keyword", 1, ["0 First keyword\n1"]),
        (
            "Second keyword",
            0,
            ["2 This is a test note. Second keyword found here"],
        ),
        (
            "Second keyword",
            1,
            ["1 \n2 This is a test note. Second keyword found here\n3"],
        ),
        (
            "Third keyword",
            0,
            ["5 Looking for a Third keyword here."],
        ),
        (
            "keyword",
            0,
            [
                "0 First keyword",
                "2 This is a test note. Second keyword found here",
                "5 Looking for a Third keyword here.",
            ],
        ),
        ("missing keyword", 0, []),
    ],
)
def test_search_notes(keyword, size, expected, note_manager):
    results = note_manager.search_notes("Test Note", keyword, size)
    assert results == expected


@pytest.mark.parametrize(
    "section_name, expected",
    [
        ("TODO", "Here is a todo item\nAnother todo item"),
        ("MISSING SECTION", ""),
        ("ANOTHER SECTION", "Included"),
    ],
)
def test_search_section(section_name, expected, note_manager):
    results = note_manager.search_section("Test Note", section_name)
    assert results == expected
