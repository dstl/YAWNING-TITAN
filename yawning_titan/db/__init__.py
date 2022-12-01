from abc import abstractmethod
from typing import Final, List, Mapping, Union

from tinydb import TinyDB
from tinydb.queries import Query, QueryInstance
from tinydb.table import Document

from yawning_titan import DB_DIR


class YawningTitanTinyDB:

    @abstractmethod
    def __init__(self, name: str):
        self._name: Final[str] = name
        self._db = TinyDB(DB_DIR / f"{self._name}.json")

    @property
    def name(self):
        return self._name

    @property
    def db(self):
        return self._db

    @abstractmethod
    def insert(self, item: Mapping) -> int:
        return self.db.insert(item)

    @abstractmethod
    def all(self) -> List[Document]:
        return self.db.all()

    @abstractmethod
    def get(self, doc_id: int) -> Union[Document, None]:
        return self.db.get(doc_id=doc_id)

    @abstractmethod
    def search(self, query: QueryInstance) -> List[Document]:
        return self.db.search(query)


class YawningTitanQuery(Query):
    def __init__(self):
        super(YawningTitanQuery, self).__init__()

    def len_equals(self, i: int) -> QueryInstance:
        def test_len(val, i):
            try:
                return len(val) == i
            except TypeError:
                return False

        return self.test(test_len, i)