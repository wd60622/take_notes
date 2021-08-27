import os

import pytest

from take_notes.manager import NoteManager

test_dir = os.path.abspath(os.path.join(__file__, "../test_data"))


@pytest.fixture
def note_manager(mocker):
    mocker.patch("take_notes.manager.NoteManager.NOTES_DIR", new=test_dir)
    return NoteManager()


@pytest.fixture
def empty_note_manager(mocker):
    mocker.patch("take_notes.manager.NoteManager.available_notes", new=[])
    return NoteManager()
