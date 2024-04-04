import os
from pathlib import Path

from komodo.framework.komodo_context import KomodoContext
from komodo.shared.documents.file_writer_helper import FileWriterHelper
from komodo.shared.documents.text_extract_helper import TextExtractHelper
from komodo.shared.utils.digest import get_num_tokens
from komodo.shared.utils.filestats import file_details
from komodo.store.collection_store import CollectionStore


class KomodoCollection:
    def __init__(self, *, shortcode, name, path, description, files=None, user=None, cache=None):
        self.shortcode = shortcode
        self.guid = shortcode
        self.name = name
        self.path = path
        self.description = description
        self.files: [Path] = files or []
        self.cache = cache
        self.user = user

        # files can be a list of strings or paths
        self.files = [Path(f) for f in self.files]

        # make sure the directory exists
        os.makedirs(self.path, exist_ok=True)

    def __str__(self):
        return f"KomodoCollection(name={self.name}, guid={self.guid}, description={self.description})"

    def __eq__(self, other):
        if not isinstance(other, KomodoCollection):
            return False
        return self.guid == other.guid

    def __hash__(self):
        return self.guid

    def get_total_tokens(self) -> int:
        total_tokens = 0
        for file in self.files:
            text = self.get_file_text(file)
            total_tokens += get_num_tokens(text)
        return total_tokens

    def get_file_text(self, path: Path):
        return TextExtractHelper(Path(path), cache_path=self.cache).extract_text()

    def get_collection_context(self, max_size=100000):
        context = KomodoContext()
        context.add("Collection Name", self.name)
        total_size = 0
        total_files = len(self.files)

        for index, file in enumerate(self.files):
            max_per_file = (max_size - total_size) // (total_files - index)

            text = self.get_file_text(file)
            actual = len(text)
            fitted = actual if actual < max_per_file else max_per_file
            text = text[:fitted]
            total_size += fitted

            context.add(file.stem + " Path", str(file))
            context.add(file.stem + " Contents", text)

            print("Added file to context: ", file.name, " with text length: ", len(text), " actual size: ", actual)

        return context

    def get_collection_summary(self):
        return {
            "name": self.name,
            "description": self.description,
            "files": [f.name for f in self.files]
        }

    def get_collection_summary_for_user(self):
        return "Collection: " + self.name + "\n" + "Description: " + self.description + "\n" + "Files: " + str(
            [f.stem for f in self.files]) + "\n"

    def add_file(self, filename: str, contents: str, mode: str, existing_behavior: str) -> Path:
        path = self.path / filename
        helper = FileWriterHelper(self.path, filename, mode)
        helper.write_to_file(contents, existing_behavior)
        self.files.append(path)
        self.update([path])
        return path

    def sync(self):
        files = [self.path / f for f in os.listdir(self.path) if f[0] != '.' and f[-1] != '~']
        self.update(files)

    def update(self, files):
        store = CollectionStore()
        collection = store.get_or_create_collection(self.shortcode, self.path, self.name, self.description)
        if user := self.user:
            store.add_user_collection(user.email, self.shortcode)

        for file in collection.files:
            if not Path(file.path).exists():
                store.remove_file_in_collection(collection, file.path)

        for path in files:
            file = file_details(path)
            store.upsert_file_in_collection(collection, file)
            
        store.store_collection(collection)
