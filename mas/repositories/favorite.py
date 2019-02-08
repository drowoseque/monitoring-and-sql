from typing import List
from asyncpg.exceptions import UniqueViolationError
from mas.helpers import postgres

_GET_BY_USER_ID_QUERY = 'SELECT object_id FROM favorite.authorized_users WHERE user_id = $1'
_INSERT_QUERY = 'INSERT INTO favorite.authorized_users (user_id, object_id, time_added) VALUES ($1, $2, CURRENT_TIMESTAMP)'


async def get(*, user_id: int) -> List[int]:
    records = await postgres.execute(
        query=_GET_BY_USER_ID_QUERY,
        params=(user_id,)
    )
    return [record.get('object_id') for record in records]


async def add(*, user_id: int, object_id: int) -> None:
    try:
        await postgres.execute(
            query=_INSERT_QUERY,
            params=(user_id, object_id)
        )
    except UniqueViolationError:
        pass
