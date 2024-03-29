from pathlib import Path

from komodo.proto.generated.collection_pb2 import File
from komodo.shared.documents.text_extract_helper import TextExtractHelper


class KomodoCollection:
    def __init__(self, *, shortcode, name, description, files=None, cache=None):
        self.shortcode = shortcode
        self.guid = shortcode
        self.name = name
        self.description = description
        self.files: [File] = files or []
        self.cache = cache

    def __str__(self):
        return f"KomodoCollection(name={self.name}, guid={self.guid}, description={self.description})"

    def __eq__(self, other):
        if not isinstance(other, KomodoCollection):
            return False
        return self.guid == other.guid

    def __hash__(self):
        return self.guid

    def get_file_text(self, file):
        return TextExtractHelper(Path(file.path), cache_path=self.cache).extract_text()
