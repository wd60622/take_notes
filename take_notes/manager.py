import os

from itertools import islice

class NoteManager:
    def __init__(self):
        if not os.path.exists(self.NOTES_DIR):
            self.create_notes_location()

    @property
    def NOTES_DIR(self):
        return os.path.join(os.environ["HOME"], ".notes")

    def create_notes_location(self):
        os.mkdir(self.NOTES_DIR)

    @property
    def available_notes(self) -> list:
        files = os.listdir(self.NOTES_DIR)
        files = [file for file in files if file.endswith(".txt")]
        topics = [file.replace(".txt", "") for file in files]

        topics.sort()

        return topics

    @property
    def no_notes(self):
        return len(self.available_notes) == 0

    def already_exists(self, topic):
        return topic in self.available_notes

    def search_notes(self, topic, keyword) -> Tuple:
        file = self._file_name(topic)

        keyword = keyword.lower()

        lines = self._read_lines(file)
        locations = [i for i, line in enumerate(lines) if keyword in line.lower()]

        start_ends = [(max(loc - 1, 0), loc + 2) for loc in locations]

        def slice(lines, start, end):
            if start == 0:
                return lines[:end]

            return lines[start:end]

        places = [slice(lines, start, end) for start, end in start_ends]
        new_lines = ["".join(place).strip() for place in places]

        return new_lines

    def _read_lines(self, file):
        with open(file, "r") as f:
            lines = f.readlines()

        return lines


    def create_new_notes(self, topic=None):
        file = self._file_name(topic)
        os.system(f"touch '{file}'")

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
        os.system(f"rm '{file}'")

    def move_existing_notes(self, topic, new_topic):
        file = self._file_name(topic)
        new_file = self._file_name(new_topic)
        os.system(f"mv '{file}' '{new_file}'")

    def _file_name(self, topic):
        return os.path.join(self.NOTES_DIR, f"{topic}.txt")
