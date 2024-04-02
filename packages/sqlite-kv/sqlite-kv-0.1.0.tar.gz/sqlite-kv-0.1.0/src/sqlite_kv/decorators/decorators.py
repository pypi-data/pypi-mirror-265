from functools import wraps
import aiosqlite
from aiosqlite import Connection

def with_db(db_path: str = 'db.sqlite'):
  """Runs `coro` inside `async with aiosqlite.connect(db_path)` if `db is None`"""
  def decorator(coro):
    @wraps(coro)
    async def _f(*args, db: Connection = None, **kwargs):
      if db is None:
        async with aiosqlite.connect(db_path) as db:
          return await coro(*args, db=db, **kwargs)
      else:
        return await coro(*args, db=db, **kwargs)
    return _f
  return decorator

def with_db_gen(db_path: str = 'db.sqlite'):
  """Runs `asyncgen` inside `async with aiosqlite.connect(db_path)` if `db is None`"""
  def decorator(asyncgen):
    @wraps(asyncgen)
    async def _f(*args, db: Connection = None, **kwargs):
      if db is None:
        async with aiosqlite.connect(db_path) as db:
          async for x in asyncgen(*args, db=db, **kwargs):
            yield x
      else:
        async for x in asyncgen(*args, db=db, **kwargs):
            yield x
    return _f
  return decorator

def with_table(default_table: str):
  """Adds a default `table` parameter"""
  def decorator(func):
    @wraps(func)
    def _f(*args, table: str = None, **kwargs):
      return func(*args, table=table or default_table, **kwargs)
    return _f
  return decorator

def with_args(db_path: str, table: str):
  """Compose `with_db` and `with_table`"""
  def decorator(f):
    return with_table(table)(with_db(db_path)(f))
  return decorator

def with_args_gen(db_path: str, table: str):
  """Compose `with_db_gen` and `with_table`"""
  def decorator(f):
    return with_table(table)(with_db_gen(db_path)(f))
  return decorator