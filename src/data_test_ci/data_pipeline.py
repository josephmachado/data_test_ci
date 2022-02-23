from typing import Any, Dict, List

import psycopg2.extras as p

from data_test_ci.utils.db import WarehouseConnection
from data_test_ci.utils.sde_config import get_warehouse_creds


def get_user_data() -> List[int]:
    user_ids = []
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        curr.execute("Select id from app.user")
        user_ids = curr.fetchall()
    return [int(u[0]) for u in user_ids]


def enrich_user_data(user_ids: List[int]) -> List[Dict[str, Any]]:
    id_name_map = {1: 'John', 2: 'Jane', 3: 'Doe'}
    enriched_data = []
    for id in user_ids:
        data = {'id': id, 'name': id_name_map.get(id, 'no name')}
        enriched_data.append(data)
    return enriched_data


def send_data_to_destination(data: List[Dict[str, Any]]):
    insert_query = '''
    INSERT INTO app.enriched_data (
        id,
        name
    )
    VALUES (
        %(id)s,
        %(name)s
    )
    '''
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        p.execute_batch(curr, insert_query, data)


def run() -> None:
    send_data_to_destination(enrich_user_data(get_user_data()))


if __name__ == '__main__':
    run()
