from typing import Literal, AsyncIterable, TypedDict, Unpack
from aiosqlite import Connection

class Params(TypedDict):
  db: Connection
  table: str

async def create(*, dtype: Literal['JSON', 'BLOB'] = 'JSON', **p: Unpack[Params]):
  """Create a key-value table"""
  query = f'''
    CREATE TABLE IF NOT EXISTS {p['table']} (
        ID TEXT PRIMARY KEY,
        DATA {dtype}
      )
  '''
  async with p['db'].execute(query):
    ...

async def insert(id: str, data, **p: Unpack[Params]):
  query = f'INSERT INTO {p["table"]} (ID, DATA) VALUES (?, ?)'
  async with p['db'].execute(query, [id, data]):
    await p['db'].commit()

async def read(id: str, **p: Unpack[Params]) -> str | None:
  """Point read by ID"""
  query = f'SELECT DATA FROM {p["table"]} WHERE ID = ?'
  async with p['db'].execute(query, [id]) as cur:
    row = await cur.fetchone()
    return row and row[0]
  
async def readall(*, batch_size: int = 256, **p: Unpack[Params]) -> AsyncIterable[tuple[str, str]]:
  """List all"""
  query = f'SELECT ID, DATA FROM {p["table"]}'
  async with p['db'].execute(query) as cur:
    while (batch := await cur.fetchmany(batch_size)) != []:
      for row in batch:
        yield row

async def delete(id: str, **p: Unpack[Params]):
  """Point delete by ID"""
  query = f'DELETE FROM {p["table"]} WHERE ID = ?'
  async with p['db'].execute(query, [id]):
    await p['db'].commit()

async def update(id: str, data, **p: Unpack[Params]):
  query = f'UPDATE {p["table"]} SET DATA = ? WHERE ID = ?'
  async with p['db'].execute(query, [data, id]):
    await p['db'].commit()

async def upsert(id: str, data, **p: Unpack[Params]):
  query = f'''
    INSERT INTO {p["table"]} (ID, DATA) VALUES (?1, ?2)
    ON CONFLICT(ID) DO UPDATE SET DATA=?2
  '''
  async with p['db'].execute(query, [id, data]):
    await p['db'].commit()