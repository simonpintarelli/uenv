import os

import json
from record import Record
import terminal

UENV_CLI_API_VERSION=1

class DataStore:
    def __init__(self):
        # all images store with (key,value) = (sha256,Record)
        self._images = {}

        self._store = {"system": {}, "uarch": {}, "name": {}, "version": {}, "tag": {}}

    def add_record(self, r: Record, overwrite: bool = False):
        # test for collisions
        if (not overwrite) and (self._images.get(r.sha256, None) is not None):
            raise ValueError(f"an image with the hash {r.sha256} already exists")

        sha = r.sha256
        self._images[sha] = r
        self._store["system"] .setdefault(r.system, []).append(sha)
        self._store["uarch"]  .setdefault(r.uarch, []).append(sha)
        self._store["name"]   .setdefault(r.name, []).append(sha)
        self._store["version"].setdefault(r.version, []).append(sha)
        self._store["tag"]    .setdefault(r.tag, []).append(sha)

    def find_records(self, **constraints):
        if not constraints:
            raise ValueError("At least one constraint must be provided")

        for field in constraints:
            if field not in self._store:
                raise ValueError(f"Invalid field: {field}. Must be one of 'system', 'uarch', 'name', 'version', 'tag'")

        # Find matching records for each constraint
        matching_records_sets = [
            set(self._store[field].get(value, [])) for field, value in constraints.items()
        ]

        # Intersect all sets of matching records
        if matching_records_sets:
            unique = set.intersection(*matching_records_sets)
        else:
            unique = set()

        results = [self._images[sha] for sha in unique]
        results.sort(reverse=True)
        return results

    @property
    def images(self):
        return self._images

    def get_record(self, sha256: str) -> Record:
        return self._images.get(sha256, None)

    # Convert to a dictionary that can be written to file as JSON
    # The serialisation and deserialisation are central: able to represent
    # uenv that are available in both JFrog and filesystem directory tree.
    def serialise(self, version: int=UENV_CLI_API_VERSION):
        return {
                "API_VERSION": version,
                "images": [img.dictionary for img in self._images.values()]
        }

    # Convert to a dictionary that can be written to file as JSON
    # The serialisation and deserialisation are central: able to represent
    # uenv that are available in both JFrog and filesystem directory tree.
    @classmethod
    def deserialise(cls, datastore):
        result = cls()
        for img in datastore["images"]:
            result.add_record(Record.from_dictionary(img))

class FileSystemCache():
    def __init__(self, path: str):
        self._path = path
        self._index = path + "/index.json"

        if not os.path.exists(self._index):
            # error: cache does not exists
            raise FileNotFoundError(f"filesystem cache not found {self._path}")

        with open(self._index, "r") as fid:
            raw = json.loads(fid.read())
            self._database = DataStore()
            for img in raw["images"]:
                self._database.add_record(Record.fromjson(img))

    @staticmethod
    def create(path: str, exists_ok: bool=False):
        if not os.path.exists(path):
            terminal.info(f"FileSyStemCache: creating path {path}")
            os.makedirs(path)
        index_file = f"{path}/index.json"
        if not os.path.exists(index_file):
            terminal.info(f"FileSyStemCache: creating empty index {index_file}")
            empty_config = { "API_VERSION": UENV_CLI_API_VERSION, "images": [] }
            with open(index_file, "w") as f:
                # default serialisation is str to serialise the pathlib.PosixPath
                f.write(json.dumps(empty_config, sort_keys=True, indent=2, default=str))
                f.write("\n")

        terminal.info(f"FileSyStemCache: available {index_file}")

    @property
    def database(self):
        return self._database

    def add_record(self, record: Record):
        self._database.add_record(record)

    # The path where an image would be stored
    # will return a path even for images that are not stored
    def image_path(self, r: Record) -> str:
        return self._path + "/images/" + r.sha256

    # Return the full record for a given hash
    # Returns None if no image with that hash is stored in the repo.
    def get_record(self, sha256: str):
        return self._database.get_record(sha256)

    def publish(self):
        with open(self._index, "w") as f:
            # default serialisation is str to serialise the pathlib.PosixPath
            f.write(json.dumps(self._database.serialise(), sort_keys=True, indent=2, default=str))
            f.write("\n")

