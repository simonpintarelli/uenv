class Record:

    def __init__(self, system: str, uarch: str, name: str, version: str, tag: str, date: str, size_bytes: int, sha256: str):
        self._system  = system
        self._uarch   = uarch
        self._name    = name
        self._version = version
        self._tag     = tag
        self._date    = date
        self._bytes   = size_bytes
        self._sha256  = sha256

    # build/eiger/zen2/cp2k/2023/1133706947
    @classmethod
    def frompath(cls, path: str, date: str, size_bytes: int, sha256: str):
        fields = path.split("/")
        if len(fields) != 5:
            raise ValueError("Record must have exactly 5 fields")

        system, uarch, name, version, tag = fields
        return cls(system, uarch, name, version, tag, date, size_bytes, sha256)

    @classmethod
    def fromjson(cls, raw: dict):
        system = raw["system"]
        uarch = raw["uarch"]
        name = raw["name"]
        version = raw["version"]
        tag = raw["tag"]
        date = to_datetime(raw["date"])
        size_bytes = raw["size"]
        sha256 = raw["sha256"]

        return cls(system, uarch, name, version, tag, date, size_bytes, sha256)

    def __eq__(self, other):
        if not isinstance(other, Record):
            return False
        return self.sha256==other.sha256

    def __lt__(self, other):
        if self.system  < other.system: return True
        if other.system < self.system: return False
        if self.uarch   < other.uarch: return True
        if other.uarch  < self.uarch: return False
        if self.name    < other.name: return True
        if other.name   < self.name: return False
        if self.version < other.version: return True
        if other.version< self.version: return False
        if self.tag     < other.tag: return True
        #if other.tag    < self.tag: return False
        return False

    def __str__(self):
        return f"{self.name}/{self.version}:{self.tag} @ {self.system}:{self.uarch}"

    def __repr__(self):
        return f"Record({self.system}, {self.uarch}, {self.name}, {self.version}, {self.tag})"

    @property
    def system(self):
        return self._system

    @property
    def uarch(self):
        return self._uarch

    @property
    def name(self):
        return self._name

    @property
    def date(self):
        return self._date

    @property
    def version(self):
        return self._version

    @property
    def tag(self):
        return self._tag

    @property
    def sha256(self):
        return self._sha256

    @property
    def size(self):
        return self._bytes

    @property
    def datestring(self):
        return self.date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    @property
    def path(self):
        return f"{self.system}/{self.uarch}/{self.name}{self.version}/{self.tag}"

    @property
    def dictionary(self):
        return {
                "system": self.system,
                "uarch": self.uarch,
                "name": self.name,
                "date": self.datestring,
                "version": self.version,
                "tag": self.tag,
                "sha256": self.sha256,
                "size": self.size
            }
