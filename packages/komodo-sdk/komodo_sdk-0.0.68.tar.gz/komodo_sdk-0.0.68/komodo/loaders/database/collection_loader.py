from komodo.framework.komodo_collection import KomodoCollection
from komodo.store.collection_store import CollectionStore


class CollectionLoader:

    @classmethod
    def load(cls, shortcode) -> KomodoCollection:
        collection = CollectionStore().retrieve_collection(shortcode)
        print(collection)
        return KomodoCollection(shortcode=collection.shortcode, name=collection.name,
                                description=collection.description,
                                files=collection.files)
