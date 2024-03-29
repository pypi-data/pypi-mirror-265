import os
from pathlib import Path

from komodo.framework.komodo_locations import KomodoLocations


class KomodoConfig:

    def __init__(self, **kwargs):
        self.data_directory = kwargs.get("data_directory", None)
        self.definitions_directory = kwargs.get("definitions_directory", None)
        self.kwargs = kwargs

        if self.data_directory is None:
            self.data_directory = self.get_default_data_directory()

    def get_default_data_directory(self):
        path = os.getenv("KOMODO_DATA_DIR")
        if path is None:
            if os.path.exists("/data/komodo"):
                path = "/data/komodo"

        if path is None or not os.path.exists(path):
            raise Exception("Default data directory not found. Please set KOMODO_DATA_DIR environment variable.")

        return Path(path)

    def locations(self):
        return KomodoLocations(self.data_directory)

    def shared(self):
        return self.locations().shared()

    def cache(self):
        return self.locations().cache()

    def get_value(self, key):
        return self.kwargs[key]

    def get_secret(self, name, default=None) -> str:
        if name in self.kwargs:
            return self.kwargs[name]

        if name not in os.environ and default is None:
            raise Exception(f"{name} not found in environment.")

        return os.getenv(name, default)


if __name__ == "__main__":
    config = KomodoConfig(data_directory="data", definitions_directory="definitions",
                          MONGO_URL="mongodb://root:example@localhost:27017/", ELASTIC_URL="http://localhost:9200",
                          SERP_API_KEY="123")
    print(config.get_value("data_directory"))
    print(config.get_value("definitions_directory"))
    print(config.get_value("SERP_API_KEY"))
