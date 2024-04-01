from pathlib import Path

from komodo.framework.komodo_context import KomodoContext
from komodo.proto.generated.collection_pb2 import File
from komodo.shared.documents.text_extract_helper import TextExtractHelper
from komodo.store.proto_utils import convert_proto_to_dict


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

    def get_collection_context(self):
        context = KomodoContext()
        numfiles = len(self.files)
        max_size = 100000
        if numfiles > 0:
            max_size = 100000 // numfiles
        total_size = 0

        context.add("Collection Name", self.name)
        for file in self.files:
            text = self.get_file_text(file)
            if len(text) > max_size:
                text = text[:max_size]
            total_size += len(text)

            context.add(file.name, convert_proto_to_dict(file))
            context.add(file.name + " Contents", text)
            context.add(file.name + " Page length", "500 words")
            
            print("Added file to context: ", file.name, " with text length: ", len(text))
            if numfiles > 1:
                max_size = (100000 - total_size) // (numfiles - 1)
                numfiles -= 1

        return context

    def get_collection_summary(self):
        return {
            "name": self.name,
            "description": self.description,
            "files": [f.name for f in self.files]
        }

    def get_collection_summary_for_user(self):
        return "Collection: " + self.name + "\n" + "Description: " + self.description + "\n" + "Files: " + str(
            [f.name for f in self.files]) + "\n"
