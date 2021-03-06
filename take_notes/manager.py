import os

from pathlib import Path

from itertools import islice, zip_longest

from difflib import SequenceMatcher


class FileExistsError:
    """Error for when file already exists."""


class NoteManager:
    def __init__(self):
        if not self.NOTES_DIR.exists():
            self.NOTES_DIR.mkdir()

    @property
    def NOTES_DIR(self):
        return Path.home() / ".notes"

    @property
    def available_notes(self) -> list:
        folder = self.NOTES_DIR
        topics = [
            str(file).replace(str(folder) + "/", "").replace(".txt", "")
            for file in folder.glob("*.txt")
        ]

        topics.sort()

        return topics

    def closest_note(self, topic) -> str:
        distances = [
            (SequenceMatcher(None, topic.lower(), potential.lower()).ratio(), potential)
            for potential in self.available_notes
        ]

        distances.sort(key=lambda x: x[0])

        if distances[-1][0] < 0.5:
            return ""

        return distances[-1][1]

    @property
    def no_notes(self):
        return len(self.available_notes) == 0

    def already_exists(self, topic):
        return topic in self.available_notes

    def search_section(self, topic, section_name) -> str:
        file = self._file_name(topic)

        lines = self._read_lines(file)

        start = -1
        for (i, line), next_line in zip_longest(enumerate(lines), lines[1:]):
            if line.strip() == section_name:
                start = i
            elif start != -1 and line.strip() == "":
                if next_line is None or next_line.strip() == "":
                    end = i
                    break
            else:
                end = i

        if start == -1:
            return ""

        return "".join(lines[start + 1 : end + 1]).strip()

    def search_notes(self, topic, keyword, size=0):
        file = self._file_name(topic)

        keyword = keyword.lower()

        lines = self._read_lines(file)

        locations = [i for i, line in enumerate(lines) if keyword in line.lower()]
        formated_lines = [f"{i} " + line for i, line in enumerate(lines)]

        start_ends = [(max(loc - size, 0), loc + size + 1) for loc in locations]

        def slice(start, end):
            if start == 0:
                return formated_lines[:end]

            return formated_lines[start:end]

        places = [slice(start, end) for start, end in start_ends]
        new_lines = ["".join(place).strip() for place in places]

        return new_lines

    def _read_lines(self, file):
        with open(file, "r") as f:
            lines = f.readlines()

        return lines

    def create_new_notes(self, topic=None):
        file = self._file_name(topic)
        file.touch()

    def open_existing_notes(self, topic):
        file = self._file_name(topic)
        os.system(f"vim '{file}'")

    def view_existing_notes(self, topic, n=5):
        file = self._file_name(topic)
        return self._read_n_lines(file, n)

    def _read_n_lines(self, file, n):
        with open(file, "r") as f:
            lines = list(islice(f, n))

        lines = "".join(lines).strip()
        return lines

    def delete_existing_notes(self, topic):
        file = self._file_name(topic)
        file.unlink()

    def rename_note(self, topic, new_topic):
        file = self._file_name(topic)
        new_file = self._file_name(new_topic)
        if new_file.exists():
            raise FileExistsError(f"{new_file} already exists.")

        file.rename(new_file)

    def _file_name(self, topic):
        return self.NOTES_DIR / f"{topic}.txt"
