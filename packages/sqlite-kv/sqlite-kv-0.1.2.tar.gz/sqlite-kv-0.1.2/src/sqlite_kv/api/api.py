from typing import Callable, TypeVar, Generic, AsyncIterable
from dataclasses import dataclass
from ..decorators import with_args, with_args_gen
from ..ops import create, delete, upsert, read, readall
import json

async def then(f, x):
    """aka `fmap` aka `<$>` for the `Future` monad"""
    return f(await x)

T = TypeVar('T')

@dataclass
class SQLiteKV(Generic[T]):

  db_path: str = 'db.sqlite'
  table: str = 'kv'
  parse: Callable[[str], T] = lambda x: x
  dump: Callable[[T], str] = lambda x: x
  dtype: str = 'TEXT'

  @classmethod
  def new(cls, *args, create = True, **kw) -> 'SQLiteKV':
    obj = cls(*args, **kw)
    return then(lambda _: obj, obj.create()) if create else obj
  
  @classmethod
  def documents(cls, db_path: str = 'db.sqlite', table: str = 'documents', create = True) -> 'SQLiteKV[dict]':
    """Create a JSON documents key-value DB"""
    return SQLiteKV.new(parse=json.loads, dump=json.dumps, dtype='JSON', db_path=db_path, table=table, create=create)
  
  @classmethod
  def blobs(cls, db_path: str = 'db.sqlite', table: str = 'blobs', create = True) -> 'SQLiteKV[dict]':
    """Create a BLOB key-value DB"""
    return SQLiteKV.new(dtype='BLOB', db_path=db_path, table=table, create=create)


  def _wrap(self, f):
    return with_args(self.db_path, self.table)(f)
  
  def _wrap_gen(self, f):
    return with_args_gen(self.db_path, self.table)(f)

  async def create(self, **kw):
    """Create the DB (if it didn't exist). Automatically called by factory static methods"""
    return await self._wrap(create)(dtype=self.dtype, **kw)

  async def upsert(self, key: str, value: T, **kw):
    return await self._wrap(upsert)(key, self.dump(value), **kw)

  async def read(self, key: str, **kw) -> T | None:
    r = await self._wrap(read)(key, **kw)
    return r and self.parse(r)

  async def readall(self, batch_size: int = 256, **kw) -> AsyncIterable[tuple[str, T]]:
    async for k, v in self._wrap_gen(readall)(batch_size=batch_size, **kw):
      yield k, self.parse(v)

  async def delete(self, key: str, **kw):
    await self._wrap(delete)(key, **kw)

