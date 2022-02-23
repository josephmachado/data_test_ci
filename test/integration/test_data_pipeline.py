import psycopg2.extras as p

from data_test_ci.data_pipeline import run
from data_test_ci.utils.db import WarehouseConnection
from data_test_ci.utils.sde_config import get_warehouse_creds


class TestDataPipeline:
    def setup_method(self, test_data_pipeline):
        insert_query = '''
            INSERT INTO app.user (
                id
            )
            VALUES (
                %(id)s
            )
        '''
        user_fixture = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}]
        with WarehouseConnection(
            get_warehouse_creds()
        ).managed_cursor() as curr:
            p.execute_batch(curr, insert_query, user_fixture)

    def teardown_method(self, test_data_pipeline):
        with WarehouseConnection(
            get_warehouse_creds()
        ).managed_cursor() as curr:
            curr.execute("TRUNCATE TABLE app.user;")
            curr.execute("TRUNCATE TABLE app.enriched_data;")

    def test_data_pipeline(self):
        run()
        with WarehouseConnection(
            get_warehouse_creds()
        ).managed_cursor() as curr:
            curr.execute("Select id, name from app.enriched_data")
            enriched_user_data = curr.fetchall()
        expected_data = [(1, 'John'), (2, 'Jane'), (3, 'Doe'), (4, 'no name')]
        assert enriched_user_data == expected_data
